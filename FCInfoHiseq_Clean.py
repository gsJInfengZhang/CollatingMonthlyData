#!/usr/bin/env python

import sys
import os
import re
import time
import csv
import subprocess

path = os.getcwd()
fold = path.split('/')[-1].strip()

lanes_not = []
f = open("%s-SampleSheet-tag.csv"%fold,'rb')
for i in f:
	tag = i.split(',')[-1].strip()
	if tag != 'CLN':
		lanes_not.append(i.split(',')[1].strip())
f.close()

if len(lanes_not) == 8:
	print "NO Clin Data"
	exit(1)

l = '|'.join(lanes_not)
os.system('mkdir Clean')
os.system('mkdir TMP')



#step2: HQ_Data--->QC--->qsub

    #---------HQ_Data----->QC
R1_list = []
R2_list = []
for f in os.listdir('RawData/'):
    if f.endswith('R1_001.fastq.gz'):
        R1_list.append(f)
    elif f.endswith('R2_001.fastq.gz'):
        R2_list.append(f)
pattern = '(.*?)\d_001.fastq'

pattern1 = '(.*?).gz'
w1 = open('fcinfo_hq1.sh','w')    
for i in R1_list:
    for j in R2_list:
        if re.match(pattern,i).group(1) == re.match(pattern,j).group(1):
            w1.write('/bin/java -XX:+UseG1GC  -d64 -Djava.io.tmpdir=/GPFS01/JavaTemp -Xmx30g -jar /GPFS01/softwares/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads  8  RawData/%s RawData/%s Clean/%s TMP/%s_unpaired.gz Clean/%s TMP/%s_unpaired.gz ILLUMINACLIP:/mnt/lustre/databases/GSPipelineDB/TruSeq2-PE-ALL.fa:2:20:10:1:true LEADING:15 \
            TRAILING:15 SLIDINGWINDOW:5:20  AVGQUAL:20  MINLEN:36 && date >>date.log\n'%(i,j,i,re.match(pattern1,i).group(1),j,re.match(pattern1,j).group(1)))
            break
w1.close()

os.system("rm -r lsf_fcinfo_hq.sh")
if len(lanes_not) > 0 :
	os.system("egrep -v '%s' fcinfo_hq1.sh > fcinfo_hq.sh"%l)
else:
	os.system("mv fcinfo_hq1.sh fcinfo_hq.sh")
os.system('bsubjobs.py -c 5  -q low fcinfo_hq.sh')
os.system("rm fcinfo_hq1.sh")
#os.system('sh ./Auto_run_fcinfo_hq.sh >b')

    #---------monitoring
list1 = []

def monitor(lsf_fold):
	with open('%s/sucesslist.csv'%lsf_fold,'rb') as f:
    		a = csv.reader(f,delimiter = ',')
    		for row in a:
        		list1.append(row[0])

	list3 = [1]

	while len(list3) != 0:
    		a = subprocess.check_output("bjobs|cut -f 1 -d ' '",shell=True)
    		list2 = a.split('\n')
    		list3 = [x for x in list1 if x in list2]
    		print 'sleep 60s'
    		print list3
    		time.sleep(60)

monitor("lsf_fcinfo_hq.sh")
print 'QH_Data is OK'



    #---------QC-----qsub
w2 = open('fcinfo_cl.sh', 'w')
cmd1 = "python /GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/FC_Info_all1.py -f Clean"
w2.write(cmd1)
      #  w2.write(cmd2)

w2.close()
os.system('bsubjobs.py -c 17 -q low fcinfo_cl.sh')
#os.system('sh ./Auto_run_fcinfo_cl.sh >b')

    #---------monitoring
monitor("lsf_fcinfo_cl.sh")
print "Summary_Clean is ok!!"


