#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
class for using session segmentation service
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('gen-py')

from session import SessionSegment
from session.ttypes import SessSegRequest, SessSegResponse

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class Client: 
	def __init__ (self, port):
		self.transport = TSocket.TSocket('localhost', port)
		self.transport = TTransport.TBufferedTransport(self.transport)
		protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

		self.client = SessionSegment.Client(protocol)

	def request(self, context, query):
		req = SessSegRequest(context, query)
		self.transport.open()
		ret = self.client.calculate(req)
		self.transport.close()
		return ret.score

if __name__ == '__main__':
	port = int(sys.argv[1])
	client=Client(port)
	context = [
		'我要你在我身旁',
		'我要你为我梳妆'
	]
	query='这夜的风儿吹'
	print client.request(context, query)
