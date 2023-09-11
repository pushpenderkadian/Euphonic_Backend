from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

import numpy as np
app = FastAPI()
origins = [
    "http://127.0.0.1:5501",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/get_bands")
def index():
    file=open("db/bands.json")
    bands=json.load(file)
    file.close()
    return bands

class music(BaseModel):
    band1:str
    band2:str
    band3:str

@app.post("/get_musicid")
def musicid(request:music):
    file=open("db/musicranks.json")
    file1=open("db/musics.json")
    musics=json.load(file1)
    bandslm=json.load(file)
    
    file.close()
    file1.close()
    respbands=[]
    respbands.append(request.band1)
    respbands.append(request.band2)
    respbands.append(request.band3)
    bid=""
    for i in respbands:
        bid=bid+i
        bid=bid+"_"
    
    try:
        if(len(bandslm[bid])<5 and len(bandslm[bid])>0):
            while(True):
                music_id=np.random.randint(0,len(musics))
                if(str(music_id) not in bandslm[bid]):
                    break
            bandslm[bid].append(str(music_id))
            file=open("db/musicranks.json","w")
            json.dump(bandslm,file)
            file.close()
            return str(music_id)
        mids=bandslm[bid]

        musicdets=[]
        for i in mids:
            musicdets.append(musics[i])
        print(mids)
        names=[]
        like=[]
        for i in musicdets:
            names.append(i["name"])
            like.append(int(i["likes"]))
        likes=np.array(like)
        idx=likes.argsort()
        music_id=""
        for i in range(0,len(musics)):
            if(musics[str(i)]["name"]==(names[idx[-1]])):
                music_id=str(i)
                break
    except KeyError:        
        music_id=np.random.randint(0,len(musics))
        bandslm[bid]=[]
        bandslm[bid].append(str(music_id))
        
        file=open("db/musicranks.json","w")
        json.dump(bandslm,file)
        file.close()
    
    return str(music_id)

@app.get("/get_music_dets/{id}")
def music(id):
    file=open("db/musics.json")
    music=json.load(file)
    
    file.close()
    return music[id]

@app.get("/final")
def final():
    file=open("db/final.json")
    final=json.load(file)
    file.close()
    return final


class dld(BaseModel):
    band1:str
    band2:str
    band3:str

@app.post("/addlike/{id}")
def addlike(request:dld,id):
    file=open("db/musics.json")
    musics=json.load(file)
    musics[id]["likes"]=int(musics[id]["likes"])+1
    
    file.close()
    file=open("db/musics.json","w")
    json.dump(musics,file)
    file.close()
    return {"message":"success"}

class dislike(BaseModel):
    band1:str
    band2:str
    band3:str
@app.post("/dislike/{id}")
def dislike(request:dislike,id):
    file=open("db/musicranks.json")
    file1=open("db/musics.json")
    musics=json.load(file1)
    bandslm=json.load(file)
    
    file.close()
    file1.close()
    respbands=[]
    respbands.append(request.band1)
    respbands.append(request.band2)
    respbands.append(request.band3)
    bid=""
    for i in respbands:
        bid=bid+i
        bid=bid+"_"
    mids=bandslm[bid]

    musicdets=[]
    for i in mids:
        musicdets.append(musics[i])
    print(mids)
    names=[]
    like=[]
    for i in musicdets:
        names.append(i["name"])
        like.append(int(i["likes"]))
    likes=np.array(like)
    idx=likes.argsort()
    music_id=""
    for i in range(0,len(musics)):
        if(musics[str(i)]["name"]==(names[idx[-2]])):
            music_id=str(i)
            break
    return str(music_id)

class review(BaseModel):
    email:str
    message:str
    name:str
@app.post("/review")
def review(request:review):
    file3=open("db/reviews.json")
    reviews=json.load(file3)
    file3.close()
    data={"email":request.email,"message":request.message,"name":request.name}
    reviews.append(data)
    file=open("db/reviews.json","w")
    json.dump(reviews,file)
    file.close()
    return "success"