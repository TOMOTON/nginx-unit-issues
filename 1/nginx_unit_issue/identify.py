import os
import pwd
import grp

class Identity():

    def __init__(self, user: str, group: str = None):
        self.uid = pwd.getpwnam(user).pw_uid
        if not group:
            self.gid = pwd.getpwnam(user).pw_gid
        else:
            self.gid = grp.getgrnam(group).gr_gid

    def __enter__(self):
        self.original_uid = os.getuid()
        self.original_gid = os.getgid()
        os.setegid(self.uid)
        os.seteuid(self.gid)

    def __exit__(self, type, value, traceback):
        os.seteuid(self.original_uid)
        os.setegid(self.original_gid)

if __name__ == '__main__':

    with Identity("hedy", "lamarr"):
        homedir = os.path.expanduser(f"~{pwd.getpwuid(os.geteuid())[0]}/")
        with open(os.path.join(homedir, "install.log"), "w") as file:
            file.write("Your home directory contents have been altered")