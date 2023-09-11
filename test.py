import json
import numpy as np
id="2"
file=open("db/musicranks.json")
file1=open("db/musics.json")
musics=json.load(file1)
bandslm=json.load(file)
respbands=[]
# respbands.append(request.band1)
# respbands.append(request.band2)
# respbands.append(request.band3)
bid="Euphoria_blackpink_bts_"
# for i in respbands:
#     bid=bid+i
#     bid=bid+"_"
mids=bandslm[bid]

musicdets=[]
for i in mids:
    musicdets.append(musics[i])
names=[]
like=[]
for i in musicdets:
    names.append(i["name"])
    like.append(int(i["likes"]))
likes=np.array(like)
sorted=np.sort(likes)
print(sorted)
idx=np.where(sorted==id)
print(idx)
idx=idx-1
music_id=""
for i in range(0,len(musics)):
    if(musics[str(i)]["name"]==(names[sorted[idx]])):
        music_id=str(i)
        break