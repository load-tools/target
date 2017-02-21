import tornado.ioloop
import tornado.httpserver
import tornado.web
import argparse
import numpy as np


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class CpuHandler(tornado.web.RequestHandler):
    def get(self):
        x, y = np.ogrid[-2:1:500j, -1.5:1.5:500j]

        # Increase this to improve the shape of the fractal
        iterations = 4

        c = x + 1j*y

        z = reduce(lambda x, y: x**2 + c, [1] * iterations, c)
        self.write(",".join(str(num) for num in np.angle(z)))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/cpu", CpuHandler),
        (r"/disk", MainHandler),
    ])


def main():
    parser = argparse.ArgumentParser(description='Target stub.')
    parser.add_argument('--port', dest='port', type=int, default=8888, help='target port')
    parser.add_argument('--workers', dest='workers', type=int, default=1, help='number of workers')
    args = parser.parse_args()
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(args.port)

    server.start(args.workers)

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()