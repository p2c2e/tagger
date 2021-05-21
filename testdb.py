import mysql.connector
from pydantic import BaseModel
from typing import Optional, List
from model import TagType, TagDetail


mydb = mysql.connector.connect(
  host="localhost",
  database='tagger',
  user="root",
  port=30006,
  password="mysql"
)

print(mydb)


def load_tags():
  rv = []
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM tag_detail")
  myresult = mycursor.fetchall()
  for flds in myresult:
    tt = TagDetail(id=flds[0], url=flds[1], typ=flds[2], name=flds[3])      
    print(tt)
    rv.append(tt)
  return rv

def write_tag(t):
  mycursor = mydb.cursor()
  if t.id:
    print("In the update section <<<<<<<<<<<<<<<<< ")
    # update
    sql = "UPDATE tag_detail SET url = %s, typ = %s, name = %s WHERE tag_id = %s"
    val = (t.url, t.typ, t.name, t.id)
    mycursor.execute(sql, val)
  else:
    sql = "INSERT INTO tag_detail (url, typ, name) VALUES (%s, %s, %s)"
    val = (t.url, t.typ, t.name)
    mycursor.execute(sql, val)
  mydb.commit()


def write_tags(rv):
  print("--------> "+str(len(rv)))
  with open('tags', 'w') as f:
    lines = []
    for val in rv:
      print(val)
      line = val.url + "," + val.typ + "," + val.name 
      print(line)
      lines.append(line+"\n")
    f.write("".join(lines))
  x = TagDetailList(all_tags=rv)
  with open('tags.json', 'w') as f:
    f.write(x.json())

  return rv

def load_tagtypes():
  rv = []
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM tag_type")
  myresult = mycursor.fetchall()
  for flds in myresult:
    tt = TagType(id=flds[0], name=flds[1], color=flds[2])      
    print(tt)
    rv.append(tt)
  return rv

def write_tagtype(t):
  mycursor = mydb.cursor()
  if t.id:
    print("In the update section <<<<<<<<<<<<<<<<< ")
    # update
    sql = "UPDATE tag_type SET name = %s , color = %s WHERE tag_type_id = %s"
    val = (t.name, t.color, t.id)
    mycursor.execute(sql, val)
  else:
    sql = "INSERT INTO tag_type (tag_type_id, name, color) VALUES (%s, %s, %s)"
    val = (t.id, t.name, t.color)
    mycursor.execute(sql, val)
  mydb.commit()


print(load_tags())
print(load_tagtypes())
# write_tag(TagDetail(id=5, url='New URL 2', typ='Industry', name='TMT'))
write_tagtype(TagType(id=3, name="NewType", color="Black"))
print(load_tagtypes())

mydb.disconnect()
