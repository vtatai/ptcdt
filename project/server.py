import thriftpy

# Server
pingpong_thrift = thriftpy.load("pingpong.thrift", module_name="pingpong_thrift")

from thriftpy.rpc import make_server

def ping(self):
    return "pong"

Delegate = type('Delegate', (), dict(ping=ping))

server = make_server(pingpong_thrift.PingPong, Delegate(), '127.0.0.1', 6000)
server.serve()
