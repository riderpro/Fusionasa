import pandas as pd 
import numpy as np
import re
import sys
import time
#from datetime import datetime
start = time.time()
int_max=sys.maxsize
int_min=sys.maxsize*-1
#the database to calculate cyto start end
gene_db = pd.read_csv(r'C:\final_year\db\HGNC\hgnc_complete_set.csv', encoding='utf_8')
cyt_db = pd.read_csv(r'C:\final_year\db\cytoBand.csv', encoding='utf_16')#the reference db
c_bio=len(gene_db.index)#total records in database
c_cyto=len(cyt_db.index)#total records in reference db
new=pd.DataFrame(columns=['chrno','start','end'])#creating dataframes with 3 columns
for i in range(0,c_bio):#iterating through  all records in the database
	code=gene_db['Cytoband'][i]#the cytoband in db whose start end to be calculated
	print(i,gene_db['hgnc_id'][i],gene_db['symbol'][i])
	if code is np.nan:
		#print('nan')
		continue
	if ('p' not in code) :
		if 'q' not in code:
			#print('other exception')
			continue
	if 'cen' in code:
		continue
	if 'ter' in code:
		continue
	# checking if the cytoband is single(3p56.5) or a range(4p56.5-p56.8)
	list_of_cytoband=re.split(r'-',code)
	l=len(list_of_cytoband)
	if l==1:
		list_of_cytoband = re.split(r'\|', code)
		l = len(list_of_cytoband)

	if l==1:#if the cytoband is not a range
		# extracting cytoband without chromose no
		cyt=re.search('([pq]\d*).*',code)[0]
		chrno1=re.search('(\w*)([pq]\d*).*',code)[1]#extracting only chromosome no
		for j in range(0,c_cyto):#iterating through all records in reference db
			chrno2=re.search('(chr)(\w*)',cyt_db['chromosome'][j])[2]
			start=cyt_db['start'][j]
			end=cyt_db['end'][j]
			band=cyt_db['cytoband'][j]
			if(chrno1==chrno2):
				if cyt in band:
					if(end>int_min):
						int_min=end
						if(start<int_max):
							int_max=start
		new.loc[i]=[chrno1,int_max,int_min]
		int_max=sys.maxsize
		int_min=sys.maxsize*-1
	else:
		#if the cytoband of a particular record is a range
		if len(list_of_cytoband) == 2:
			# starting cytoband of particular row of the database
			code1 = list_of_cytoband[0]
			code2 = list_of_cytoband[1]#ending cytoband of particular row of database
			code1chr = re.search(r'(\w+)[pq]', code1)[1]
			code2chr = code1chr
			code1 = re.search(r'(\w+)([pq]\d+(.\d*)?)', code1)[2]
			for j in range(0, c_cyto):
				chrno_ref = re.search(r'(chr)(\w*)', cyt_db['chromosome'][j])[2]
				start = cyt_db['start'][j]
				end = cyt_db['end'][j]
				band = cyt_db['cytoband'][j]
				if chrno_ref == code1chr:
					if (code1 in band) or (code2 in band):
						#print(i," : ",code1, " ", code2, " ", band, " ", start, " ", end)
						if end > int_min:
							int_min = end
						if start < int_max:
							int_max = start

			new.loc[i] = [code1chr, int_max, int_min]
			#print(new.loc[i])
			int_max=sys.maxsize
			int_min=sys.maxsize*-1
new.to_csv('chrStrtEnd.csv')
mrg=pd.merge(gene_db,new,left_index=True,right_index=True,how='left')
mrg.to_csv(r'C:\final_year\db\HGNC\hgnc_complete_set_complete.csv')
end = time.time()
print((end - start)/60,'minutes')
