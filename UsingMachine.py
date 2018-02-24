#!/usr/bin/env python

import sys
import csv
from collections import defaultdict

if len(sys.argv) <2:
	print "py Total.csv"
	exit(1)

lis = []
dic_fc = defaultdict(lambda:[])
dic_lane = defaultdict(lambda:[])
dic_cln = defaultdict(lambda:[])
dic_SR = defaultdict(lambda:[])
dic_cln_SR = defaultdict(lambda:[])
with open(sys.argv[1],"rb") as f:
	a = csv.reader(f)
	for row in a:
		mach = row[0].split('_')[0]
		if mach not in lis and row[0] != '#Machine':
			lis.append(mach)
		dic_fc[mach].append(row[1])
		dic_lane[mach].append(row[2])
		if row[-1] == 'SR':
			dic_SR[mach].append(row[-1])
		elif row[-1] == 'CLN':
			dic_cln[mach].append(row[-1])
		else:
			dic_cln_SR[mach].append(row[-1])
		
print "#Machine_FC,FC_Num,Lane_Num,CLN_Lane_Num,SR_Lane_Num,Cln-Other_Lane_Num"
fc_total = 0
lane_total = 0
cln_total = 0
SR_total = 0
clnsr_total = 0
lis_sorted = sorted(lis)
for i in lis_sorted:
#	a = list(set(dic_fc[i]))
#	print a
	n_fc = len(set(dic_fc[i]))
	n_lane = len(dic_lane[i])
	n_cln = len(dic_cln[i])
	n_SR = len(dic_SR[i])
	n_cln_SR = len(dic_cln_SR[i])
	fc_total += n_fc
	lane_total += n_lane
	cln_total += n_cln
	SR_total += n_SR
	clnsr_total += n_cln_SR
	new = ','.join(map(str,[i,n_fc,n_lane,n_cln,n_SR,n_cln_SR]))
	print new
total1 = ','.join(map(str,['Total',fc_total,lane_total,cln_total,SR_total,clnsr_total]))
print total1
