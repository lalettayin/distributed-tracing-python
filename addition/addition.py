import tornado.ioloop
import tornado.web
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
        span_ctx = self.tracer.extract(Format.HTTP_HEADERS, self.request.headers)
        with self.tracer.start_span("add", child_of=span_ctx) as span:
            x = int(self.get_argument("x", 0))
            y = int(self.get_argument("y", 0))

            result = x + y

            span.log_kv({"x": x, "y": y, "result": result})

            self.write(str(result))

def make_app():
    tracer = initialize_tracer("addition")
    return tornado.web.Application([
        (r"/", MainHandler, dict(tracer=tracer)),
    ])

def main():
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()