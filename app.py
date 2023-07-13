import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://10.0.0.150:7860"

payload = {
    "prompt": "a mountain scene with a red and orange sky and trees on the mountainside, with a few clouds, vector art, liam brazier, Anton Fadeev, generative art",
    "steps": 35
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)
