import sys
import logging
import subprocess
from pid import PidFile
from ConfigParser import SafeConfigParser
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


#This class will handles any incoming request from
#the browser
class HealthCheckHandler(BaseHTTPRequestHandler):

    def check_status(self):
        global command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.wait()==0

    def do_healthcheck(self):
        if self.check_status():
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("OK")
        else:
            self.send_response(503)
            self.send_header('Content-type','text/html')
            self.end_headers()
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
            piddir = config.get('healthcheckd', 'piddir').strip('"').strip("'").strip()
        except:
            piddir = 'healthcheckd'

        try:
            port_number = int(config.get('healthcheckd', 'port').strip('"').strip("'").strip())
        except:
            port_number = 17

        try:
            command = config.get('healthcheckd', 'command')
        except:
            command = '/bin/true'

        with PidFile(piddir=piddir, pidname=pidfile) as pidfile:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            try:
                #Create a web server and define the handler to manage the
                #incoming request
                server = HTTPServer(('', port_number), HealthCheckHandler)
                print('Started httpserver on port '+str(port_number))

                #Wait forever for incoming htto requests
                server.serve_forever()

            except KeyboardInterrupt:
                logging.info('shutting down healthcheckd')
                server.socket.close()
                sys.exit()
    except Exception as e:
        msg = 'Global ERROR: '+str(e)
        logging.error(msg)
        sys.exit(msg+'\n')
