#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Title: Illumina Sequence Folder Sync Monitor  
#Author: Mao Yibo
#Email: yibo.mao@geneseeq.com
#version: 0.2
from __future__ import print_function
import os
import sys
import time
import re
import glob
import argparse
import subprocess
from collections import defaultdict
import multiprocessing
import pandas as pd
import numpy as np

#max_cluster=621211104

fastq_info_bin="/GPFS01/softwares/scripts/dealfastq/fastq_info"

def fastq_info(fastq_path):
    sys.stdout.write("Cal {}\n".format(fastq_path))
    fastq_folder, filename=os.path.split(os.path.abspath(fastq_path))
    try:
        os.makedirs("{}/Infos".format(fastq_folder))
    except:
        pass
    p=subprocess.Popen("{} {}".format(fastq_info_bin, fastq_path), shell=True, stdout=subprocess.PIPE)
    p.wait()
    df=pd.read_csv(p.stdout,header=0,index_col=None)
    return filename, df

def lane_info(fastq_folder,max_cluster, thread=32):
    max_cluster=float(max_cluster)
    fastq_folder=os.path.abspath(fastq_folder)
    runid=[x for x in fastq_folder.split("/") if x.count("_") >=3][0]
    print(runid, fastq_folder)
    result_list=[]
    fastqfile=sorted(glob.glob("{}/*.fastq.gz".format(fastq_folder)), key=lambda x: os.path.getsize(x), reverse=True)
    #print(fastqfile)
    pool=multiprocessing.Pool(int(thread))
    for n in fastqfile:
        print(n)
        result_list.append(pool.apply_async(fastq_info, (n,)))
    pool.close()
    pool.join()
    #info_dict[lane].iloc[r1/r2/ur1/ur2,:]
    info_dict=defaultdict(lambda:pd.DataFrame(np.zeros((4,10)),columns="READS,LENGTH,BASES,A,C,G,T,N,Q20,Q30".split(",")))
    lane_length=defaultdict(lambda:[0,0])
    for n in result_list:
        #SAMPLE,READS,LENGTH,BASES,A,C,G,T,N,Q20,Q30\n
        fname, fdf=n.get()
        lane=fname.split("_")[2]
        if fname.split("_")[3]=="R1" :
            pe=0 
            lane_length[lane][0]=max(lane_length[lane][0], fdf.iloc[0,2])
        else: 
            pe=1
            lane_length[lane][1]=max(lane_length[lane][1], fdf.iloc[0,2])
        if fname.startswith("Undetermined"):
            info_dict[lane].iloc[pe+2]+=fdf.iloc[0, 1:]
        else:
            info_dict[lane].iloc[pe]+=fdf.iloc[0, 1:]
    
    lanes=info_dict.keys()
    lanes.sort()
    with open("Summary_FlowCell_{}_Clean.csv".format(runid), 'w') as total_out:
        total_out.write("#KIT,LANE,PF(%),Clean_READS,LENGTH,Clean_BASES,GC(%),Q20(%),Q30(%),N(ppm),DEX_READS,DEX_RATIO(%)\n")
        read1_out=open("Summary_FlowCell_{}_R1_Clean.csv".format(runid), 'w')
        read1_out.write("#KIT,LANE,PF(%),Clean_READS,LENGTH,Clean_BASES,GC(%),Q20(%),Q30(%),N(ppm),DEX_READS,DEX_RATIO(%)\n")
        read2_out=open("Summary_FlowCell_{}_R2_Clean.csv".format(runid), 'w')
        read2_out.write("#KIT,LANE,PF(%),Clean_READS,LENGTH,Clean_BASES,GC(%),Q20(%),Q30(%),N(ppm),DEX_READS,DEX_RATIO(%)\n")
        ##SAMPLE,READS,LENGTH,BASES,A,C,G,T,N,Q20,Q30\n
        total_read=0
        total_dex_read=0
        r1_total_len=0
        r2_total_len=0
        r1_total_bases=0
        r2_total_bases=0
        r1_total_gc=0
        r2_total_gc=0
        r1_total_q20=0
        r2_total_q20=0
        r1_total_q30=0
        r2_total_q30=0
        r1_total_n=0
        r2_total_n=0
        for lane in lanes:
            ldf=info_dict[lane]
            r1len,r2len=lane_length[lane]
            r1_total_len=max(r1_total_len, r1len)
            r2_total_len=max(r2_total_len, r2len)
            r1df=ldf.iloc[[0,2],:].sum()
            #reads are the same in r1 and r2
            reads=r1df["READS"]
            reads_dex=ldf.loc[0, "READS"]
            total_read+=reads
            total_dex_read+=reads_dex
            r1_bases=r1df["BASES"]
            r1_total_bases+=r1_bases
            r1_gc=r1df["G"]+r1df["C"]
            r1_total_gc+=r1_gc
            r1_n=r1df["N"]
            r1_total_n+=r1_n
            r1_q20=r1df["Q20"]
            r1_total_q20+=r1_q20
            r1_q30=r1df["Q30"]
            r1_total_q30+=r1_q30
            r2df=ldf.iloc[[1,3],:].sum()
            r2_bases=r2df["BASES"]
            r2_total_bases+=r2_bases
            r2_gc=r2df["G"]+r2df["C"]
            r2_total_gc+=r2_gc
            r2_n=r2df["N"]
            r2_total_n+=r2_n
            r2_q20=r2df["Q20"]
            r2_total_q20+=r2_q20
            r2_q30=r2df["Q30"]
            r2_total_q30+=r2_q30
            reads_dex_pct=100.*reads_dex/reads
            lane_total_bases=r1_bases+r2_bases
            #KIT,LANE,PF(%),Clean_READS,LENGTH,Clean_BASES,GC(%),Q20(%),Q30(%),N(ppm),DEX_READS,DEX_RATIO(%)
            total_info=[runid, lane, max(100.*reads/max_cluster, 0), reads, max(r1len,r2len), lane_total_bases/10.**6, 100.*(r1_gc+r2_gc)/lane_total_bases, 
                            100.*(r1_q20+r2_q20)/lane_total_bases, 100.*(r1_q30+r2_q30)/lane_total_bases, (r1_n+r2_n)*10.**6/lane_total_bases, reads_dex, reads_dex_pct]
            total_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*total_info))
            read1_info=[runid, lane,max(100.*reads/max_cluster, 0), reads, r1len, r1_bases/10.**6, 100.*r1_gc/r1_bases, 
                            100.*r1_q20/r1_bases, 100.*r1_q30/r1_bases, r1_n*10.**6/r1_bases, reads_dex, reads_dex_pct]
            read1_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*read1_info))
            read2_info=[runid, lane,max(100.*reads/max_cluster, 0), reads, r2len, r2_bases/10.**6, 100.*r2_gc/r2_bases, 
                            100.*r2_q20/r2_bases, 100.*r2_q30/r2_bases, r2_n*10.**6/r2_bases, reads_dex, reads_dex_pct]
            read2_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*read2_info))
        fc_total_base=r1_total_bases+r2_total_bases
        total_info=[runid,"TOTAL",max(100*total_read/8/max_cluster,0), total_read, max(r1_total_len, r2_total_len), fc_total_base/10.**6, 
                    100.*(r1_total_gc+r2_total_gc)/fc_total_base, 100.*(r1_total_q20+r2_total_q20)/fc_total_base, 100.*(r1_total_q30+r2_total_q30)/fc_total_base,
                    (r1_total_n+r2_total_n)*10.**6/fc_total_base,total_dex_read, 100.*total_dex_read/total_read ]
        total_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*total_info))
        read1_info=[runid,"TOTAL",max(100*total_read/8/max_cluster,0), total_read, r1_total_len, r1_total_bases/10.**6, 
                    100.*r1_total_gc/r1_total_bases, 100.*r1_total_q20/r1_total_bases, 100.*r1_total_q30/r1_total_bases,
                    r1_total_n*10.**6/r1_total_bases,total_dex_read, 100.*total_dex_read/total_read ]
        read1_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*read1_info))
        read2_info=[runid,"TOTAL",max(100*total_read/8/max_cluster, 0), total_read, r2_total_len, r2_total_bases/10.**6, 
                    100.*r2_total_gc/r2_total_bases, 100.*r2_total_q20/r2_total_bases, 100.*r2_total_q30/r2_total_bases,
                    r2_total_n*10.**6/r2_total_bases,total_dex_read, 100.*total_dex_read/total_read ]
        read2_out.write("{},{},{:0>.2f},{},{},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{:0>.2f},{},{:0>.2f}\n".format(*read2_info))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--thread",type=int, help="Thread of Program.", default=32)
    parser.add_argument("-f","--folder",type=str, help="Fastq Folder. Default: './RawData'", default='./RawData')
    args=parser.parse_args()
    folder=os.path.realpath(args.folder)
    if len(glob.glob("{}/*.fastq.gz".format(folder)))==0:
	print("Folder {} does not contain fastq files.".format(folder))
        sys.exit()
    for n in folder.split("/"):
        if n.count("_")>=3:
            runid=n
    machine=runid.split("_")[1]
    if machine[0]=='E':
        max_cluster=621211104
    elif machine[0]=='K':
        max_cluster=482988240
    elif machine[0]=='M' or machine[0]=='C':
        if os.path.exists('GenerateFASTQRunStatistics.xml'):
            infostr=open('GenerateFASTQRunStatistics.xml').read()
            max_cluster=re.findall(r"<NumberOfClustersRaw>(\d+)</NumberOfClustersRaw>", infostr)[0]
        else:
            max_cluster=-1
    elif machine[0]=='N':
        if len(glob.glob("Data/Intensities/BaseCalls/Reports/html/*/all/all/all/lane.html"))!=0:
            infostr=open(glob.glob("Data/Intensities/BaseCalls/Reports/html/*/all/all/all/lane.html")[0]).read()
            max_cluster=re.findall(r"<td>.+</td>",infostr)[1].replace(",","")
        else:
            max_cluster=-1
    print(folder, max_cluster)
    lane_info(folder, max_cluster, args.thread)




                        
                        
                        
                        
                        
    
    
    
    
    
    
    
