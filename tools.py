'''
Created on Feb 5, 2012

@author: vamf12
'''
import os
import mimetypes
from google.appengine.ext.webapp import template
from xml.dom.minidom import Document


template_location = os.path.join(os.path.dirname(__file__), 'templates')


class ResponseMixin(object):
    
    
    def render(self, template_name_or_xml_document, values=dict(), content_type=None):
        if isinstance(template_name_or_xml_document, Document):
            return self.render_xml(template_name_or_xml_document)
        
        else:
            template_name = template_name_or_xml_document
            if not content_type:
                content_type, _ = mimetypes.guess_type(template_name)
                if not content_type:
                    content_type = 'text/html'
                
            self.response.headers['Content-Type'] = content_type
            return self.response.out.write(template.render(os.path.join(template_location, template_name), values))
        
        
    def render_xml(self, document):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(document.toxml())