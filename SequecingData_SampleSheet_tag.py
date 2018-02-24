#!/usr/bin/env python

import sys
import csv
import os
from collections import defaultdict

if len(sys.argv) < 2:
	print "py sequencingdatafold"
	print "eg: py 171107_E00514_0240_AH532CCCXY"
	exit(1)

path = "/GPFS01/home/njsh/SequencingData"

fold = sys.argv[1]

print "#Fold,Lane,stat,DualOrSingle"
Lane_lis = list('12345678')
tag_list = ["WES","WGS","WGBS","RNA","YH158","KY200","KY201","KY203","PBMC"]
Lane_Sample = defaultdict(lambda:[])
index_dic = defaultdict(lambda:[])
def SampleCount(fold,csvfile):
	with open('%s/%s/%s'%(path,fold,csvfile),'rb') as f:
		a = csv.reader(f)
		for row in a:
			if row[0] == 'Lane':
				break
		for row in a:
			lane = 'L00' + row[0]
			sample = row[2]
			sr = row[-2]
			lis1 = []
			for tag in tag_list:
				if tag in sample:
					Lane_Sample[lane].append(tag)
					lis1.append(sample)
				else:
					pass
#					Lane_Sample[lane].append('')
			if sr == '':
				if sample not in lis1:
					Lane_Sample[lane].append('CLN')
				else:
					pass
			else:
				Lane_Sample[lane].append('SR')
			if len(row) >9:
				index1 = row[6]
				index2 = row[8]
				index_dic[lane].append(index2)				
			else:
				index_dic[lane] = ''
	f.close()
	w = open('%s/%s/%s-SampleSheet-tag.csv'%(path,fold,fold),'w')
	result = {}
	index_result = {}
	for i in Lane_lis:
		key = 'L00' + i
		aa = set(Lane_Sample[key])
		bb = list(aa)
		index = set(index_dic[key])
		cc = list(index)
		if len(cc) == 0:
			index_result[key] = 'singel_index'
		elif len(cc) == 1 and 'NNNNNN' in cc[0]:
			index_result[key] = 'singel_index'
		else:
			index_result[key] = 'dual_index'
#		cc = bb.index('')
#		bb[cc] = 'CLN'
		result[key] = '-'.join(bb)
		new = ','.join((map(str,[fold,key,result[key],index_result[key]])))
		w.write(new+'\n')
		print new
	w.close()
			
if os.path.exists("%s/%s/SampleSheet.csv.original.ori"%(path,fold)):
	SampleCount(fold,'SampleSheet.csv.original.ori')
elif os.path.exists("%s/%s/SampleSheet.csv.original"%(path,fold)):
	SampleCount(fold,'SampleSheet.csv.original')
else:
	SampleCount(fold,'SampleSheet.csv')
