import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import random2

url = "http://10.0.0.150:7860"
input = "Generate an image depicting a subject expressing uncertainty or contemplation, with a sense of curiosity and openness. Colors like shades of blue and green may be associated with the subject's introspection. subject, uncertainty, contemplation, curiosity, openness, blue, green"
counter = 0
seed = random2.randint(0,1000000)
style= "surreal, cyberpunk, lofi, calm"
prompts = ["a beautiful sunrise scene,astronaught standing on a foreign planet, ((colors)) view of outer space, bright planets, stars, Bob Thompson, naturalism, landscape"
            ,"a beautiful daytime scene, astronaught standing on a foreign planet, ((colors)) view of outer space, bright planets, stars, Bob Thompson, naturalism, landscape"
            ,"(dark) a beautiful evening scene, astronaught standing on a foreign planet, ((colors)) view of outer space, bright planets, stars, Bob Thompson, naturalism, landscape"
            ,"((dark)) a beautiful night scene,astronaught standing on a foreign planet, ((colors)) view of outer space, bright planets, stars, Bob Thompson, naturalism, landscape"
            ,"((pitch black)) a beautiful midnight scene,astronaught standing on a foreign planet, ((outer space)), Full moon, galaxies, shooting stars, stars, Bob Thompson, naturalism, landscape"]
negative_prompt = "(((text, watermark))), blur, clouds, fog, mist, ugly, chaotic, yellow"

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
        counter = counter + 1
        print(counter)
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + i
                }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            version = counter
            image.save('output_{}.png'.format(version), pnginfo=pnginfo)
            image.save('output_X.png', pnginfo=pnginfo)
    
    
    else:
        counter +=1
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

                for i in r2['images']:
                    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                    png_payload3 = {
                        "image": "data:image/png;base64," + i
                        }
                    response4 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload3)

                    pnginfo = PngImagePlugin.PngInfo()
                    pnginfo.add_text("parameters", response4.json().get("info"))
                    version = counter
                    image.save('output_{}.png'.format(version), pnginfo=pnginfo)
                    image.save('output_X.png'.format(version), pnginfo=pnginfo)
