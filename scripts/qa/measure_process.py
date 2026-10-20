#!/usr/bin/env python3
"""Record a child process's desktop RSS/CPU/wall time without interpreting it as Android."""
import argparse,json,resource,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metrics',type=Path,required=True);p.add_argument('--log',type=Path,required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
command=a.command[1:] if a.command and a.command[0]=='--' else a.command
start=time.monotonic()
with a.log.open('w') as stream:
    process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT)
    try:code=process.wait(timeout=120)
    except subprocess.TimeoutExpired:process.kill();process.wait();code=124
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
a.metrics.write_text(json.dumps({'scope':'Linux desktop subprocess resource usage; not Android memory or battery','elapsed_seconds':time.monotonic()-start,'max_rss_kib':usage.ru_maxrss,'user_cpu_seconds':usage.ru_utime,'system_cpu_seconds':usage.ru_stime,'exit_code':code},indent=2)+'\n')
raise SystemExit(code)
