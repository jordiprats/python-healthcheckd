from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import subprocess

PORT_NUMBER = 17

#This class will handles any incoming request from
#the browser
class HealthCheckHandler(BaseHTTPRequestHandler):

    def check_supervisord_status(self):
        # supervisorctl status | awk '{ print $2 }' | sort | uniq | wc -l
        p = subprocess.Popen("/bin/true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        linecount=0
        lastline=""
        for line in p.stdout.readlines():
            lastline = line.strip()
            linecount+=1
        retval = p.wait()

        return (retval==0 and linecount==1 and lastline=="OK")


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

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), HealthCheckHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print 'shutting down the web server'
    server.socket.close()
