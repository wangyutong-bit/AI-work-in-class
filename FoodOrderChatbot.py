import os
import tkinter as tk

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


class FoodOrderChatbotClient:
    def __init__(self, debug=False):
        self.debug = debug
        self.client = client
        self.context = [self.generate_system_message("""
            你是订餐机器人，为披萨餐厅自动收集订单信息。
            
            你要首先问候顾客。然后等待用户回复收集订单信息。收集完信息需确认顾客是否还需要添加其他内容。
            最后需要询问是否自取或外送，如果是外送，你要询问地址（没有外送费）。
            最后告诉顾客订单总金额，并送上祝福。

            请确保明确所有选项、附加项和尺寸，以便从菜单中识别出该项唯一的内容。
            你的回应应该以简短、非常随意和友好的风格呈现。

            菜单包括（单位为元(人民币)）：

            菜品：
            意式辣香肠披萨（大、中、小） 12.95、10.00、7.00
            芝士披萨（大、中、小） 10.95、9.25、6.50
            茄子披萨（大、中、小） 11.95、9.75、6.75
            薯条（大、小） 4.50、3.50
            希腊沙拉 7.25

            配料：
            奶酪 2.00
            蘑菇 1.50
            香肠 3.00
            加拿大熏肉 3.50
            AI酱 1.50
            辣椒 1.00

            饮料：
            可乐（大、中、小） 3.00、2.00、1.00
            雪碧（大、中、小） 3.00、2.00、1.00
            瓶装水 5.00
        """)]
    
    # 构造用户消息对象
    def generate_user_message(self, user_input):
        return {"role": "user", "content": user_input}
    
    # 构造系统消息对象
    def generate_system_message(self, system_output):
        return {"role": "system", "content": system_output}
    
    # 构造助手消息对象
    def generate_assistant_message(self, assistant_output):
        return {"role": "assistant", "content": assistant_output}
    
    # 从 OpenAI API 获取 LLM 生成的结果
    def get_completion_from_messages(self, messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature, # 控制模型输出的随机程度
        )
        return response.choices[0].message.content
    
    # 用户与 LLM 进行交流，完成点单的交流过程
    def chat(self, user_input):
        # Step 1: 依据用户输入文本，生成用户消息
        user_message = self.generate_user_message(user_input)
        if self.debug: 
            print(f"用户消息：{user_message}")
            print("--------------------------")
        # Step 2: 将用户消息加入上下文
        self.context.append(user_message)
        # Step 3: 请求 LLM 生成回复
        if self.debug: 
            print(f"上下文：{self.context}")
            print("--------------------------")
        response = self.get_completion_from_messages(self.context)        
        # Step 4: 依据回复生成助理消息
        assistant_message = self.generate_assistant_message(response)
        if self.debug: 
            print(f"客服回复：{assistant_message}")
            print("--------------------------")
        # Step 5: 将助理消息加入上下文
        self.context.append(assistant_message)
        # Step 6: 返回助理消息
        return assistant_message
    
    # 实现结账的流程
    def checkout(self):
        # Step 1: 创建临时上下文
        temp_context = self.context.copy()
        if self.debug: 
            print(f"用户消息：用户申请结账。")
            print("--------------------------")
        # Step 2: 创建临时系统消息
        temp_system_message = self.generate_system_message("\创建上一个食品订单的 json 摘要。逐项列出每件商品的价格，注意不要漏项。\
            字段应该是：1) 披萨，包括大小 2) 配料列表 3) 饮料列表，包括大小 4) 配菜列表，包括大小 5) 总价")
        # Step 3: 将临时系统消息加入临时上下文
        temp_context.append(temp_system_message)
        temp_context.append(self.generate_user_message("我需要结账，一共多少钱。"))
        if self.debug: 
            print(f"上下文：{temp_context}")
            print("--------------------------")
        # Step 4: 请求 LLM 生成回复
        response = self.get_completion_from_messages(temp_context)
        # Step 5: 依据回复生成助理消息
        assistant_message = self.generate_assistant_message(response)
        if self.debug: 
            print(f"客服回复：{assistant_message}")
            print("--------------------------")
        # Step 6: 将助理消息加入临时上下文
        temp_context.append(assistant_message)
        # Step 7: 返回助理消息
        return assistant_message


class FoodOrderChatbot:
    # chatbot_client 是点餐机器人的业务逻辑类
    def __init__(self, root: tk.Tk, chatbot_client: FoodOrderChatbotClient):
        self.client = chatbot_client
        self.root = root
        self.root.title("食物点餐机器人")
        # self.root.geometry("600x600")
        self.root.geometry("720x480")
        # 创建用户输入区域
        self.input_frame = tk.Frame(self.root, padx=10, pady=10)
        self.input_frame.pack(fill=tk.X)
        # 创建文本输入区域
        self.text_input = tk.Entry(self.input_frame)
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        # 创建聊天按钮
        self.button_chat = tk.Button(self.input_frame, text="聊天", command=lambda: self.on_button_chat_click())
        self.button_chat.pack(side=tk.RIGHT)
        # 创建聊天区域
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # 创建聊天文本框，用于显示聊天消息
        self.chat_text = tk.Text(self.chat_frame)
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        # 创建底部结账区域
        self.checkout_frame = tk.Frame(self.root)
        self.checkout_frame.pack(fill=tk.X, padx=10, pady=10)
        # 创建结账按钮
        self.button_checkout = tk.Button(self.checkout_frame, text="结账", command=lambda: self.on_button_checkout_click())
        self.button_checkout.pack(side=tk.RIGHT)
        # 焦点转移至用户输入框
        self.text_input.focus()
    
    # 在聊天文本框中展示用户输入和 LLM 的输出结果
    def update_chat(self, message):
        if message["role"] == "user":
            self.chat_text.insert(tk.END, f"用户：{message['content']}\n")
        elif message["role"] == "assistant":
            self.chat_text.insert(tk.END, f"机器人：{message['content']}\n")

    # “聊天”按钮点击事件的响应函数
    def on_button_chat_click(self):
        # Step 1: 获取用户输入
        user_input = self.text_input.get()
        # Step 2: 将用户输入更新到聊天面板
        self.update_chat(self.client.generate_user_message(user_input))
        # Step 3: 使用 ChatbotClient 聊天
        response = self.client.chat(user_input)
        # Step 4: 更新聊天面板
        self.update_chat(response)
        # Step 5: 清空文本输入框
        self.text_input.delete(0, tk.END)
        self.text_input.focus()
    
    # “结账”按钮点击事件的响应函数
    def on_button_checkout_click(self):
        # Step 1: 使用 ChatbotClient 结账
        response = self.client.checkout()
        # Step 2: 更新聊天面板
        self.update_chat(response)
        # Step 3: 清空文本输入框
        self.text_input.delete(0, tk.END)
        self.text_input.focus()


# 创建点餐机器人客户端
root = tk.Tk()
chatbot_client = FoodOrderChatbotClient(debug=True)
chatbot = FoodOrderChatbot(root, chatbot_client)
root.mainloop()
