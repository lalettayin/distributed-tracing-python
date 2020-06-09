import os
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        x = int(self.get_argument("x", 0))
        y = int(self.get_argument("y", 0))

        total =  0 if (x % 2) == 0 else y
        http = AsyncHTTPClient()
        for _ in range(x // 2):
            payload = {"x": y, "y": y}
            url = url_concat(os.getenv("ADDITION_URL"), payload)
            response = await http.fetch(url)
            total += int(response.body)

        self.write(str(total))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    print(os.getenv("ADDITION_URL"))
    main()