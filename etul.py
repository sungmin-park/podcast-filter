from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import mimetypes
from google.appengine.ext.webapp import template
import httplib
from xml.dom.minidom import parse


template_location = os.path.join(os.path.dirname(__file__), 'templates')


class Templated(webapp.RequestHandler):
    
    def get(self, template_name, values=dict(), content_type=None):
        if not content_type:
            content_type, _ = mimetypes.guess_type(template_name)
            if not content_type:
                content_type = 'text/html'
            
        self.response.headers['Content-Type'] = content_type
        self.response.out.write(template.render(os.path.join(template_location, template_name), values))
        

class MainPage(Templated):
    
    def get(self):
        Templated.get(self, 'index.html')
        

class Etul(Templated):
    
    def get(self):
        conn = httplib.HTTPConnection("rss.ohmynews.com")
        conn.request('GET', '/RSS/podcast_etul_main.xml')
        
        potcast = parse(conn.getresponse())
        for item in potcast.getElementsByTagName('item'):
            duration = item.getElementsByTagName('itunes:duration')[0].firstChild.nodeValue
            if duration < '00:10:00' :
                item.parentNode.removeChild(item)
                
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(potcast.toxml())


application = webapp.WSGIApplication([('/', MainPage), ('/etul.xml', Etul)])


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
