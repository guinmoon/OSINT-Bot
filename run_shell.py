import os
import subprocess
# stream = os.popen('cd ok_tools && node ./profile_by_phonenumber.js 79286362051 true')
# output = stream.read()
# print(output)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


email = 'samsalieva.elmira@gmail.com'
cmd = ['/usr/bin/python3','/home/m_vs_m/cerebro/addons/GHunt/hunt_json.py',email]
raw_info = execute(cmd)
print(raw_info)