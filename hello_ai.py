import os

from openai import OpenAI


def chat_with_ai() -> None:
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "DASHSCOPE_API_KEY is not set. Please configure it in your terminal first."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    model = os.getenv("DASHSCOPE_MODEL", "qwen-plus")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a student learning AI development. Reply in concise, "
                    "friendly Simplified Chinese."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Say hello to the world and mention that you are learning AI "
                    "API usage with Qwen."
                ),
            },
        ],
    )

    print(f"AI answer: {response.choices[0].message.content}")


if __name__ == "__main__":
    try:
        chat_with_ai()
    except Exception as exc:
        print(f"Request failed. Check your API key, model access, or network: {exc}")
