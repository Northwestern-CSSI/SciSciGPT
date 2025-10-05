import base64
import os
from func.gcp import upload_file_to_gcp

workspace = os.getenv("LOCAL_STORAGE_PATH")

def load_image(image_path) -> dict:
    def encode_image(image_data):
        return base64.b64encode(image_data).decode('utf-8')

    if image_path.startswith(('http://', 'https://')):
        # If it's a URL, fetch and encode the image
        import requests
        response = requests.get(image_path)
        response.raise_for_status()
        image_base64 = encode_image(response.content)
    else:
        # If it's a local file, read and encode it
        with open(image_path, "rb") as image_file:
            image_base64 = encode_image(image_file.read())

    return {'base64': image_base64}


import uuid
def upload_image(img: str, img_type: str='path'):

    try:
        import requests
        import io
        import base64

        if img_type == 'base64':
            # Handle both "data:image/png;base64,XXXXX" and "XXXXX" formats
            if img.startswith('data:'):
                # Extract base64 part after the comma
                img = img.split(',')[1]
            # Convert base64 to bytes and save temporarily
            image_data = base64.b64decode(img)
            temp_path = f"{workspace}/{uuid.uuid4()}.png"
            with open(temp_path, "wb") as f:
                f.write(image_data)
            img = temp_path
            temp_file_created = True
        elif img_type == 'path':
            temp_file_created = False
        else:
            raise ValueError("img_type must be either 'base64' or 'path'")
        
        response = upload_file_to_gcp(img)
        return response
        
    except Exception as e:
        return str(e)


import json
from typing import Union
def multimodal_item(item: dict) -> list[dict]:
    if item["type"] == "text":
        try:
            item_list = [item]
            item = json.loads(item["text"])
            if "images" in item:
                for image in item["images"]:
                    image_base64 = load_image(image["download_link"])["base64"]
                    mime_type = image["mime_type"]
                    image_url = f"data:{mime_type};base64,{image_base64}"
                    item_list.append({"type": "image_url", "image_url": { "url": image_url }})
            
        except:
            item_list = [item]
    else:
        item_list = [item]

    return item_list


from langchain_core.messages import AnyMessage, HumanMessage
from copy import deepcopy
def show_images_to_llm(message: AnyMessage) -> AnyMessage:
    content = message.content
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]

    new_content = []
    for item in content:
        new_content += multimodal_item(item)
    
    return HumanMessage(content=new_content)



from typing import Union
import json
from langchain_core.messages import AnyMessage

def if_item_contains_image(item: Union[str, dict]) -> bool:
    try:
        item = json.loads(item) if isinstance(item, str) else item
        return "images" in item
    except:
        return False
    
def if_message_contains_image(message: AnyMessage) -> bool:
    content = message.content
    content = [{"type": "text", "text": content}] if isinstance(content, str) else content

    for item in content:
        if if_item_contains_image(item.get("text", "")):
            return True
    return False