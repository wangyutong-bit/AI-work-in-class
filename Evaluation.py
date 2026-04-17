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
def get_completion_from_messages(messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0.8, max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content



# 方法 1： 人工评估 LLM 生成的结果

# 测试用户输入样本
customer_query_1 = "我的预算不够，能买哪一台电视？"
customer_query_2 = "我需要给我的智能手机充电。"
customer_query_3 = "最便宜的音响是哪款？"
customer_query_4 = "请告诉我关于 SmartX Pro 手机和 FotoSnap 相机，单反那款。另外，也介绍一下你们的电视。"

# 第一版 系统提示
def find_products_and_category_v1(user_input):
    delimiter = "######"
    system_message = f"""
    你将收到客户服务查询，客户服务查询将使用 {delimiter} 字符串分隔。
    输出一个 JSON 对象的 Python 列表，每个对象包含以下字段：
    - "category": <计算机和笔记本电脑，智能手机和配件，电视和家庭影院系统，游戏机和配件，音响设备，相机和摄像机 中的一个>
    - "products": <必须在下面允许的产品中找到的产品列表>

    其中，类别和产品必须在客户服务查询中找到。
    如果用户提到了某个产品，则必须将其与下面的允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。

    允许的产品以 JSON 格式提供。每个项目的键是产品类别，值是该类别中允许的产品列表。
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

    return get_completion_from_messages(messages=[
        { "role": "system", "content": system_message },
        { "role": "user", "content": f"{delimiter} {user_input} {delimiter}" },
    ])

# 分别测试 4 个用户输入样本
def test_find_products_and_category_v1():
    print("第一版系统提示的测试结果：=========================")
    products_response_1 = find_products_and_category_v1(customer_query_1)
    print("products_response_1:----------------------")
    print(products_response_1)


    products_response_2 = find_products_and_category_v1(customer_query_2)
    print("products_response_2:----------------------")
    print(products_response_2)


    products_response_3 = find_products_and_category_v1(customer_query_3)
    print("products_response_3:----------------------")
    print(products_response_3)


    products_response_4 = find_products_and_category_v1(customer_query_4)
    print("products_response_4:----------------------")
    print(products_response_4)
# test_find_products_and_category_v1()

# 第二版 系统提示
# 额外添加提示信息，以及少量示例样本
def find_products_and_category_v2(user_input):
    delimiter = "######"
    system_message = f"""
    你将收到客户服务查询，客户服务查询将使用 {delimiter} 字符串分隔。
    你需要输出 JSON 对象的 Python 列表，每个对象包含以下字段：
    - "category": <计算机和笔记本电脑，智能手机和配件，电视和家庭影院系统，游戏机和配件，音响设备，相机和摄像机 中的一个>
    - "products": <必须在下面允许的产品中找到的产品列表>
    请勿输出任何不属于 JSON 格式要求之外的任何字符。
    同时，在输出请求的 JSON 后，不要编写任何解释性文本。

    其中，类别和产品必须在客户服务查询中找到。
    如果用户提到了某个产品，则必须将其与下面的允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。

    请根据用户查询中提到的产品名称和类别，列出所有与之相关的产品。
    同时，你不能假设产品名称中包含关于价格、质量或其他特征的任何信息（名称包含的产品类别除外）。

    允许的产品以 JSON 格式提供。每个项目的键是产品类别，值是该类别中允许的产品列表。
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
    
    # 示例样本
    few_shot_user_1 = "我想要最贵的电脑，你有什么推荐？"
    few_shot_assistant_1 = """[{"category": "计算机和笔记本电脑", "products": ["TechPro Ultrabook", "BlueWave 游戏笔记本", "PowerLite 可翻转笔记本", "TechPro 台式机", "BlueWave Chromebook"]"""
    
    return get_completion_from_messages(messages=[
        { "role": "system", "content": system_message },
        { "role": "user", "content": f"{delimiter} {few_shot_user_1} {delimiter}" },
        { "role": "assistant", "content": few_shot_assistant_1 },
        { "role": "user", "content": f"{delimiter} {user_input} {delimiter}" },
    ])


# 修改实现后，重新测试 4 个用户输入样本
def test_find_products_and_category_v2():
    print("第二版系统提示+示例的测试结果：=========================")
    products_response_1 = find_products_and_category_v2(customer_query_1)
    print("products_response_1:----------------------")
    print(products_response_1)


    products_response_2 = find_products_and_category_v2(customer_query_2)
    print("products_response_2:----------------------")
    print(products_response_2)


    products_response_3 = find_products_and_category_v2(customer_query_3)
    print("products_response_3:----------------------")
    print(products_response_3)


    products_response_4 = find_products_and_category_v2(customer_query_4)
    print("products_response_4:----------------------")
    print(products_response_4)
# test_find_products_and_category_v2()

# 方法二： 引入量化指标，评估 LLM 生成的结果

# 测试用户输入样本集合，包括用户输入和期望的输出
query_samples = [
    { # query 1
        "customer_query": """我的预算不够，能买哪一台电视？""",
        "ideal_answer": {
            "电视和家庭影院系统": set([
                "CineView 4K 电视",
                "SoundMax 家庭影院",
                "CineView 8K 电视",
                "SoundMax 音响",
                "CineView OLED 电视"
            ])
        }
    },
    { # query 2
        "customer_query": """我需要给我的智能手机充电。""",
        "ideal_answer": {
            "智能手机和配件": set([
                "MobiTech 电源壳", 
                "MobiTech 无线充电器"
            ])
        }
    },
    { # query 3
        "customer_query": """最便宜的音响是哪款？""",
        "ideal_answer": {
            "音响设备": set([
                "AudioPhonic 降噪耳机",
                "WaveSound 蓝牙音箱",
                "AudioPhonic 真无线耳机",
                "WaveSound 音响",
                "AudioPhonic 唱盘"
            ])
        }
    },
    { # query 4
        "customer_query": """请告诉我关于 SmartX Pro 手机和 FotoSnap 相机，单反那款。另外，也介绍一下你们的电视。""",
        "ideal_answer": {
            "智能手机和配件": set(["SmartX Pro 手机"]),
            "相机和摄像机": set(["FotoSnap 单反相机"]),
            "电视和家庭影院系统": set([
                "CineView 4K 电视",
                "SoundMax 家庭影院",
                "CineView 8K 电视",
                "SoundMax 音响",
                "CineView OLED 电视"
            ])
        }
    },
    { # query 5
        "customer_query": """请告诉我关于 CineView 电视，8K 版本的，Gamesphere 游戏机，X 版的那款。我现在的预算不够，能买哪一款电脑呢？""",
        "ideal_answer": {
            "电视和家庭影院系统": set(["CineView 8K 电视"]),
            "游戏机和配件": set(["GameSphere X"]),
            "计算机和笔记本电脑": set([
                "TechPro Ultrabook",
                "BlueWave 游戏笔记本",
                "PowerLite 可翻转笔记本",
                "TechPro 台式机",
                "BlueWave Chromebook"
            ])
        }
    },
    { # query 6
        "customer_query": """我想和朋友一起玩赛车游戏，那台游戏机比较好？""",
        "ideal_answer": {
            "游戏机和配件": set([
                "GameSphere X",
                "ProGamer 手柄",
                "GameSphere Y",
                "ProGamer 赛车方向盘",
                "GameSphere VR 头显"
            ])
        }
    },
    { # query 7
        "customer_query": """我应该给我的摄影师朋友什么礼物最好？""",
        "ideal_answer": {
            "相机和摄像机": set([
                "FotoSnap 单反相机",
                "ActionCam 4K 相机",
                "FotoSnap 微单相机",
                "ZoomMaster 摄像机",
                "FotoSnap 拍立得相机"
            ])
        }
    },
    { # query 8
        "customer_query": """我想要一台时光机。""",
        "ideal_answer": {}
    }
]

class PN:
    category: str
    products: list[str]

# 计算输出结果的准确度（量化指标）
def eval_response(response: str, ideal_answer: dict[str, set[str]]) -> float:
    # 清理响应字符串，移除 Markdown 代码块标记
    response = response.strip()
    if response.startswith("```"):
        # 找到第一个换行符
        first_newline = response.find("\n")
        if first_newline != -1:
            # 找到结束的 ```
            end_block = response.rfind("```")
            if end_block > first_newline:
                # 提取代码块内容
                response = response[first_newline:end_block].strip()
    
    # 将 LLM 生成的结果转换为 Python 字典对象
    try:
        product_names: list[PN] | PN = json.loads(response.replace("'", '"'))
    except json.JSONDecodeError:
        print(f"JSON 解析错误，响应内容: {response}")
        return 0.0  # 解析失败返回 0 分

    # 防止 product_names 是一个单独的对象，而不是一个列表
    if isinstance(product_names, dict):
        product_names = [product_names]

    # 如果 LLM 生成的结果为空，即没有产品或类别
    if len(product_names) == 0:
        # 如果期望结果中也没有产品或类别，则返回 1.0，否则返回 0.0
        return 1.0 if len(ideal_answer) == 0 else 0.0
    
    correct_products = 0
    total_products = 0

    for category_product in product_names:
        category = category_product.get("category", "")
        product = set(category_product.get("products", []))

        ideal_product = ideal_answer.get(category, set())

        # 计算 ideal_product 和 product 的交集的大小
        correct_products += len(ideal_product & product)
        total_products += len(ideal_product)
    
    # 如果期望结果中没有产品或类别，则返回 1.0
    if total_products == 0:
        return 1.0
    
    # 输出结果与期望结果中相同的产品名称的数量除以期望结果中产品名称的数量
    return correct_products / total_products

# 遍历所有测试样本，计算 LLM 生成的结果的准确度
def test_eval_response():
    # 累计总分
    score_sum_v1 = 0
    score_sum_v2 = 0
    # 遍历输入样本，计算总分
    for index, query in enumerate(query_samples):
        print(f"==== QUERY {index} ====")
        customer_query = query['customer_query']
        ideal_answer = query['ideal_answer']
        print(f"用户输入: {customer_query}")
        print(f"期望输出: {ideal_answer}")
        response_v1 = find_products_and_category_v1(customer_query)
        print(f"响应 v1: {response_v1}")
        response_v2 = find_products_and_category_v2(customer_query)
        print(f"响应 v2: {response_v2}")
        eval_response_v1_score = eval_response(response_v1, ideal_answer)
        print(f"响应 v1评估得分: {eval_response_v1_score}")
        
        eval_response_v2_score = eval_response(response_v2, ideal_answer)
        print(f"响应 v2评估得分: {eval_response_v2_score}")
        
        score_sum_v1 += eval_response_v1_score
        score_sum_v2 += eval_response_v2_score

    # 计算平均准确度分数
    score_avg_v1 = score_sum_v1 / len(query_samples)
    score_avg_v2 = score_sum_v2 / len(query_samples)
    print(f"修改前的平均分: {score_avg_v1}")
    print(f"修改后的平均分: {score_avg_v2}")
test_eval_response()