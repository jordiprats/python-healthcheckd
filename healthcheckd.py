import subprocess
from ConfigParser import SafeConfigParser
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 17

#This class will handles any incoming request from
#the browser
class HealthCheckHandler(BaseHTTPRequestHandler):

    def check_supervisord_status(self):
        # supervisorctl status | awk '{ print $2 }' | sort | uniq | wc -l
        p = subprocess.Popen("/bin/true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retval = p.wait()

        return retval==0


    def do_healthcheck(self):
        if self.check_supervisord_status():
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write("OK")
        else:
            self.send_response(503)
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write("ERROR")

    #Handler for the GET requests
    def do_GET(self):
        self.do_healthcheck()
        return

    #Handler for the HEAD requests
    def do_HEAD(self):
        self.do_healthcheck()
        return

if __name__ == "__main__":
    try:
        configfile = sys.argv[1]
    except IndexError:
        configfile = './healthcheckd.config'

    with PidFile('healthcheckd') as pidfile:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            #Create a web server and define the handler to manage the
            #incoming request
            server = HTTPServer(('', PORT_NUMBER), HealthCheckHandler)
            print 'Started httpserver on port ' , PORT_NUMBER

            #Wait forever for incoming htto requests
            server.serve_forever()

        except KeyboardInterrupt:
            print 'shutting down healthcheckd'
            server.socket.close()
