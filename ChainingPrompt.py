import os
import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 从 .env 文件中加载 OPENAI_API_KEY
if not load_dotenv(find_dotenv()):
    print("无法加载 .env 文件。")

# 创建 OpenAI API 客户端
client = OpenAI(
        api_key=os.getenv("SILICONFLOW_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://api.siliconflow.cn/v1",  # 填写DashScope SDK的base_url
    )


# 从 OpenAI API 获取 LLM 生成的结果
def get_completion_from_messages(messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0, max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

# 定义函数，查找用户输入中可能存在的产品名称和类别
def find_products_and_category(user_input: str) -> str:
    delimiter = "######"
    system_message = f"""
    你将收到客户服务查询，客户服务查询将使用 {delimiter} 字符串分隔。
    你需要输出 JSON 对象的 Python 列表，每个对象包含以下字段：
    - "category": <计算机和笔记本电脑，智能手机和配件，电视和家庭影院系统，游戏机和配件，音响设备，相机和摄像机 中的一个>
    - "products": <必须在下面允许的产品中找到的产品列表>
    仅输出JSON对象列表内容，不要输出字符串和JSON标识(```json)。
    
    其中，类别和产品必须在客户服务查询中找到。
    如果用户提到了某个产品，则必须将其与下面的允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。

    请根据用户查询中提到的产品名称和类别，列出所有与之相关的产品。
    同时，你不能假设产品名称中包含关于价格、质量或其他特征的任何信息（名称包含的产品类别除外）。

    允许的产品以 JSON 格式提供。
    允许的产品列表：
    {{
        "计算机和笔记本电脑": ["TechPro Ultrabook", "BlueWave 游戏笔记本", 
            "PowerLite 可翻转笔记本", "TechPro 台式机", "BlueWave Chromebook"],
        "智能手机和配件": ["SmartX Pro 手机", "MobiTech 电源壳",
            "SmartX Mini 手机", "MobiTech 无线充电器", "SmartX EarBuds"],
        "电视和家庭影院系统": ["CineView 4K 电视", "SoundMax 家庭影院",
        "CineView 8K 电视", "SoundMax 音响", "CineView OLED 电视"],
        "游戏机和配件": ["GameSphere X", "ProGamer 手柄",
            "GameSphere Y", "ProGamer 赛车方向盘", "GameSphere VR 头显"],
        "音响设备": ["AudioPhonic 降噪耳机", "WaveSound 蓝牙音箱",
            "AudioPhonic 真无线耳机", "WaveSound 音响", "AudioPhonic 唱盘"],
        "相机和摄像机": ["FotoSnap 单反相机", "ActionCam 4K 相机",
            "FotoSnap 微单相机", "ZoomMaster 摄像机", "FotoSnap 拍立得相机"]
    }}
    """
    
    product_names =  get_completion_from_messages(messages=[
        { "role": "system", "content": system_message },
        { "role": "user", "content": f"{delimiter} {user_input} {delimiter}" },
    ])
    return product_names

# 产品列表
products = {
    "TechPro Ultrabook":{
        "name": "TechPro Ultrabook",
        "category": "计算机和笔记本电脑",
        "brand": "TechPro",
        "model_number": "TP-UB100",
        "warranty": "1年",
        "rating": 4.5,
        "features": ["13.3英寸显示屏", "8GB内存", "256GB固态硬盘", "英特尔酷睿i5处理器"],
        "description": "一款时尚轻巧的超级本，适用于日常使用。",
        "price": 799.99,
    },
    "BlueWave 游戏笔记本电脑": {
        "name": "BlueWave 游戏笔记本电脑",
        "category": "计算机和笔记本电脑",
        "brand": "BlueWave",
        "model_number": "BW-GL200",
        "warranty": "2年",
        "rating": 4.7,
        "features": ["15.6英寸显示屏", "16GB内存", "512GB固态硬盘", "NVIDIA GeForce RTX 3060"],
        "description": "一款高性能的游戏笔记本电脑，提供沉浸式体验。",
        "price": 1199.99
    },
    "BlueWave Chromebook": {
        "name": "BlueWave Chromebook",
        "category": "计算机和笔记本电脑",
        "brand": "BlueWave",
        "model_number": "BW-CB100",
        "warranty": "1年",
        "rating": 4.1,
        "features": ["11.6英寸显示屏", "4GB内存", "32GB eMMC", "Chrome 操作系统"],
        "description": "一款紧凑且价格实惠的Chromebook，适用于日常任务。",
        "price": 249.99
    },
    "SmartX Pro 手机": {
        "name": "SmartX Pro 手机",
        "category": "智能手机和配件",
        "brand": "SmartX",
        "model_number": "SX-PP10",
        "warranty": "1年",
        "rating": 4.6,
        "features": ["6.1英寸显示屏", "128GB存储", "1200万像素双摄像头", "5G"],
        "description": "一款功能强大的智能手机，具备先进的摄像功能。",
        "price": 899.99
    },
    "MobiTech 电源壳": {
        "name": "MobiTech 电源壳",
        "category": "智能手机和配件",
        "brand": "MobiTech",
        "model_number": "MT-PC20",
        "warranty": "1年",
        "rating": 4.3,
        "features": ["5000mAh电池", "无线充电", "兼容 SmartX ProPhone"],
        "description": "一款具备内置电池的保护壳，可延长使用时间。",
        "price": 59.99
    },
    "SoundMax 音响": {
        "name": "SoundMax 音响",
        "category": "电视和家庭影院系统",
        "brand": "SoundMax",
        "model_number": "SM-SB50",
        "warranty": "1年保修",
        "rating": 4.3,
        "features": ["2.1声道", "300瓦输出", "无线低音炮", "蓝牙"],
        "description": "通过这款时尚而强大的声音系统提升您的电视音质。",
        "price": 199.99
    },
    "CineView 4K 电视": {
        "name": "CineView 4K 电视",
        "category": "电视和家庭影院系统",
        "brand": "CineView",
        "model_number": "CV-4K55",
        "warranty": "2年",
        "rating": 4.8,
        "features": ["55英寸显示屏", "4K分辨率", "HDR", "智能电视"],
        "description": "一台具有鲜艳色彩和智能功能的出色4K电视。",
        "price": 599.99
    },
    "SoundMax 家庭影院": {
        "name": "SoundMax 家庭影院",
        "category": "电视和家庭影院系统",
        "brand": "SoundMax",
        "model_number": "SM-HT100",
        "warranty": "1年",
        "rating": 4.4,
        "features": ["5.1声道", "1000W输出", "无线低音炮", "蓝牙"],
        "description": "一套强大的家庭影院系统，为您带来身临其境的音频体验。",
        "price": 399.99
    },
    "CineView 8K 电视": {
        "name": "CineView 8K 电视",
        "category": "电视和家庭影院系统",
        "brand": "CineView",
        "model_number": "CV-8K65",
        "warranty": "2年",
        "rating": 4.9,
        "features": ["65英寸显示屏", "8K分辨率", "HDR", "智能电视"],
        "description": "用这款令人惊艳的8K电视体验电视的未来。",
        "price": 2999.99
    },
    "CineView OLED 电视": {
        "name": "CineView OLED电视",
        "category": "电视和家庭影院系统",
        "brand": "CineView",
        "model_number": "CV-OLED55",
        "warranty": "2年保修",
        "rating": 4.7,
        "features": ["55英寸屏幕", "4K分辨率", "HDR", "智能电视"],
        "description": "用这款OLED电视体验真正的深黑和鲜艳的色彩。",
        "price": 1499.99
    },
    "GameSphere X": {
        "name": "GameSphere X",
        "category": "游戏机和配件",
        "brand": "GameSphere",
        "model_number": "GS-X",
        "warranty": "1年保修",
        "rating": 4.9,
        "features": ["4K游戏", "1TB存储", "向后兼容", "在线多人游戏"],
        "description": "一款面向极致游戏体验的下一代游戏机。",
        "price": 499.99
    },
    "ProGamer手柄": {
        "name": "ProGamer手柄",
        "category": "游戏机和配件",
        "brand": "ProGamer",
        "model_number": "PG-C100",
        "warranty": "1年保修",
        "rating": 4.2,
        "features": ["人体工程学设计", "可定制按钮", "无线", "可充电电池"],
        "description": "高品质的游戏手柄，提供精准和舒适的操作。",
        "price": 59.99
    },
    "GameSphere Y": {
        "name": "GameSphere Y",
        "category": "游戏机和配件",
        "brand": "GameSphere",
        "model_number": "GS-Y",
        "warranty": "1年保修",
        "rating": 4.8,
        "features": ["4K游戏", "500GB存储", "向后兼容", "在线多人游戏"],
        "description": "一款性能强大的紧凑型游戏机。",
        "price": 399.99
    },
    "FotoSnap 单反相机": {
        "name": "FotoSnap 单反相机",
        "category": "相机和摄像机",
        "brand": "FotoSnap",
        "model_number": "FS-DSLR200",
        "warranty": "1年保修",
        "rating": 4.7,
        "features": ["2420万像素传感器", "1080p视频", "3英寸液晶屏", "可更换镜头"],
        "description": "用这款多功能单反相机捕捉令人惊叹的照片和视频。",
        "price": 599.99
    },
    "ActionCam 4K": {
        "name": "ActionCam 4K",
        "category": "相机和摄像机",
        "brand": "ActionCam",
        "model_number": "AC-4K",
        "warranty": "1年保修",
        "rating": 4.4,
        "features": ["4K视频", "防水", "图像稳定", "Wi-Fi"],
        "description": "使用这款坚固而紧凑的4K动作摄像机记录您的冒险旅程。",
        "price": 299.99
    },
}

# 根据产品名称，查询产品列表中的产品详细信息
def get_product_by_name(name):
    return products[name]

# 根据产品类别，查询产品列表中的产品详细信息
def get_product_by_category(category):
    return [
        product for product in products.values() 
        if product['category'] == category
    ]


# 从提取的产品名称列表中，获取产品详细信息
def get_products_string(products_response: str):
    try:
        data_list = json.loads(products_response)
    except Exception as e:
        print("读取产品列表失败，请检查输出是否正确。")
        print(e)
        data_list = []
    
    products_string = ""

    if len(data_list) == 0:
        return products_string
    
    for data in data_list:
        try:
            if 'products' in data:
                for product_name in data["products"]:
                    product = get_product_by_name(product_name)
                    if product:
                        products_string += json.dumps(product, ensure_ascii=False, indent=4) + "\n"
                    else:
                        print(f'Error: Product {product_name} not found.')
            elif 'category' in data:
                category_name = data["category"]
                products = get_product_by_category(category_name)
                if products:
                    products_string += json.dumps(products, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Error: {e}')
    
    return products_string


# 生成最终的回复
def get_final_response(user_input:str,product_detail: str) -> str:
    delimiter = "######"
    system_message = f"""\
    你是电商平台的智能客服，请以友好并乐于助人的态度回复，\
    并使用简洁的方式回答问题，确保向用户提出相关的后续问题。\
    """
    final_response = get_completion_from_messages(messages=[
        { "role": "system", "content": system_message },
        { "role": "user", "content": f"{delimiter} {user_input} {delimiter}" },
        { "role": "system", "content": f"以下是系统查询得到的相关产品信息：\n{product_detail}" },
    ])
    print("get_final_response:---------------------\n",final_response) 
    return final_response

def chaining_Prompt_demo():
    # 用户输入的内容
    user_input = "请告诉我关于 SmartX Pro 手机和 FotoSnap 相机，单反那款。另外，也介绍一下你们的电视。"
    # user_input = "我的路由器坏了"
    
    # 查找用户输入中可能存在的产品名称和类别
    product_names = find_products_and_category(user_input)
    print(product_names)
    print("已输出产品名称和类别=================================")
    
    # 查询产品信息，输出JSON字符串
    product_detail = get_products_string(product_names)
    print(product_detail)
    print("已输出产品消息信息=================================")
    
    # 生成最终的回复
    get_final_response(user_input,product_detail)
chaining_Prompt_demo()
