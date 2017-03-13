#!/bin/sh
if [ $# != 6 ] ; then
	echo -e "\033[31m sh train.sh word2vec_bin_dir train_file output_dir alpha method port\033[0m"
	exit 1
fi

###
# This script is used for training the mikolov_word2vec model, 
# and setup a thrift service for calculating the probability 
# of session segmentation.
###

# directory for word2vec executable file named "word2vec"
word2vec_bin_dir=$1
# training file for word2vec
# each line in the form:
#	query answer
#	use \t to split
train_file=$2 
# output directory for save training result
output_dir=$3
# alpha[float], for controlling the weight of variance in cut off calculation
# cut off prob = mean + alphs * variance
alpha=$4
# method for calculate similarity
# [max/avg/sum]
method=$5
# port for running session thrift server
port=$6

mkdir $output_dir

vector_size=200
skip_gram_window=50
word2vec_file=$output_dir/vectors
la_port=1028 # port for la segmentation service

echo -e "\033[31m begin word segmentation, result in $output_dir/train_seg\033[0m"
python wordseg.py $train_file $output_dir/train_seg $la_port

echo -e "\033[31m training word2vec\033[0m"
time $word2vec_bin_dir/word2vec -train $output_dir/train_seg -output $word2vec_file -cbow 0 -size $vector_size -window $skip_gram_window -negative 5 -hs 1 -sample 1e-4 -threads 12 -binary 0 -save-vocab $output_dir/vocab
sed -i '1d' $word2vec_file # remove first line : statistic info
echo -e "\033[31m vector file: $word2vec_file\033[0m"
echo -e "\033[31m vocab file: $output_dir/vocab\033[0m"

echo -e "\033[31m start session segmentation service in port $port, using alpha=$alpha, method=$method\033[0m"
echo -e "\033[31m use python session_client.py $port to call for segsession server\033[0m"
echo -e "\033[31m use sh kill.sh $port to kill the thrift server\033[0m"
nohup python session_server.py $port $alpha $method $vector_size $word2vec_file $la_port &
