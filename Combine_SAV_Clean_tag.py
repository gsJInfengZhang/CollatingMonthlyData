#!/usr/bin/env python

import sys

if len(sys.argv) < 4:
	print "py 171228_E00516_0250_AHFGLVCCXY-SAV.csv Summary_FlowCell_171228_E00516_0250_AHFGLVCCXY_Clean.csv 171228_E00516_0250_AHFGLVCCXY-SampleSheet-tag.csv"
	exit(1)

print "#Machine,Folder,Lane,stat,PF(%),PF_Bases,Q30_R1(%),Q30_R2(%),Q30_index(%),PF_reads,Clean_reads,Clean_Bases,CleanReadsPct(%),CleanDataPct(%),Dex_Ratio(%),SingelOrDual,CLN-or-SR"

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])
f3 = open(sys.argv[3])


SAV_dic = {}
Machine_dic = {}
LaneBases_dic = {}
Q30R1_dic = {}
Q30_R2_dic = {}
Raw_Reads_dic = {}
Raw_Bases_dic = {}
for i in f1:
	i = i.rstrip()
	if not i.startswith('#'):
		j = i.split(',')
		key = ','.join([j[0],j[2]])
		va = ','.join(j[3:])
		SAV_dic[key] = va
		Raw_Reads_dic[key] = float(j[-1])
		Raw_Bases_dic[key] = float(j[4])
		Machine_dic[key] = j[1]
		LaneBases_dic[key] = float(j[4])
		Q30R1_dic[key] = float(j[5])
		Q30_R2_dic[key] = float(j[6])
Clean_dic = {}
Dex_dic = {}
Clean_Reads_dic = {}
Clean_Bases_dic = {}
for i in f2:
	i = i.rstrip()
	if not i.startswith('#'):
		j = i.split(',')
		key = ','.join(j[0:2])
		j[3] = round(float(j[3])/1000000,2)
		j[5] = round(float(j[5])/1000,2)
		Clean_Reads_dic[key] = j[3]
		Clean_Bases_dic[key] = j[5]
		va = ','.join(map(str,[j[3],j[5],j[-1]]))
		Clean_dic[key] = va
		Dex_dic[key] = j[-1]
CLN_dic = {}
Dex_siordu = {}
for i in f3:
	i = i.rstrip()
	if not i.startswith('#'):
		j = i.split(',')
		key = ','.join(j[0:2])
		va = j[2]
		CLN_dic[key] = va
		Dex_siordu[key] = j[-1]
LaneBasesstat_dic = {}
Q30R1stat_dic = {}
Q30R2stat_dic = {}
dexstat_dic = {}
reads_pct = {}
bases_pct = {}
def sa(d,k):
	if k not in d:
		d[k] = '-'
	else:
		pass
	return d
for key in sorted(CLN_dic.keys()):
	if CLN_dic[key] == 'CLN':
		ma = key.split('_')[1]
		if ma.startswith('E00'):
			if LaneBases_dic[key] >= 120:
				LaneBasesstat_dic[key] = 'PASS'
			else:
				LaneBasesstat_dic[key] = 'LaneBases Failed'
			if Q30R1_dic[key] >= 90:
				Q30R1stat_dic[key] = 'PASS'
			else:
				Q30R1stat_dic[key] = 'Q30_R1 Failed'
			if Q30_R2_dic[key] >= 75:
				Q30R2stat_dic[key] = 'PASS'
			else:
				Q30R2stat_dic[key] = 'Q30_R2 Failed'						
			if Dex_dic[key] >= 90:
				dexstat_dic[key] = 'PASS'
			else:
				dexstat_dic[key] = 'Dex_Ratio Failed'
		elif ma.startswith('K00'):
			if LaneBases_dic[key] >= 110:
                                LaneBasesstat_dic[key] = 'PASS'
                        else:
                                LaneBasesstat_dic[key] = 'LaneBases Failed'
                        if Q30R1_dic[key] >= 92:
                                Q30R1stat_dic[key] = 'PASS'                                       
                        else:
                                Q30R1stat_dic[key] = 'Q30_R1 Failed'                                           
                        if Q30_R2_dic[key] >= 80:
                                Q30R2stat_dic[key] = 'PASS'                                               
                        else:
                                Q30R2stat_dic[key] = 'Q30_R2 Failed'
			if Dex_siordu[key] == 'singel_index':
                        	if Dex_dic[key] >= 95:
                                	dexstat_dic[key] = 'PASS'
                        	else:
                                	dexstat_dic[key] = 'Dex_Ratio Failed'
			else:
				if Dex_dic[key] >= 90:
                                        dexstat_dic[key] = 'PASS'
                                else:
                                        dexstat_dic[key] = 'Dex_Ratio Failed'
		stat = '|'.join([LaneBasesstat_dic[key],Q30R1stat_dic[key],Q30R2stat_dic[key],dexstat_dic[key]])
		if 'Failed' in stat:
			re = stat.replace('PASS','.')
		else:
			re = 'PASS'
		reads_pct[key] = round((Clean_Reads_dic[key]/Raw_Reads_dic[key]*100),2)
		bases_pct[key] = round((Clean_Bases_dic[key]/Raw_Bases_dic[key]*100),2)
		new = ','.join(map(str,[Machine_dic[key],key,re,SAV_dic[key],Clean_Reads_dic[key],Clean_Bases_dic[key],reads_pct[key],bases_pct[key],Dex_dic[key],Dex_siordu[key],CLN_dic[key]]))
		print new
	else:
		sa(Machine_dic,key)
		sa(SAV_dic,key)
		sa(Clean_dic,key)
		sa(Dex_dic,key)
		sa(Dex_siordu,key)
		sa(Clean_Reads_dic,key)
		sa(Clean_Bases_dic,key)
		sa(reads_pct,key)
		sa(bases_pct,key)
		re = '-'
		new = ','.join(map(str,[Machine_dic[key],key,re,SAV_dic[key],Clean_Reads_dic[key],Clean_Bases_dic[key],reads_pct[key],bases_pct[key],Dex_dic[key],Dex_siordu[key],CLN_dic[key]]))
		print new
	

