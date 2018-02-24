#!/usr/bin/env python

import sys
import os 
import csv
from collections import defaultdict

if len(sys.argv) < 2:
	print "py SAV.info"
	print "py 171230_E00517_0250_BHFGV2CCXY.info"
	exit(1)
info = sys.argv[1]
filename = sys.argv[1].split('.')[0]
name = info.split('_')[1]
fc = info.split('.')[0].split('_')[3]
##obtain FC
fc1 = ''
if fc.startswith('A'):
        fc1 = 'FCA'
elif fc.startswith('B'):
        fc1 = 'FCB'
##obtain Machine
dic = {'E00516':'X1','E00515':'X2','E00514':'X3','E00517':'X4',"E00499":'X5',"E00572":'YZ1',"E00591":'YZ2',"K00141":'4000',"A00248":"NV","A00254":"NV","A00290":"NV","A00292":"NV","C70114":"Miseq","C70117":"Miseq","C70115":"Miseq","C70116":"Miseq","M02274":"Miseq","M03014":"Miseq","M05093":"Miseq"}
if name in dic:
        if dic[name] == 'Miseq':
                machine = 'Miseq'
        else:
                machine = dic[name] + '_' + fc1
else:
        machine = '-'
##Extract info from SAV file
read_dic = defaultdict(lambda:[])
read_list = []
with open(info,"rb") as f:
        a = csv.reader(f,delimiter = '\t')
        key = 'aaaa'
        for row in a:
                if len(row) > 1 and 'Read' in row[0] and row[1] == '':
                        if row[0] not in read_list:
                                read_list.append(row[0])
                        key = row[0]
                if key != 'aaaa':
                        read_dic[key].append(row)
f.close()
r1_lis = []
r2_lis = []
index_lis = []
for i in read_dic[read_list[0]]:
        if len(i) > 2 and 'Lane' not in i[0] and 'Read' not in i[0] and i[0] != '':
                r1_lis.append(i)
for i in read_dic[read_list[-1]]:
        if len(i) > 2 and 'Lane' not in i[0] and 'Read' not in i[0] and i[0] != '':
                r2_lis.append(i)
if len(read_list) == 3:
        for i in read_dic[read_list[1]]:
                if len(i) > 2 and 'Lane' not in i[0] and 'Read' not in i[0] and i[1] != '':
                        if len(i) == 16:
                                index_lis.append(float(i[7]))
                        elif len(i) == 18:
                                index_lis.append(float(i[9]))
else:
        tmp1 = []
        tmp2 = []
        for i in read_dic[read_list[1]]:
                if len(i) > 2 and 'Lane' not in i[0] and 'Read' not in i[0] and i[0] != '':
                        if len(i) == 16:
                                tmp1.append(float(i[7]))
                        elif len(i) == 18:
                                tmp1.append(float(i[9]))
        for i in read_dic[read_list[2]]:
                if len(i) > 2 and 'Lane' not in i[0] and 'Read' not in i[0] and i[0] != '':
                        if len(i) == 16:
                                tmp2.append(float(i[7]))
                        elif len(i) == 18:
                                tmp2.append(float(i[9]))
        for i in range(len(tmp1)):
                index_lis.append(format((tmp1[i] + tmp2[i])/2,'0.2f'))
if len(r1_lis) != len(r2_lis):
        print "%s is fail" % filename

##Combine Info
print "#Folder,Machine,Lane,PF,PF_Bases,Q30_R1,Q30_R2,Q30_index,PF_reads"
for i in range(len(r1_lis)):
        if len(r1_lis[0]) == 16:
                pf_bases1 = float(r1_lis[i][8])
                pf_bases  = round(float(pf_bases1) *2,2)
        elif len(r1_lis[0]) == 18:
                pf_bases1 = float(r1_lis[i][10])
                pf_bases  = round(float(pf_bases1) *2,2)
Num_dic = {}
for i in range(len(r1_lis)):
        lane = 'L00' + r1_lis[i][0]
        Num_dic['PF'] = float(r1_lis[i][3].split()[0])
        if len(r1_lis[0]) == 16:
                Num_dic['Q30_R1'] = r1_lis[i][7]
                Num_dic['Q30_R2'] = r2_lis[i][7]
                Num_dic['PF_bases1'] = float(r1_lis[i][8])
                Num_dic['PF_reads1'] = float(r1_lis[i][6])
                Num_dic['PF_bases']  = round(float(r1_lis[i][8]) *2,2)
        elif len(r1_lis[0]) == 18:
                Num_dic['Q30_R1'] = r1_lis[i][9]
                Num_dic['Q30_R2'] = r2_lis[i][9]
                Num_dic['PF_bases1'] = float(r1_lis[i][10])
                Num_dic['PF_reads1'] = float(r1_lis[i][8])
                Num_dic['PF_bases']  = round(float(r1_lis[i][10]) *2,2)
        Num_dic['Q30_index'] = float(index_lis[i])
	new = ','.join(map(str,[filename,machine,lane,Num_dic['PF'],Num_dic['PF_bases'],Num_dic['Q30_R1'],Num_dic['Q30_R2'],Num_dic['Q30_index'],Num_dic['PF_reads1']]))
	print new

