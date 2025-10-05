from langchain_core.messages import HumanMessage, ToolMessage
from func.image import load_image
import json

def _multimodal_item(item: dict) -> list[dict]:
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



def _multimodal_message(message: ToolMessage) -> HumanMessage:
    content = message.content
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]

    new_content = []
    for item in content:
        new_content += _multimodal_item(item)
    
    return HumanMessage(content=new_content)