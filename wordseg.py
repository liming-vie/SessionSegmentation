#! /usr/bin/env python
import sys
sys.path.append('la')
sys.path.append('la/gen-py')
from la_client import LAClient

input_file=sys.argv[1]
output_file=sys.argv[2]
la_port=int(sys.argv[3])

with open(input_file) as fin, open(output_file, 'w') as fout:
	lines=[line.strip() for line in fin.readlines()]
	client=LAClient(la_port)
	lines=client.request_multiple(lines)
	fout.write('\n'.join(lines)+'\n')
