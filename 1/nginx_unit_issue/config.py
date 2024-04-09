import getpass
import os
import pwd


env_user=os.getenv('USER')
env_home=os.getenv('HOME')

user=getpass.getuser()
euid = os.geteuid()

pwuid = pwd.getpwuid(euid)
homedir = os.path.expanduser(f"~{pwuid[0]}/")

print('Process environment:')
print(f' - {user=} ({euid=}) [env:USER={env_user}]')
print(f' - {homedir=} [env:HOME={env_home}]')