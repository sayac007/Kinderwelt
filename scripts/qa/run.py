#!/usr/bin/env python3
"""Reproducible technical evidence only. Never collects child observations."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from static_audit import audit

ROOT = Path(__file__).resolve().parents[2]
POLICY = json.loads((ROOT/"tests/qa/policy.json").read_text())
ERROR = re.compile(r"SCRIPT ERROR:|^ERROR:|Parse Error|\[GUT ERROR\]",re.M)


def digest():
    names = subprocess.check_output(["git","ls-files","-co","--exclude-standard","-z"],cwd=ROOT).decode().split("\0")
    value = hashlib.sha256()
    for name in sorted(set(filter(None,names))):
        if not (name.startswith(("core/","games/","content/","assets/","tests/","scripts/",".github/")) or name in {"project.godot","export_presets.cfg"}):
            continue
        path=ROOT/name
        if path.is_file():
            value.update(name.encode()+b"\0"+path.read_bytes())
    return value.hexdigest()


def validate_junit(path):
    tree=ET.parse(path)
    cases=tree.findall(".//testcase")
    if not cases or any(c.get("status")!="pass" or c.find("failure") is not None or c.find("skipped") is not None for c in cases):
        raise ValueError("JUnit contains failing/pending cases or no executed tests")
    if int(tree.getroot().get("tests","0")) != len(cases):
        raise ValueError("JUnit test count is inconsistent")
    for suite in tree.iter():
        if suite.tag in {"testsuite","testsuites"} and any(int(suite.get(key,"0")) for key in ["failures","errors","skipped"]):
            raise ValueError("JUnit reports failed or skipped work")
    if any(int(c.get("assertions","0")) <= 0 for c in cases):
        raise ValueError("A framework test has no assertions")
    assertions=sum(int(c.get("assertions","0")) for c in cases)
    if assertions<=0:
        raise ValueError("No framework assertions executed")
    return {"tests":len(cases),"assertions":assertions,"failed":0,"skipped":0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="New output directory; existing paths are refused")
    args=parser.parse_args()
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    output=(args.output or ROOT/"qa-results"/run_id).resolve()
    output.mkdir(parents=True,exist_ok=False)
    source_digest=digest()
    report={"schema":1,"run_id":run_id,"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "source_dirty":bool(subprocess.check_output(["git","status","--porcelain"],cwd=ROOT,text=True).strip()),
        "source_sha256":source_digest,"started_utc":datetime.now(timezone.utc).isoformat(),"policy":POLICY,"steps":[],
        "human_gates":{"real_device_performance":"NOT MEASURED","child_usability":"NOT RUN","educational_transfer":"NOT ESTABLISHED","manual_accessibility":"NOT RUN"}}
    env=os.environ.copy()
    godot=env.get("GODOT","godot")
    command=shutil.which(godot) if not Path(godot).is_absolute() else godot
    if not command:
        report["steps"].append({"name":"engine-version","status":"FAIL","reason":"GODOT executable missing"})
    session=tempfile.TemporaryDirectory(prefix="kinderwelt-quality.",dir="/tmp")
    session_path=Path(session.name)
    env.update(XDG_DATA_HOME=str(session_path/"data"),XDG_CONFIG_HOME=str(session_path/"config"),XDG_CACHE_HOME=str(session_path/"cache"),KINDERWELT_QA_OUTPUT=str(output))
    for path in ["data","config","cache"]: (session_path/path).mkdir()

    def step(name,argv,timeout=180,check=None):
        item={"name":name,"command":list(map(str,argv)),"status":"FAIL"}
        logfile=output/(name+".log")
        item["log"]=logfile.name
        try:
            with logfile.open("w") as stream:
                proc=subprocess.run(list(map(str,argv)),cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout)
            item["exit_code"]=proc.returncode
            log=logfile.read_text(errors="replace")
            if proc.returncode!=0:
                item["reason"]="Command exited unsuccessfully"
            elif ERROR.search(log):
                item["reason"]="Godot/GUT error in output despite process status"
            else:
                if check: item.update(check(log))
                item["status"]="PASS"
        except subprocess.TimeoutExpired:
            item.update(exit_code=124,reason="Command timeout")
        except (OSError,ValueError,ET.ParseError,KeyError) as exc:
            item["reason"]=str(exc)
        report["steps"].append(item)
        print(name+": "+item["status"],flush=True)
        if item["status"]!="PASS": print("  See "+str(logfile),flush=True)
        return item["status"]=="PASS"

    def engine_check(log):
        actual=log.strip()
        if actual!=POLICY["engine_version"]: raise ValueError("Engine version differs from pinned build")
        return {"version":actual}

    def existing_check(log):
        outcomes=re.findall(r"^(RESULT|LEARNING RESULT|INPUT RESULT|SCENARIOS RESULT): (\d+) checks, (\d+) failures$",log,re.M)
        if len(outcomes)!=4 or any(int(n)==0 or int(f)!=0 for _,n,f in outcomes):
            raise ValueError("All four existing suites must execute nonzero checks and pass")
        adventure=re.findall(r"^ADVENTURE RESULT: (\d+) checks, (\d+) failures$",log,re.M)
        if len(adventure)!=1 or int(adventure[0][0])==0 or int(adventure[0][1])!=0:
            raise ValueError("Adventure suite must execute nonzero checks and pass")
        return {"adventure_checks":int(adventure[0][0]),"checks":sum(int(n) for _,n,_ in outcomes),"suites":[{"name":n,"checks":int(c),"failed":int(f)} for n,c,f in outcomes]}

    def python_check(log):
        match=re.search(r"Ran (\d+) tests?",log)
        if not match or int(match[1])==0: raise ValueError("No static checker regression tests ran")
        return {"tests":int(match[1])}

    try:
        static=audit(ROOT,POLICY)
        (output/"static.json").write_text(json.dumps(static,indent=2)+"\n")
        report["steps"].append({"name":"static-audit","status":static["status"],"report":"static.json","findings":len(static["findings"]),"files_examined":static["files_examined"]})
        step("static-checker-regression",[sys.executable,"-m","unittest","discover","-s","tests/qa","-p","test_static_audit.py","-v"],check=python_check)
        ready=command and static["status"]=="PASS" and step("engine-version",[command,"--version"],check=engine_check)
        if ready:
            installed=step("install-gut",["bash","scripts/install-gut.sh"])
            # A truly empty import cache and user-data root, without deleting the
            # developer's prepared .godot cache or real local saves.
            fresh=session_path/"fresh-project"
            fresh.mkdir()
            shutil.copy2(ROOT/"project.godot",fresh/"project.godot")
            for name in ["core","games","content","assets"]: (fresh/name).symlink_to(ROOT/name,target_is_directory=True)
            step("fresh-import",[command,"--headless","--path",fresh,"--editor","--import","--quit"])
            step("fresh-startup",[command,"--headless","--path",fresh,"--quit-after","60"])
            step("existing-suite",["bash","tests/run.sh"],timeout=600,check=existing_check)
            if installed:
                # Framework classes must be imported; the editor plugin remains off.
                imported=step("framework-import",[command,"--headless","--path",ROOT,"--editor","--import","--quit"])
                if imported:
                    base=[command,"--headless","--path",ROOT,"-s","addons/gut/gut_cmdln.gd","-gconfig=tests/qa/gut.json"]
                    upstream=",".join("res://.godot/qa-tools/gut/"+p for p in POLICY["upstream_tests"])
                    step("gut-upstream",base+["-gtest="+upstream,"-gjunit_xml_file="+str(output/"upstream.xml")],check=lambda _:validate_junit(output/"upstream.xml"))
                    step("gut-quality",base+["-gtest=res://tests/qa/test_quality.gd","-gjunit_xml_file="+str(output/"quality.xml")],timeout=300,check=lambda _:validate_junit(output/"quality.xml"))
                    step("gut-experience",base+["-gtest=res://tests/qa/test_experience.gd","-gjunit_xml_file="+str(output/"experience.xml")],timeout=300,check=lambda _:validate_junit(output/"experience.xml"))
                    try:
                        coverage=json.loads((output/"coverage.json").read_text())["cases"]
                        expected={(t["module"],t["task"],tuple(v)) for t in static["tasks"] for v in POLICY["viewports"]}
                        actual={(r["module"],r["task"],tuple(r["viewport"])) for r in coverage}
                        ok=actual==expected and len(coverage)==len(expected) and all(r["status"]=="PASS" for r in coverage)
                        report["steps"].append({"name":"coverage-completeness","status":"PASS" if ok else "FAIL","expected":len(expected),"executed":len(coverage),"authored_tasks":len(static["tasks"])})
                    except (OSError,ValueError,KeyError,TypeError):
                        report["steps"].append({"name":"coverage-completeness","status":"FAIL","reason":"Missing/malformed current-run coverage"})
        else:
            report["steps"].append({"name":"runtime-checks","status":"NOT RUN","reason":"Static review or pinned engine prerequisite failed"})
        if digest()!=source_digest:
            report["steps"].append({"name":"source-stability","status":"FAIL","reason":"Source changed during this run"})
    except (OSError,ValueError,KeyError,TypeError) as exc:
        report["steps"].append({"name":"qa-harness","status":"FAIL","reason":str(exc)})
    finally:
        session.cleanup()
        report["finished_utc"]=datetime.now(timezone.utc).isoformat()
        report["technical_status"]="PASS" if report["steps"] and all(s["status"]=="PASS" for s in report["steps"]) else "FAIL"
        report["human_trial_readiness"]="NOT APPROVED BY AUTOMATION; complete manual preflight and consent/safeguarding decisions first"
        (output/"report.json").write_text(json.dumps(report,indent=2)+"\n")
        print("Technical QA: "+report["technical_status"]+"; evidence: "+str(output),flush=True)
    return 0 if report["technical_status"]=="PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
