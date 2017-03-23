#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class PostHandler(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('base.html')
        main = t.render()
        self.response.write(main)

    def post(self):
        theTitle = self.request.get('title')
        thePost = self.request.get('post')
        newPost = PostHandler(title = theTitle, post = thePost)
        postKey = newPost.put()
        self.redirect('/blog')

class AllPostHandler(MainHandler):
    def get(self):
        q = PostHandler.all()
        t = jinja_env.get_template('post_handle.html')
        main = t.render(post = q)
        self.response.write(main)

#class ViewPostHandler(id, AllPostHandler):
    #def get(self):


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', AllPostHandler),
    #webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
], debug=True)
