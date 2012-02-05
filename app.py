from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import httplib
from xml.dom.minidom import parse


from tools import ResponseMixin


class MainPage(webapp.RequestHandler, ResponseMixin):
    
    
    def get(self):
        self.render('index.html')
        

class Etul(webapp.RequestHandler, ResponseMixin):
    
    
    def get(self):
        conn = httplib.HTTPConnection("rss.ohmynews.com")
        conn.request('GET', '/RSS/podcast_etul_main.xml')
        
        podcast = parse(conn.getresponse())
        for item in podcast.getElementsByTagName('item'):
            duration = item.getElementsByTagName('itunes:duration')[0].firstChild.nodeValue
            if duration < '00:10:00' :
                item.parentNode.removeChild(item)
        
        self.render_xml(podcast)


application = webapp.WSGIApplication([('/', MainPage), ('/etul.xml', Etul)])


if __name__ == "__main__":
    run_wsgi_app(application)
