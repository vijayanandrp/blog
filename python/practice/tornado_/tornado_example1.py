#!/usr/bin/env python


import tornado.ioloop
import tornado.web
import os.path

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")


curr_dir = os.path.dirname(__file__)
# settings - to tell tornado where to find the html files
settings = dict(
	template_path =  os.path.join(curr_dir, "templates"),
	static_path = os.path.join(curr_dir, "static"),
	debug = True
)


def make_app():
	return tornado.web.Application([
		(r'/', MainHandler), 
	], **settings)


if __name__ == '__main__':
	print 'server started running at 8888'
	print 'Ctrl+C to quit'
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()


