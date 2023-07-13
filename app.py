import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://<YOUR LAN IP>:7860" #alternatively, an FQDN

counter = 0 #keep track of for loop cycles

for i in range(4): # send the payloads
    if(counter == 0):
        input = "what"
        style = " liam brazier, Anton Fadeev, generative art"
        payload = {
            "prompt": input + style,
            "steps": 35,
            "width": 512,
            "height": 512,
        }
    if(counter == -1):
        input = "what is your" 
        payload = {
            "prompt": input + style,
            "steps": 35,
            "width": 512,
            "height": 512,
        }
    if(counter == -2): 
        input = "who is your favourite ice"
        payload = {
            "prompt": input + style,
            "steps": 35,
            "width": 512,
            "height": 512,
        }   
    if(counter == -3):
        input = "who is your favourite ice cream flavor?" 
        payload = {
            "prompt": input + style,
            "steps": 35,
            "width": 512,
            "height": 512,
        }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload) #request response

    r = response.json() #save response here (image stored as binary within a JSON)

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0]))) # decode the binary image

        png_payload = {
        "image": "data:image/png;base64," + i #pull image from JSON
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload) #import payload

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('output.png', pnginfo=pnginfo) #output png

    counter = counter -1 #increment counter

    print(-counter, input) #print to console
