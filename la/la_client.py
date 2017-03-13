# -*- coding:utf-8 -*-
import sys
sys.path.append('gen-py/')

from la.LAService import Client
from la.ttypes import LARequest, LAResponse, Token

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class LAClient:
	'''
		client for call la segmentation service
	'''
	def __init__(self, port):
		self.transport = TSocket.TSocket('localhost', port)
		self.transport = TTransport.TBufferedTransport(self.transport)
		protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

		self.client = Client(protocol)

	def request_multiple(self, queries):
		ret = []
		self.transport.open()
		for q in queries:
			req=LARequest(q.strip())
			res = self.client.process(req)
			ret.append(' '.join([i.term for i in res.tokens]))
		self.transport.close()
		return ret 

	def request(self, query):
		self.transport.open()
		req=LARequest(query.strip())
		res = self.client.process(req)
		ret = ' '.join([i.term for i in res.tokens])
		self.transport.close()
		return ret

# test
if __name__ == '__main__':
	la_port=1028
	client=LAClient(la_port)
	while True:
		q=raw_input()
		print client.request(q)
