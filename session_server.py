#! /usr/bin/env python
# -*- coding:utf-8 -*-
import math
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('gen-py')
sys.path.append('la/')
sys.path.append('la/gen-py')

from session import SessionSegment
from session.ttypes import SessSegRequest, SessSegResponse
from la_client import LAClient

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class SessSegServer:
	def __init__(self, vector_file, vector_size, alpha, method, la_port):
		self.vecotr_size = vector_size
		self.alpha = alpha
		# load word2vec
		self.vectors={}
		with open(vector_file) as fin:
			for line in fin:
				ps=line[:-2].split(' ')
				self.vectors[ps[0]]=[float(i) for i in ps[1:]]
		# init la client
		self.la_client=LAClient(la_port)
		# determine which method to calculate similarity
		if method=='sum':
			self.similarity = self.sum_pooling
		elif method=='avg':
			self.similarity = self.heuristic_avg
		else:
			self.similarity = self.heuristic_max

	def sentence_vector(self, line):
		words=line[:-1].split(' ')
		return [(self.vectors[i] if i in self.vectors else [1e-5 for j in range(vector_size)]) for i in words]

	def cosine(self, v1, v2):
		s=sum(map(lambda(a,b):a*b, zip(v1,v2)))
		a=math.sqrt(sum([i**2 for i in v1]))
		b=math.sqrt(sum([i**2 for i in v2]))
		return s/(a*b)

	def sum_pooling(self, pre, cur):
		pre_sum=np.array(pre).cumsum(axis=0, dtype=None, out=None)[-1]
		cur_sum=np.array(cur).cumsum(axis=0, dtype=None, out=None)[-1]
		return self.cosine(pre_sum, cur_sum)

	def heuristic_max(self, pre, cur):
		s=0.0
		for i in range(len(pre)):
			s+=max([self.cosine(pre[i], cur[j]) for j in range(len(cur))])
		return s/len(pre)
 
	def heuristic_avg(self, pre, cur):
		s=0.0
		for i in range(len(pre)):
			s+=sum([self.cosine(pre[i], cur[j]) for j in range(len(cur))])
		return s/len(pre)/len(cur)

	def cut_off(self, text):
		'''
			calculate cut off probability
		'''
		# get sentenvce vector
		vector=[self.sentence_vector(t) for t in text]
		# calculate similarities
		sims=[self.similarity(vector[i-1], vector[i]) for i in range(1, len(vector))]
		peak=sims[0] # left peak in current session
		# get depth
		depth=[0 for i in range(len(sims))]
		for i in range(len(sims)):
			depth[i]=peak-sims[i]
			peak=peak if peak>sims[i] else sims[i]
		# calculate cut of prob
		avg=np.mean(depth)
		std=np.std(depth, axis=0)
	 	return avg+self.alpha*std

	def la_segment(self, texts):
		return self.la_client.request_multiple([t.encode('utf-8') for t in texts])
	
	def calculate(self, request):
		text=request.context
		text.extend([request.query])
		text=self.la_segment(text)
		score = self.cut_off(text)
		return SessSegResponse(score)

if __name__ == '__main__':
	alpha=float(sys.argv[2])
	port=int(sys.argv[1])
	method=sys.argv[3]
	vector_size=int(sys.argv[4])
	vector_file=sys.argv[5]
	la_port=int(sys.argv[6])
	# init
	print 'initializing server handler'
	handler=SessSegServer(vector_file, vector_size, alpha, method, la_port)
	# test
	req=SessSegRequest([
			'老公看着办哦',
			'老公陪着老婆',
			'爱你哦',
			'我也爱你'
			],
			'四重奏这部日剧评价很高'
			)
	score = handler.calculate(req)
	print score
	# run thrift server
	print 'starting server'
	processor = SessionSegment.Processor(handler)
	transport = TSocket.TServerSocket(port=port)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()
	server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
	server.serve()
