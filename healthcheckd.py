import sys
import logging
import subprocess
from ConfigParser import SafeConfigParser
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


#This class will handles any incoming request from
#the browser
class HealthCheckHandler(BaseHTTPRequestHandler):

    def check_status(self):
        # supervisorctl status | awk '{ print $2 }' | sort | uniq | wc -l
        p = subprocess.Popen("/bin/true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retval = p.wait()

        return retval==0

    def do_healthcheck(self):
        if self.check_status():
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

    try:
        config = SafeConfigParser()
        config.read(configfile)

        try:
            pidfile = config.get('healthcheckd', 'pidfile').strip('"').strip("'").strip()
        except:
            pidfile = 'healthcheckd'

        try:
            port_number = config.get('healthcheckd', 'port').strip('"').strip("'").strip()
        except:
            port_number = 17

        with PidFile(pidfile) as pidfile:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            try:
                #Create a web server and define the handler to manage the
                #incoming request
                server = HTTPServer(('', port_number), HealthCheckHandler)
                print 'Started httpserver on port ' , PORT_NUMBER

                #Wait forever for incoming htto requests
                server.serve_forever()

            except KeyboardInterrupt:
                logging.info('shutting down healthcheckd')
                server.socket.close()
    except:
        msg = 'Error opening config file: '+configfile
        logging.error(msg)
        sys.exit(msg+'\n')
