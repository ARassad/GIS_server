from subprocess import Popen


def update():
    p = Popen(['bash', '/root/poas/rpis/update_tracks.sh'])
    p.wait()
    stdout, stderr = p.communicate()
    print(stdout)
    print(stderr)

