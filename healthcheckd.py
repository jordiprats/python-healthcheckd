import sys
import logging
import subprocess
from pid import PidFile
from configparser import ConfigParser
from http.server import BaseHTTPRequestHandler,HTTPServer


#This class will handles any incoming request from
#the browser
class HealthCheckHandler(BaseHTTPRequestHandler):

    def check_status(self):
        global command
        p = subprocess.Popen('bash -c \''+command+"'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()[0]
        print(p.returncode)
        return p.returncode==0

    def do_healthcheck(self):
        if self.check_status():
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("OK", "utf-8"))
        else:
            self.send_response(503)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("ERROR", "utf-8"))

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
        configfile = '/etc/healthcheckd.config'

    try:
        config = ConfigParser()
        config.read(configfile)

        try:
            pidfile = config.get('healthcheckd', 'pidfile').strip('"').strip("'").strip()
        except:
            pidfile = 'healthcheckd'

        try:
            piddir = config.get('healthcheckd', 'piddir').strip('"').strip("'").strip()
        except:
            piddir = '/tmp'

        try:
            port_number = int(config.get('healthcheckd', 'port').strip('"').strip("'").strip())
        except:
            port_number = 17

        try:
            command = config.get('healthcheckd', 'command').strip('"').strip("'").strip()
        except Exception as e:
            command = '/bin/true'
            print('INFO: setting default command: '+command)

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
