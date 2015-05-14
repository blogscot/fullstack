from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

html_start = "<!DOCTYPE html><html><head><title>Hey!</title></head><body>"
html_end = "</body></html>"

html_form = "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' /><input type='submit' value='Submit' /></form>"

greeting_eng = "Hello!"
greeting_esp = "&#161Hola!<p><a href='/hello'>Back</a></p>"


class webserverHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    try:
      if self.path.endswith('/hello'):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = html_start
        output += greeting_eng
        output += html_form
        output += html_end
        
        self.wfile.write(output)

      if self.path.endswith('/hola'):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = html_start
        output += greeting_esp
        output += html_form
        output += html_end

        self.wfile.write(output)

    except:
      self.send_error(404, 'File Not Found %s' % self.path)

  def do_POST(self):
    try:
      self.send_response(301)
      self.end_headers()

      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
        fields=cgi.parse_multipart(self.rfile, pdict)
        messagecontent = fields.get('message')

        output = html_start

        output += "<p>Okay, how about this: </p>"
        output += "<p> %s </p>" % messagecontent[0]
        output += html_form

        output += html_end
        self.wfile.write(output)
        # print output

    except:
      pass


def main():
  try:
    port = 8080
    server = HTTPServer(('', port), webserverHandler)
    print "Web server listening on port %s" % port
    print "Press ^C to terminate"
    server.serve_forever()

  except KeyboardInterrupt:
    print "^C entered, stopping server..."
    server.socket.close()


if __name__ == '__main__':
  main()