import openai

# 配置千问 API
# 注意：base_url 必须指向阿里云的兼容地址
client = openai.OpenAI(
    api_key="xxxxxxxx", 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 保持昨天的 Prompt 逻辑不变
SYSTEM_PROMPT = """
你是一位居住在资深软件工程师导师（Senior Dev Mentor）。
1. 你的语言风格是中英夹杂，语气要像在茶餐厅聊天一样地道（例如使用：Start-up, Bug, Deploy, 搞掂, 唔该）。
2. 你会对学生提交的代码进行严格 Code Review。
3. 如果代码写得好，你会赞赏；如果写得烂，你会直接指出问题，并给出具体的 Refactor 建议。
"""

def ask_qwen_mentor(user_code):
    try:
        response = client.chat.completions.create(
            model="qwen3.5-flash",  # 这里可以换成 qwen-plus 或 qwen-turbo
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"请点评以下 Python 代码：\n\n{user_code}"}
            ]
        )
        # 打印导师的点评
        print("--- 导师 Qwen 的回复 ---")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"发生错误：{e}")

# 还是这段初级代码
test_code = """
def my_func(list):
    res = []
    for i in list:
        if i % 2 == 0:
            res.append(i)
    return res
"""

ask_qwen_mentor(test_code)