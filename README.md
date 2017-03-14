# Session Segmentation
 
This repo is an implementation of [Dialogue Session Segmentation by Embedding-Enhanced TextTiling](https://arxiv.org/abs/1610.03955), containing a trainning script and thrift service setup process.

## Prerequisite

* Python 2.7
* Mikolov Word2Vec
* Word Segmentation Tool. Replace the la service call.
* Thrift. Used to setup the Session Segmentation Service in session_server.py. Use session_client.py to call the service.
