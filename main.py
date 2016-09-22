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
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kw):
        self.response.write(*args, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class Homepage(Handler):
#    def render_posts(self, posts="")
#        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
#        self.render("posts.html", posts=posts)

#    def get(self):
#        self.render_posts()

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        self.render("posts.html", posts=posts)


class NewPost(Handler):
    def render_front(self, title="", post="", error=""):
        self.render("front.html", title=title, post=post, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title = title, post = post)
            a.put()

            self.redirect("/")

        else:
            error = "We need both a title and a post!"
            self.render_front(title, post, error)


class ViewPostHandler(Handler):
#    def get(self, post_id):
#        post = Post.get_by_id(int(post_id))

#    def render_view(self, title="", post=""):
#        post = Post.get_by_id(int(post_id))
#        self.render("viewpost.html", title=title, post=post)

#    def get(self):
#        self.render_view()

#    def get(self):
#        self.response.write("Hiya")

#        if there is a post with that id, render the single post form
#    else: produce this helpful error message: there is no post with that id

    # This works (below), just needs some formatting
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        wpost = str(post.title) + str(post.post)
        self.response.write(wpost)


#class SinglePost(Handler):

#        view = post.key().id()
        # some code to handle the request - get(key) for id. obj
        # but use ORM syntax rather than Gql syntax
#        post_id = post.key().id()

        # db Model Post:
#        post = Post.get_by_id(int(post_id))
#        view = post.key().id()
#        self.response.write(view, post)

#        self.response.write('%s' % int(post_id), str(post_id))

        # below code is psuedocode:
#        key = db.Key.from_path.('Model', int(id))
#        viewpost = db.get(key)
#        key = db.Key.from_path.('Post', int(post_id))
#        view = db.get(key)

#        self.response.write(key)
        #viewpost = db.GqlQuery("SELECT * FROM Post WHERE id= "# single id")
#        self.render("viewpost.html", viewpost=viewpost)



app = webapp2.WSGIApplication([
    ('/', Homepage),
    ('/new', NewPost),
    webapp2.Route('/view/<post_id:\d+>', ViewPostHandler)
], debug=True)

# implement below route instead of view once get_id code is working
#webapp2.Route('/<id:|d+>', ViewPostHandler)


#/Users/Ruthie/blog/main.py
