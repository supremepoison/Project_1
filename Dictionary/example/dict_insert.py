import pymysql
import re

f = open('/home/tarena/AID1808/Project_1/Dictionary/dict.txt')
db = pymysql.connect('localhost','root','123456','dictionary')

cursor = db.cursor()
pattern = r'([-a-z]+)\s+(.+)'

for line in f:
# line = f.readline()
    try:
        obj = re.match(pattern,line)
        word = obj.group(1)
        inter = obj.group(2)
    except:
        continue
    # print(word+':'+inter)
    sql = 'insert into words (word,interpret) values("%s","%s")' %(word,inter)

    try:
        cursor.execute(sql)
        db.commit()
    except:-
        db.rollback()
f.close()

