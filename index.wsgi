#!/home/i/ivova/.local/bin/python3
this_file = "/home/i/ivova/packages/bin/activate_this.py"
execfile(this_file, dict(__file__=this_file))

import sys
sys.path.insert(0, "/home/i/ivova/trav_api/public_html/")

sys.stderr = open("/home/i/ivova/trav_api/public_html/log.txt", "a")

## WITHOUT DEBUG:
#from index import app as application
## END: WITHOUT DEBUG

## WITH DEBUG:
from index import app

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, True)
## END: WITH DEBUG

#from flup.server.fcgi import WSGIServer
#WSGIServer(app).run()
