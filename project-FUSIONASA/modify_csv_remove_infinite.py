import pandas as pd
import numpy as np

import sys
import time
#from datetime import datetime
start = time.time()
int_max=sys.maxsize
int_min=sys.maxsize*-1
gene_db = pd.read_csv(r'~/Downloads/for_infinite_db/Tumor_suppressor_gene_complete_set_with_start_end.csv', encoding='utf_8')#the database to calculate cyto start end
c_bio=len(gene_db.index)#total records in database
# new=pd.DataFrame(columns=['chrno','start','end'])#creating dataframes with 3 columns
for i in range(0,c_bio):#iterating through  all records in the database
	# code=gene_db['Cytoband'][i]#the cytoband in db whose start end to be calculated
	start=gene_db['start'][i]
	end=gene_db['end'][i]
	if (abs(start-int_max)==3372036854775808.0):
		gene_db=gene_db.drop(i,axis=0)
		print('inside')
gene_db.to_csv(r'~/Downloads/removed_infinite/Tumor_suppressor_gene.csv')
end = time.time()
print(end)
