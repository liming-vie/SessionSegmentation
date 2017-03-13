#!/bin/bash
if [ $# != 1 ] ; then 
	echo -e "\033[31m sh example word2vec_bin_dir\033[m"
	exit 1
fi

# using the executable file of mikolov_word2vec
word2vec_bin_dir=$1
# the test data is deleted here
sh train.sh $word2vec_bin_dir ./test/weibo_chat ./test/ 0.8 max 1129
