import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from firebase_admin import credentials, initialize_app, storage
import random2
import os

# Open the JSON file
with open('prompt.json') as f:
    data = json.load(f)

# Access the 'user' variable and print its value
poll = data['poll']
answer1 = data['answer1']
answer2 = data['answer2']
answer3 = data['answer3']
answer4 = data['answer4']
pollId = random2.randint(100000,999999)


#initialize firebase app w/ credentials
cred = credentials.Certificate('firebase_key.json')
initialize_app(cred, {'storageBucket': 'quid-eda9a.appspot.com'})

#declare AI server URL
url = "http://10.0.0.150:7860"


#Image gen components
style= "((dark)),lofi, vibrant, colorful, vector art" 
#prompts = "outer space"
negative_prompt = "Split frame, out of frame, cropped, multiple frame, split panel, multi panel,amputee,autograph,bad anatomy,bad illustration,bad proportions,beyond the borders,blank background,blurry,body out of frame,boring background,branding,cropped,cut off,deformed,disfigured,dismembered,disproportioned,distorted,draft,duplicate,duplicated features,extra arms,extra fingers,extra hands,extra legs,extra limbs,fault,flaw,fused fingers,grains,grainy,gross proportions,hazy,identifying mark,improper scale,incorrect physiology,incorrect ratio,indistinct,kitsch,logo,long neck,low quality,low resolution,macabre,malformed,mark,misshapen,missing arms,missing fingers,missing hands,missing legs,mistake,morbid,mutated hands,mutation,mutilated ,off-screen,out of frame,out of frame,outside the picture,pixelated,poorly drawn face,poorly drawn feet,poorly drawn hands,printed words,render,repellent,replicate,reproduce,revolting dimensions,script,shortened,sign,signature,split image,squint,storyboard,text,tiling,trimmed,ugly,unfocused,unattractive,unnatural pose,unreal engine,unsightly,watermark,written language"

# Payloads
payload = {
    "prompt": poll + style + answer1 + answer2 + answer3 + answer4,
    "steps": 20,
    "seed": -1,
    "length": 512, 
    "width": 512,
    'sampler_index': "DPM2 Karras",
    'cfg_scale': 7,
    'restore_faces': True,
    'negative_prompt': negative_prompt
            }

option_payload = {
    "sd_model_checkpoint": "dreamshaper_7.safetensors [ed989d673d]",
    "CLIP_stop_at_last_layers": 2
    }


#API POST request to Standard-diffusion
print(payload)
response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
r = response.json()

#decode JSON image into PNG
with open('json_data.json', 'w') as outfile:
    outfile.write(str(r))
for j in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(j.split(",",1)[0])))
    png_payload = {
        "image": "data:image/png;base64," + j
        }
    

#API POST request for image metadata   
response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
pnginfo = PngImagePlugin.PngInfo()
pnginfo.add_text("parameters", response2.json().get("info"))
image.save('output_X.png', pnginfo=pnginfo)


    # Put your local file path 
fileName = 'output_X.png'
bucket = storage.bucket()
blob = bucket.blob('wallpapers/{}/{}'.format(pollId,fileName))
blob.upload_from_filename(fileName)

# Opt : if you want to make public access from the URL
blob.make_public()
imageURL = blob.public_url
url_json = {'url':imageURL}
print(json.dumps(url_json))
with open('image_url.json', 'w') as f:
    json.dump(url_json, f)
