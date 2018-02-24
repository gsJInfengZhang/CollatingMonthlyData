
## 流程
1.每批下机目录打标签，标注存临床lane，目前会排除（SR、WES、WGS、WGBS、RNA、YH158、KY200、KY201、KY203)
```python
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/SequecingData_SampleSheet_tag.py 171107_E00514_0240_AH532CCCXY
```
- 说明
1.1 输入文件为下机目录，代码中默认读SampleSheet.csv.original.ori或SampleSheet.csv.original或SampleSheet.csv
1.2 输出文件为3列，输出文件名称为171107_E00514_0240_AH532CCCXY-SampleSheet-tag.csv

#Fold  | Lane | stat
------------  | ------------- | --------
171231_E00515_0258_AHFHVTCCXY  | L001 | CLN-WES 
171231_E00515_0258_AHFHVTCCXY  | L002 | CLN
171231_E00515_0258_AHFHVTCCXY  | L003 | WES-CLN-SR

2.根据SAV文件读取抓取信息
```python
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Extract_SAV_info.py SAV-file.info
```
- 说明
2.1 输入文件为SAV文件，文件命名后缀为.info
2.2 输出文件如下：

| #Folder|Machine|Lane|PF|PF_Bases|Q30_R1|Q30_R2|Q30_index|PF_reads|
|---|---|---|---|---|---|---|---|---|
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L001|73.8|138.4|93.8|86.13|94.62|458.43| 
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L002|69.18|129.48|93.46|83.61|94.31|429.74
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L003|66.76|125.04|93.15|83.92|94.57|414.73
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L004|69.97|131.22|93.85|85.37|93.48|434.66
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L005|67.89|127.04|93.6|85.28|94.35|421.72
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L006|69.3|129.64|93.87|85.8|92.56|430.5
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L007|66.94|125.18|92.06|83.02|94.13|415.83
|171231_E00516_0253_BHFJ2LCCXY|X1_FCB|L008|64.07|119.9|91.66|81.49|93.31|398.0

3. 临床下机目录生成Clean数据，并统计每条lane的Clean数据量

```python
FCInfoHiseq_Clean.py
```

引用的代码有：
```python
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/FC_Info_all1.py
```

- 说明
3.1 代码运行目录为下机目录，且此目录下有171107_E00514_0240_AH532CCCXY-SampleSheet-tag.csv文件（此文件第一步得到）
3.2 输出中有CleanBases

4.RawData CleanData以及tag文件汇总

```python
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Combine_SAV_Clean_tag.py 171228_E00516_0250_AHFGLVCCXY-SAV.csv Summary_FlowCell_171228_E00516_0250_AHFGLVCCXY_Clean.csv 171228_E00516_0250_AHFGLVCCXY-SampleSheet-tag.csv
```  

- 说明
4.1 输入文件见代码说明
4.2 输出文件为汇总文件，具体见下表：

|#Machine|Folder|Lane|stat|PF(%)|PF_Bases|Q30_R1(%)|Q30_R2(%)|Q30_index(%)|PF_reads|Clean_reads|Clean_Bases|CleanReadsPct(%)|CleanDataPct(%)|Dex_Ratio(%)|SingelOrDual|CLN-or-SR
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L001|-|77.37|144.82|95.04|90.2|96.5|480.62|-|-|-|-|-|singel_index|SR-RNA-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L002|-|73.92|138.42|94.9|86.55|95.36|459.21|-|-|-|-|-|singel_index|SR-RNA-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L003|PASS|73.15|136.96|95.16|89.15|95.33|454.42|425.61|120.67|93.66|88.11|96.64|singel_index|CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L004|-|74.9|140.48|94.68|86.15|95.85|465.28|-|-|-|-|-|singel_index|SR-RNA-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L005|-|71.07|133.12|93.94|85.68|95.08|441.5|-|-|-|-|-|singel_index|SR-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L006|-|70.37|131.84|94.06|87.2|94.85|437.17|-|-|-|-|-|singel_index|SR-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L007|-|69.4|129.96|93.64|86.13|94.56|431.09|-|-|-|-|-|singel_index|SR-CLN
X1_FCA|171228_E00516_0250_AHFGLVCCXY|L008|-|69.44|130.18|93.74|85.08|93.7|431.38|-|-|-|-|-|singel_index|SR-CLN

5. 每月仪器的上机情况

```python
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/UsingMachine.py result.csv
```
- 说明
5.1 输入文件：上步总结的result.csv
5.2 输出文件：输出每台仪器的上机情况

|#Machine_FC|FC_Num|Lane_Num|CLN_Lane_Num|SR_Lane_Num|Cln-Other_Lane_Num
|----|----|----|----|----|----|
4000|6|48|29|4|15
X1|18|144|22|76|46
X2|16|128|25|62|41
X3|10|80|0|79|1
X4|20|160|0|154|6
X5|11|88|0|88|0
YZ1|2|16|0|16|0
Total|83|664|76|479|109

6.对文件汇总的结果分临床和非临床

```markdown
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Split_CLN.py result.csv
```
- 说明
6.1 输入文件为result.csv
6.2 输出文件为CLN-result/Result-Cln.csv Other-result/Result-other.csv

7. 指标统计（分仪器，分是否临床）

```markdown
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Machine_boxplot_input.py Result-Cln.csv/Result-other.csv CLN/Other
```

- 说明
7.1 输入文件为临床或分临床的输入文件
7.2 输出文件为分仪器分指标的最大值，最小值，平均数，方差等

### 月汇报代码：
```python
mkdir result result/CleanInfo result/CLN-result/Machine_boxplot result/Other-result/Machine_boxplot
for i in `ls *info`;do echo "/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Extract_SAV_info.py "$i"";done | sh >result/SAV-result.csv
cp ~/SequencingData/1712*/*Clean.csv result/
mv *Clean.csv CleanInfo/
rm CleanInfo/*R1_Clean.csv
rm CleanInfo/*R2_Clean.csv
for i in `cat id.folder | grep -v '_C' | grep -v '_M' | grep -v '_A00'`;do echo "/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/SequecingData_SampleSheet_tag.py "$i"";done | sh >result/SampleSheet-tag.csv
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Combine_SAV_Clean_tag.py SAV-result.csv Summary_clean.csv SampleSheet-tag.csv >result.csv
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/UsingMachine.py result.csv
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Split_CLN.py result.csv
cd CLN-result
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Machine_boxplot_input.py Result-Cln.csv CLN >CLN-zhibiao.csv
cd Other-result
/GPFS01/home/zhangjf/scripts/3CollatingMonthlyData/Machine_boxplot_input.py Result-other.csv Other >Other-zhibiao.csv
cd Machine_boxplot
Rscript box_data.R Clean_Bases.csv Clean_Bases Clean_Bases.pdf
Rscript box_data.R PF_Bases.csv PF_Bases PF_Bases.pdf
Rscript box_Pct.R Q30_R1.csv Q30_R1 Q30_R1.pdf
Rscript box_Pct.R Q30_R2.csv Q30_R2 Q30_R2.pdf
Rscript box_Pct.R CleanDataPct.csv CleanDataPct CleanDataPct.pdf
Rscript box_Pct.R Dex_Ratio.csv Dex_Ratio Dex_Ratio.pdf

# CollatingMonthlyData
