#!/usr/bin/env python

import sys
import os

if len(sys.argv) < 2:
	print "py result.csv"
	exit(1)

w1 = open("CLN-result/Result-Cln.csv","w")
w2 = open("Other-result/Result-other.csv","w")

for i in open(sys.argv[1]):
	i = i.rstrip()
	if i.startswith('#'):
		w1.write(i+'\n')
		w2.write(i+'\n')
	else:
		j = i.split(',')
		if j[-1] == 'CLN':
			w1.write(i + '\n')
		else:
			w2.write(i + '\n')
w1.close()
w2.close()
	

