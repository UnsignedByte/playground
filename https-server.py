# -*- coding: utf-8 -*-
# @Author: UnsignedByte
# @Date:   16:44:37, 17-Jul-2020
# @Last Modified by:   UnsignedByte
# @Last Modified time: 16:50:49, 17-Jul-2020

import http.server, ssl

server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,server_side=True,certfile='./localhost.pem',ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()