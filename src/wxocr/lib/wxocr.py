import os
import uuid
import base64
import json
from . import wcocr



wxocr_path = "/opt/wechat/wxocr"
wechat_path = "/opt/wechat"

if not os.path.exists(wxocr_path):
    raise RuntimeError(f"WeChat OCR path not found: {wxocr_path}")
if not os.path.exists(wechat_path):
    raise RuntimeError(f"WeChat path not found: {wechat_path}")

wcocr.init("/opt/wechat/wxocr", "/opt/wechat")


def ocr(base64_img):
    try:
        # Create temp directory if not exists
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        if not base64_img:
            return jsonify({"error": "No base64 image data provided"})
        # Extract image type from base64 data
        image_type, base64_img = extract_image_type(base64_img)
        if not image_type:
            # 返回json错误信息
            return jsonify({"error": "Invalid base64 image data"})
        # Generate unique filename and save image
        filename = os.path.join(temp_dir, f"{str(uuid.uuid4())}.{image_type}")
        try:
            image_bytes = base64.b64decode(base64_img)
            with open(filename, "wb") as f:
                f.write(image_bytes)

            # Process image with OCR
            result = wcocr.ocr(filename)
            return jsonify(result)

        finally:
            # Clean up temp file
            if os.path.exists(filename):
                os.remove(filename)

    except Exception as e:
        return jsonify({"error": str(e)})


def extract_image_type(base64_data):
    # Check if the base64 data has the expected prefix
    if base64_data.startswith("data:image/"):
        # Extract the image type from the prefix
        prefix_end = base64_data.find(";base64,")
        if prefix_end != -1:
            return (
                base64_data[len("data:image/") : prefix_end],
                base64_data.split(";base64,")[-1],
            )
    return "png", base64_data

def jsonify(data, status=200):
    """模拟 Flask 的 jsonify 行为"""
    return json.dumps(data, ensure_ascii=False), status

