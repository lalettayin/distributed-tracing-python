import os
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat
from jaeger_client import Config
from opentracing import Format

def initialize_tracer(service_name):
    config = Config(config={
            "sampler": {
                "type": "const",
                "param": 1,
            },
            "local_agent": {
                "reporting_host": "jaeger",
                "reporting_port": "6831",
            },
            "logging": True,
        }, service_name=service_name, validate=True)
    return config.initialize_tracer(io_loop=tornado.ioloop.IOLoop.current())

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, tracer):
        self.tracer = tracer

    async def get(self):
        with self.tracer.start_span("multiply") as span:
            x = int(self.get_argument("x", 0))
            y = int(self.get_argument("y", 0))

            total =  0 if (x % 2) == 0 else y
            http = AsyncHTTPClient()

            headers = {}
            self.tracer.inject(span, Format.HTTP_HEADERS, headers)
            
            for _ in range(x // 2):
                payload = {"x": y, "y": y}
                url = url_concat(os.getenv("ADDITION_URL"), payload)
                response = await http.fetch(url, headers=headers)
                total += int(response.body)

            span.log_kv({"x": x, "y": y, "result": total})

            self.write(str(total))

def make_app():
    tracer = initialize_tracer("multiplication")
    return tornado.web.Application([
        (r"/", MainHandler, dict(tracer=tracer)),
    ])

def main():
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    print(os.getenv("ADDITION_URL"))
    main()