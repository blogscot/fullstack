from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

html_start = "<!DOCTYPE html><html><head><title>Restaurants</title></head><body>"
html_end = "</body></html>"
html_header = "<h1>Welcome!</h1>"
html_new_restaurant_form = "<form method='POST' enctype='multipart/form-data' action='/new'><h2>Add New Restaurant</h2>Name:&nbsp;<input name='restaurant' type='text' /><input type='submit' value='Add' /></form>"

html_edit_restaurant_form = "<form method='POST' enctype='multipart/form-data' action='/%s/edit'><h2>Update Restaurant</h2>Name:&nbsp;<input name='restaurant' value='%s' type='text' /><input type='submit' value='Update' /></form>"

class webserverHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    try:

      # ROOT
      if self.path == '/':
        print "home"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # add a list of restaurants
        items = session.query(Restaurant).all()

        output = html_start
        output += html_header

        output += "<ul>"

        for item in items:
          output += "<li> %s" % item.name
          output += "&nbsp;<a href=' /%s/edit'>Edit</a>" % item.id
          output += "&nbsp;<a href=' /%s/delete'>Delete</a>" % item.id
        output += "</li></ul>"
        
        output += "<br><a href='/new'>Add New Restaurant</a>"
        output += html_end
        
        self.wfile.write(output)

      # NEW
      elif self.path.endswith('/new'):
        print "adding"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = html_start
        output += html_new_restaurant_form
        output += html_end
 
        self.wfile.write(output)                

      # EDIT
      elif self.path.endswith('/edit'):
        print "editing"

        restaurantId = self.path.split('/')[1]
        item = session.query(Restaurant).filter_by(id=restaurantId).one()

        if item != []:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()

          output = html_start
          output += html_edit_restaurant_form % (restaurantId, item.name)
          output += html_end
 
          self.wfile.write(output)            

      # DELETE
      elif self.path.endswith('/delete'):
        print "delete!"

        restaurantId = self.path.split('/')[1]
        item = session.query(Restaurant).filter_by(id=restaurantId).one()

        if item != []:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()

          temp1 = "<h1>Are You Sure You Want To Delete %s?</h1>"
          temp2 = "<form method='POST' action='/%s/delete'><input type='submit' value='Delete'/></form>"

          output = html_start
          output += temp1 % item.name
          output += temp2 % restaurantId
          output += html_end

          self.wfile.write(output)
      
      else:
        print "Unresolved Url!"
        print self.path()            

    except:
      self.send_error(404, 'File Not Found %s' % self.path)


  def do_POST(self):
    try:
      print "POST"

      # NEW
      if self.path.endswith('/new'):
        print ("adding new restaurant")
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'multipart/form-data':
          fields=cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('restaurant')
          print messagecontent[0]

          restaurant = Restaurant(name=messagecontent[0]) 
          session.add(restaurant)
          session.commit()

        # Redirects back to start page
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/')
        self.end_headers()

      # EDIT
      if self.path.endswith('/edit'):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'multipart/form-data':
          fields=cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('restaurant')

          restaurantId = self.path.split('/')[1]

          item = session.query(Restaurant).filter_by(id=restaurantId).one()

          if item != []:
            item.name = messagecontent[0]
            session.add(item)
            session.commit()

        # Redirects back to start page
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/')
        self.end_headers()

      # DELETE
      elif self.path.endswith('/delete'):
        print "deleting"

        restaurantId = self.path.split('/')[1]

        item = session.query(Restaurant).filter_by(id=restaurantId).one()

        if item != []:
          session.delete(item)
          session.commit()

        # Redirects back to start page
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/')
        self.end_headers()

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