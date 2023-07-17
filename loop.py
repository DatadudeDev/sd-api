import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from firebase_admin import credentials, initialize_app, storage
import random2
import random
import string
import os


# Open the JSON file
with open('user_data.json') as f:
    data = json.load(f)

# Access the 'user' variable and print its value
username = data['user']
poll = data['poll']
os.remove("user_data.json")

cred = credentials.Certificate('firebase_key.json')
initialize_app(cred, {'storageBucket': 'quid-eda9a.appspot.com'})

url = "http://10.0.0.150:7860"
input = "Generate an image depicting a subject expressing uncertainty or contemplation, with a sense of curiosity and openness. Colors like shades of blue and green may be associated with the subject's introspection. subject, uncertainty, contemplation, curiosity, openness, blue, green"
counter = 0
seed = random2.randint(0,1000000)
style= "Cartoon Network Studios, 2D animation, Color: Vibrant, bold, composition: Dynamic, exaggerated, exaggerated proportions"

prompts = ["was"
        ,"was 9/11"
        #,"was 9/11 an inside job"
        #,"was 9/11 an inside job by the US government"
         ]
negative_prompt = "Split frame, out of frame, cropped, multiple frame, split panel, multi panel,amputee,autograph,bad anatomy,bad illustration,bad proportions,beyond the borders,blank background,blurry,body out of frame,boring background,branding,cropped,cut off,deformed,disfigured,dismembered,disproportioned,distorted,draft,duplicate,duplicated features,extra arms,extra fingers,extra hands,extra legs,extra limbs,fault,flaw,fused fingers,grains,grainy,gross proportions,hazy,identifying mark,improper scale,incorrect physiology,incorrect ratio,indistinct,kitsch,logo,long neck,low quality,low resolution,macabre,malformed,mark,misshapen,missing arms,missing fingers,missing hands,missing legs,mistake,morbid,mutated hands,mutation,mutilated ,off-screen,out of frame,out of frame,outside the picture,pixelated,poorly drawn face,poorly drawn feet,poorly drawn hands,printed words,render,repellent,replicate,reproduce,revolting dimensions,script,shortened,sign,signature,split image,squint,storyboard,text,tiling,trimmed,ugly,unfocused,unattractive,unnatural pose,unreal engine,unsightly,watermark,written language"






####################################### Text2Image ###############################################
for i in prompts:
    if counter == 0: 
        payload = {
                "prompt": i + style,
                "steps": 20,
                "seed": seed,
                "length": 512, 
                "width": 512,
                'sampler_index': "DPM2 Karras",
                'cfg_scale': 7,
                'restore_faces': True,
                'negative_prompt': negative_prompt
            }
        option_payload = {
            "sd_model_checkpoint": "models/hestylev15Rooms_v15.ckpt [b931cc5ece]",
            "CLIP_stop_at_last_layers": 2
            }
        response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        with open('json_data.json', 'w') as outfile:
            outfile.write(str(r))
        for j in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(j.split(",",1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + j
                }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
            print(counter , "--->" , i)
            counter = counter + 1
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            version = counter
            image.save('output_{}.png'.format(version), pnginfo=pnginfo)
            image.save('output_X.png', pnginfo=pnginfo)


            # Put your local file path 
            fileName = 'output_{}.png'.format(counter)
            bucket = storage.bucket()
            blob = bucket.blob('wallpapers/{}/{}/{}/'.format(username,poll,fileName))
            blob.upload_from_filename(fileName)

            # Opt : if you want to make public access from the URL
            blob.make_public()
            print("your file url", blob.public_url)   
    else:

        image2 = open('output_X.png', 'rb').read()
        def img_to_base64(image2):
            base64_str = str(base64.b64encode(image2), "utf-8")
            return "data:image/png;base64," + base64_str

        payload = {
                "init_images": [img_to_base64(image2)],
                'prompt' : style + i,
                "steps": 20,
                "cfg_scale": 7,
                "batch_size": 1,
                "negative_prompt": negative_prompt,
                "sampler_index": "DPM++ SDE Karras",
                "save_images": False,
                "restore_faces": True,
                "width": 512,
                "height": 512,
                "denoising_strength": 0.85,
                "seed": seed,
                "script_name": "",
            }
        option_payload = {
                    "sd_model_checkpoint": "models/hestylev15Rooms_v15.ckpt [b931cc5ece]",
                    "CLIP_stop_at_last_layers": 2
                    }

        response3 = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

        response3 = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)

        r2 = response3.json()

        with open('json_data2.json', 'w') as outfile:
                outfile.write(str(r2))

                for j in r2['images']:
                    image = Image.open(io.BytesIO(base64.b64decode(j.split(",",1)[0])))
                    png_payload3 = {
                        "image": "data:image/png;base64," + j
                        }
                    response4 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload3)
                    print(counter, "--->",  i)
                    counter +=1
                    pnginfo = PngImagePlugin.PngInfo()
                    pnginfo.add_text("parameters", response4.json().get("info"))
                    version = counter
                    image.save('output_{}.png'.format(version), pnginfo=pnginfo)
                    image.save('output_X.png'.format(version), pnginfo=pnginfo)

                # Put your local file path 
                fileName = 'output_{}.png'.format(counter)
                bucket = storage.bucket()
                blob = bucket.blob('wallpapers/{}/{}/{}/'.format(username,poll,fileName))
                blob.upload_from_filename(fileName)

                # Opt : if you want to make public access from the URL
                blob.make_public()
                print("your file url", blob.public_url)
