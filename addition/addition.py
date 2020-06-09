import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        x = int(self.get_argument("x", 0))
        y = int(self.get_argument("y", 0))
        result = x + y
        self.write(str(result))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()