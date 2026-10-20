#!/usr/bin/env python3
"""Record a child process's desktop RSS/CPU/wall time without interpreting it as Android."""
import argparse,json,resource,subprocess,time,threading
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metrics',type=Path,required=True);p.add_argument('--log',type=Path,required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
command=a.command[1:] if a.command and a.command[0]=='--' else a.command
start=time.monotonic()
ready=None
timed_out=threading.Event()
with a.log.open('w') as stream:
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    def stop_late():
        if process.poll() is None:
            timed_out.set();process.kill()
    timer=threading.Timer(120,stop_late);timer.daemon=True;timer.start()
    for line in process.stdout:
        if line.startswith('MODERN READY:') and ready is None:ready=time.monotonic()-start
        stream.write(line);stream.flush()
    process.wait();timer.cancel();code=124 if timed_out.is_set() else process.returncode
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
a.metrics.write_text(json.dumps({'scope':'Linux desktop subprocess resource usage; not Android memory or battery','elapsed_seconds':time.monotonic()-start,'startup_to_ready_wall_seconds':ready,'max_rss_kib':usage.ru_maxrss,'user_cpu_seconds':usage.ru_utime,'system_cpu_seconds':usage.ru_stime,'exit_code':code},indent=2)+'\n')
raise SystemExit(code)
