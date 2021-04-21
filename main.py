from typing import Optional
from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random

app = FastAPI()
class TagDetail(BaseModel):
  url: str
  typ: str
  name: str

class TagType(BaseModel):
  name: str
  color: str

class TagDetailList(BaseModel):
    all_tags: List[TagDetail]


def load_tags():
  rv = []
  with open('tags', 'r') as f:
    for line in f:
      flds = line.rstrip().split(',')
      tt = TagDetail(name=flds[2], url=flds[0], typ=flds[1])      
      print(tt)
      rv.append(tt)

  from io import StringIO
  import json
  rv = []
  with open('tags.json', 'r') as f:
    json_data_file = f.readlines()
    json_data_file = "\n".join(json_data_file)
    inp = json.load(StringIO(json_data_file))
    print(type(inp))
    item_list2 = TagDetailList(all_tags=inp["all_tags"])
    print("------------ 5 ", item_list2)
  return rv

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
  with open('tagtypes', 'r') as f:
    for line in f:
      flds = line.rstrip().split(',')
      tt = TagType(name=flds[0], color=flds[1])      
      print(tt)
      rv.append(tt)
  return rv

@app.post('/tag')
async def tag_item(item: TagDetail):
  tt = load_tags()
  print("------ 4"+str(len(tt)))
  for tag in tt:
    if( tag.url == item.url ):
      tag.typ = item.typ
      tag.name = item.name
      write_tags(tt)
      return item
  print("------- 2")
  tt.append(item)
  write_tags(tt)
 
  return item


@app.get('/tag/{url}')
async def get_tag(url: str):
  tt = load_tags()
  print(url)
  for tag in tt:
    print('-'+tag.url+'-')
    if( tag.url == url ):
      return tag
  return { "error" : "Unable to find item" }
  

@app.get('/test')
async def test_item():
  return write_tags([TagDetail(url='url', typ='TYPE', name='NAME')])

@app.get('/tagtypes')
async def get_tag_types():
  return [ x[1] for (x, _) in load_tagtypes() ]

async def say_hello():
  return JSONResponse(content={ 
"tagtypes": [
  "industry",
  "type",
  "format",
  "cloud" 
]
})

@app.get('/tagmeta/{tagtype}')
async def tag_meta(tagtype: str):
  tt = load_tagtypes()
  for tag in tt:
    print('-'+tag.name+'-')
    if( tag.name == tagtype ):
      return tag 
  
  return JSONResponse(content={
  "error": "Did not find "+tagtype
})
