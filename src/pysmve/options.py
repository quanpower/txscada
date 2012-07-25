try:
	import argparse
except ImportError, e:
	from utils import argparse

parser = argparse.ArgumentParser(usage="Cada comando recibe argumentos spearados por comas")
parser.add_argument('-r', '--reload', action = "store_true", default = False,
					help = "Use Flask run script instead of Twisted reactor loop. "
					"Useful for testing only the web application reload")

parser.add_argument('-p', '--port', default=4000, type=int,
					help="Port to bind the webserver to.")
parser.add_argument('command', nargs=1, default='server')
parser.add_argument('-l', '--logfile', default='smve.log',
                    help="File for logging output")
parser.add_argument('-v', '--verbose', default=False, action='store_true',
                    help="Log to stdout")