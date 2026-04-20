import json
from typing import Any

from llm_client import invoke_text


PRODUCTS = {
    "TechPro Ultrabook": {
        "name": "TechPro Ultrabook",
        "category": "电脑和笔记本",
        "brand": "TechPro",
        "model_number": "TP-UB100",
        "warranty": "1年",
        "rating": 4.5,
        "features": ["13.3 英寸屏幕", "8GB 内存", "256GB SSD", "Intel Core i5"],
        "description": "轻薄便携，适合日常办公和学习。",
        "price": 799.99,
    },
    "BlueWave Gaming Laptop": {
        "name": "BlueWave Gaming Laptop",
        "category": "电脑和笔记本",
        "brand": "BlueWave",
        "model_number": "BW-GL200",
        "warranty": "2年",
        "rating": 4.7,
        "features": ["15.6 英寸屏幕", "16GB 内存", "512GB SSD", "RTX 3060"],
        "description": "面向游戏和高性能需求的笔记本。",
        "price": 1199.99,
    },
    "BlueWave Chromebook": {
        "name": "BlueWave Chromebook",
        "category": "电脑和笔记本",
        "brand": "BlueWave",
        "model_number": "BW-CB100",
        "warranty": "1年",
        "rating": 4.1,
        "features": ["11.6 英寸屏幕", "4GB 内存", "32GB eMMC", "ChromeOS"],
        "description": "轻量入门机型，适合网页办公。",
        "price": 249.99,
    },
    "SmartX ProPhone": {
        "name": "SmartX ProPhone",
        "category": "手机和配件",
        "brand": "SmartX",
        "model_number": "SX-PP10",
        "warranty": "1年",
        "rating": 4.6,
        "features": ["6.1 英寸屏幕", "128GB 存储", "双摄", "5G"],
        "description": "主打拍照和日常旗舰体验的智能手机。",
        "price": 899.99,
    },
    "CineView 4K TV": {
        "name": "CineView 4K TV",
        "category": "电视和家庭影院",
        "brand": "CineView",
        "model_number": "CV-4K55",
        "warranty": "2年",
        "rating": 4.8,
        "features": ["55 英寸", "4K", "HDR", "智能电视"],
        "description": "画质均衡，适合家庭观影。",
        "price": 599.99,
    },
    "SoundMax Home Theater": {
        "name": "SoundMax Home Theater",
        "category": "电视和家庭影院",
        "brand": "SoundMax",
        "model_number": "SM-HT100",
        "warranty": "1年",
        "rating": 4.4,
        "features": ["5.1 声道", "1000W 输出", "低音炮", "蓝牙"],
        "description": "适合客厅影音升级的家庭影院套装。",
        "price": 399.99,
    },
    "FotoSnap DSLR Camera": {
        "name": "FotoSnap DSLR Camera",
        "category": "相机和摄像设备",
        "brand": "FotoSnap",
        "model_number": "FS-DSLR200",
        "warranty": "1年",
        "rating": 4.7,
        "features": ["2420 万像素", "1080p 视频", "3 英寸屏幕", "可换镜头"],
        "description": "适合入门摄影和旅行拍摄。",
        "price": 599.99,
    },
}


def extract_catalog_matches(user_input: str) -> list[dict[str, Any]]:
    catalog = json.dumps(list(PRODUCTS.values()), ensure_ascii=False, indent=2)
    prompt = f"""
你是商品识别助手。请根据用户问题，从给定商品目录中找出相关商品。

要求：
1. 只返回 JSON 数组。
2. 每一项只包含 "name" 和 "category" 两个字段。
3. 如果用户提到某个品类但没有提到具体商品，可以返回该品类下所有相关商品。
4. 如果没有匹配项，返回 []。

商品目录：
{catalog}

用户问题：{user_input}
""".strip()

    response = invoke_text(prompt, temperature=0)
    return json.loads(response)


def get_product_details(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not matches:
        return []

    selected_names = {item["name"] for item in matches if "name" in item}
    selected_categories = {item["category"] for item in matches if "category" in item}

    results = []
    for product in PRODUCTS.values():
        if product["name"] in selected_names or product["category"] in selected_categories:
            results.append(product)
    return results


def build_final_response(user_input: str, product_details: list[dict[str, Any]]) -> str:
    details_text = json.dumps(product_details, ensure_ascii=False, indent=2)
    prompt = f"""
你是电商平台客服。请结合用户问题和系统查询到的商品信息，给出简洁、自然、友好的中文回复。
如果商品信息为空，直接说明未找到相关商品，并引导用户换个关键词继续提问。

用户问题：{user_input}

商品信息：
{details_text}
""".strip()

    return invoke_text(prompt, temperature=0.4)


def chaining_prompt_demo() -> None:
    user_input = "请告诉我 SmartX ProPhone 和 FotoSnap DSLR Camera 的情况，另外也介绍一下你们的电视。"

    matches = extract_catalog_matches(user_input)
    print("============= Extracted Matches =============")
    print(json.dumps(matches, ensure_ascii=False, indent=2))

    product_details = get_product_details(matches)
    print("============= Product Details =============")
    print(json.dumps(product_details, ensure_ascii=False, indent=2))

    final_response = build_final_response(user_input, product_details)
    print("============= Final Response =============")
    print(final_response)


if __name__ == "__main__":
    chaining_prompt_demo()
