
from subprocess import Popen

def update():
    p = Popen("UpdateTrack.bat", cwd=r"C:\Users\Arkadi\Desktop\CURS3.2\RPIS\GIS\GIS_server\src")
    stdout, stderr = p.communicate()
    print(stdout)
    print(stderr)

