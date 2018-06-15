import requests
def main(argv=None):
	exec(requests.get(argv[1]).content)
if __name__ == "__main__":
