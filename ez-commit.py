#!/usr/bin/python3

# IGNORE ME
# just a script to help me
# commit my new work because
# remembering stuff is hard, amirite?

from os import system

commit = input("Enter commit msg: ")

system("git add ./*")
system("git commit -m \"%s\"" % commit)
system("git push -u origin master")
print("done :)")
exit(0)
