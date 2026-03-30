import json
import os

import openai


client = openai.OpenAI(
    api_key="输入你的 API Key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def multiply_numbers(a: int, b: int) -> int:
    print(f">>> [调用工具] 执行乘法: {a} * {b}")
    return a * b

def add_numbers(a: int, b: int) -> int:
    print(f">>> [调用工具] 执行加法: {a} + {b}")
    return a + b


tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "当需要计算两个整数的和时，使用这个工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个加数"},
                    "b": {"type": "integer", "description": "第二个加数"},
                },
                "required": ["a", "b"],
            },
        },
        
    }
]


tools2 = [
    {
        "type": "function",
        "function": {
            "name": "multiply_numbers",
            "description": "当需要计算两个整数的积时，使用这个工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个乘数"},
                    "b": {"type": "integer", "description": "第二个乘数"},
                },
                "required": ["a", "b"],
            },
        },
        
    }
]


def explain_api_error(exc: Exception) -> str:
    if isinstance(exc, openai.BadRequestError):
        try:
            error_body = exc.response.json()
        except Exception:
            error_body = None

        error = (error_body or {}).get("error", {})
        code = error.get("code")
        message = error.get("message", str(exc))

        if code == "Arrearage":
            return (
                "接口请求失败：当前阿里云 DashScope 账户处于欠费或不可用状态。\n"
                "这不是代码逻辑错误，而是账户状态拦住了请求。\n"
                "处理方式：登录阿里云百炼 / DashScope 控制台，检查余额、套餐、账单状态和 API Key 所属账号。"
            )

        return f"接口请求失败：{message}"

    return f"调用模型时发生异常：{exc}"


def run_agent(user_query: str) -> None:
    if not client.api_key:
        print("未检测到 API Key。请先设置环境变量 DASHSCOPE_API_KEY。")
        return

    messages = [{"role": "user", "content": user_query}]

    try:
        response = client.chat.completions.create(
            model="qwen3.5-flash",
            messages=messages,
            tools=tools,
        )
    except Exception as exc:
        print(explain_api_error(exc))
        return

    try:
        response = client.chat.completions.create(
            model="qwen3.5-flash",
            messages=messages,
            tools=tools2,
        )
    except Exception as exc:
        print(explain_api_error(exc))
        return

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            if function_name == "add_numbers":
                args = json.loads(tool_call.function.arguments)
                result = add_numbers(args.get("a"), args.get("b"))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                )

        try:
            final_response = client.chat.completions.create(
                model="qwen-max",
                messages=messages,
            )
        except Exception as exc:
            print(explain_api_error(exc))
            return

        print("AI 最终回答:", final_response.choices[0].message.content)
    else:
        print("AI 直接回答:", response_message.content)


run_agent("嘿，导师！帮我算下 98765 乘以 54321 等于多少？")
