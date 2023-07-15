import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import io

url = "http://10.0.0.150:7860"
image2 = open('output.png', 'rb').read()

def img_to_base64(image2):
    base64_str = str(base64.b64encode(image2), "utf-8")
    return "data:image/png;base64," + base64_str


payload = {
                "init_images": [img_to_base64(image2)] ,
                "resize_mode": 0,
                "denoising_strength": 0.75,
                "image_cfg_scale": 0,
                "mask_blur": 4,
                "inpainting_fill": 0,
                "inpaint_full_res": True,
                "inpaint_full_res_padding": 0,
                "inpainting_mask_invert": 0,
                "initial_noise_multiplier": 0,
                "prompt": "",
                "seed": -1,
                "subseed": -1,
                "subseed_strength": 0,
                "seed_resize_from_h": -1,
                "seed_resize_from_w": -1,
                "batch_size": 1,
                "n_iter": 1,
                "steps": 50,
                "cfg_scale": 7,
                "width": 512,
                "height": 512,
                "restore_faces": False,
                "tiling": False,
                "do_not_save_samples": False,
                "do_not_save_grid": False,
                "negative_prompt": "",
                "eta": 0,
                "s_min_uncond": 0,
                "s_churn": 0,
                "s_tmax": 0,
                "s_tmin": 0,
                "s_noise": 1,
                "override_settings": {},
                "override_settings_restore_afterwards": True,
                "script_args": [],
                "sampler_index": "Euler",
                "include_init_images": False,
                "script_name": "",
                "send_images": True,
                "save_images": False,
                "alwayson_scripts": {}
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
            image.save('output2.png', pnginfo=pnginfo)
