import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from google import genai


class Settings(BaseSettings):
    GOOGLE_GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


SYSTEM_PROMPT = """你是一個 Windows 命令列助手。使用者會在 Windows Terminal 中用非常簡短的方式問問題，請你回答可以直接在 Windows cmd.exe 執行的指令。

規則：
- 只回答純文字單行指令
- 不要使用 JSON、Markdown 或任何格式化
- 不要加上任何解釋或註解
- 不要使用 PowerShell 或 bash 專屬語法，只能用 cmd.exe 相容的指令
- 如果指令包含使用者需要替換的部分，用明顯的佔位符如 input.mp4、output.mp4 等"""


def main():
    if len(sys.argv) < 2:
        print("Usage: ai <your question>")
        sys.exit(1)

    user_message = " ".join(sys.argv[1:])
    
    settings = Settings()
    client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    
    print(response.text.strip())


if __name__ == "__main__":
    main()
