#!/usr/bin/env python
# coding: utf-8

import os
import yaml
import logging
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''<html>
<body>
    Notify your access. 
    <img src="/ring" style="display:none"/>
</body>
</html>
        ''')

class RingHandler(webapp.RequestHandler):
    def get(self):
        logging.debug("**** RING ****")
        target = self.request.headers['referer']
        notify( get_param('userhash'),
                'snaka72', u'はてなダイアリーアクセス通知', 
                ''.join([target, ' from ', self.request.remote_addr]) , target)
        self.response.out.write("")


def notify(user_hash, username, title, comment, url):
    apikey = get_param('apikey')
    prefix = username[0:2]

    body = {'title' : (u"%s" % title).encode('utf-8'),
            'text'  : (u"%s" % comment).encode('utf-8'),
            'icon'  : get_param('icon'),
            'link'  : (u"%s" % url).encode('utf-8')}
    encoded_body = urllib.urlencode(body)

    url = "http://api.notify.io/v1/notify/%s?api_key=%s" % (user_hash, apikey)
    logging.debug("notify url: %s" % url)
    res = urlfetch.fetch(url,
                         payload = encoded_body,
                         method = urlfetch.POST,
                         deadline = 10)

def get_param(name):
    f = open(os.path.join(os.path.dirname(__file__), "secret.yaml"))
    secret = yaml.load(f)
    f.close()
    return secret[name]


def main():
    application = webapp.WSGIApplication([('/',     MainHandler),
                                          ('/ring', RingHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

