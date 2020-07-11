import happybase
conn=happybase.Connection('192.168.1.156')
table=conn.table('fusionasa2')
st=57758500
en=57772954
for k,data in table.scan():
    if (int(data['variants_info:start']) >= en):
        continue
    if int(data['variants_info:start']) in range(st, en) and int(data['variants_info:end']) in range(st, en):
        print(k)