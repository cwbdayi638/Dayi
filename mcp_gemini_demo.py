"""
示範如何使用 Google Gemini 模型結合 Gradio MCP 伺服器。

此腳本會：
1. 從環境變數（或 Colab 的 `userdata`）讀取 `GOOGLE_API_KEY`，並初始化 Gemini API。
2. 設定 MCP 伺服器 URL（在 Hugging Face Spaces 上部署的 Gradio MCP 伺服器）。
3. 定義一個轉接器函式 `call_mcp_letter_counter`，透過 `gradio_client` 呼叫遠端的 letter_counter 工具。
4. 宣告可供 Gemini 呼叫的工具，並建立 `GenerativeModel`。
5. 與使用者互動，當 Gemini 決定呼叫字母計數器工具時，會呼叫遠端 MCP 伺服器並將結果回傳給 Gemini。

執行前請確保安裝了以下套件，且設定了可用的 `GOOGLE_API_KEY`：

```bash
pip install google-generativeai gradio_client python-dotenv
```

在 Colab 環境中可以使用 `userdata.get('GOOGLE_API_KEY')` 讀取儲存的金鑰；
在其他環境請改用 `dotenv` 或 `os.environ`。腳本預設會嘗試兩者。
"""

import os
import google.generativeai as genai
from gradio_client import Client
from dotenv import load_dotenv

# 嘗試從 .env 檔案載入環境變數
load_dotenv()

# 優先從 Colab 的 userdata 讀取金鑰；若沒有則從環境變數讀取
try:
    from google.colab import userdata  # type: ignore
    api_key = userdata.get('GOOGLE_API_KEY')  # type: ignore
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError("請設定 GOOGLE_API_KEY 以使用 Gemini API")

# 初始化 Gemini 客戶端
genai.configure(api_key=api_key)

# 您部署在 Hugging Face 上的 MCP 伺服器 URL
MCP_SERVER_URL = "https://cwadayi-mcp-1.hf.space/"


def call_mcp_letter_counter(word: str, letter: str) -> int:
    """透過 gradio_client 呼叫遠端的 letter_counter 工具。"""
    try:
        print("--- 正在呼叫遠端 MCP 伺服器 ---")
        print(f"    伺服器: {MCP_SERVER_URL}")
        print(f"    參數: word='{word}', letter='{letter}'")

        client = Client(src=MCP_SERVER_URL)
        # 不指定 api_name，gradio_client 會自動尋找預設端點
        result = client.predict(word, letter)

        print(f"--- MCP 伺服器回傳結果: {result} ---")
        return int(result)
    except Exception as e:
        print(f"呼叫 MCP 伺服器失敗: {e}")
        return -1


# 宣告可供 Gemini 呼叫的工具
letter_counter_tool_declaration = {
    "name": "call_letter_counter_tool",
    "description": "計算一個指定的字母在一段文字中出現了幾次。",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "word": {"type": "STRING", "description": "要在其中搜尋的完整文字。"},
            "letter": {"type": "STRING", "description": "要計數的單一字元。"},
        },
        "required": ["word", "letter"],
    },
}


def main() -> None:
    """主執行函式：建立 Gemini 模型並開始對話。"""
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        tools=[letter_counter_tool_declaration],
    )

    print("你好！我是 Gemini，已經連接了您的字母計數器工具。您可以開始提問了。（輸入 'exit' 結束）")
    chat = model.start_chat(enable_automatic_function_calling=False)

    while True:
        prompt = input("您: ")
        if prompt.lower() == "exit":
            break

        response = chat.send_message(prompt)
        # 嘗試取得 Gemini 回傳的函式呼叫
        function_call = None
        try:
            function_call = response.candidates[0].content.parts[0].function_call
        except Exception:
            pass

        if function_call:
            print(f"--- Gemini 決定呼叫工具: {function_call.name} ---")
            if function_call.name == "call_letter_counter_tool":
                args = function_call.args
                tool_result = call_mcp_letter_counter(word=args["word"], letter=args["letter"])

                print("--- 將工具結果回傳給 Gemini，讓它產生最終回覆 ---")
                response = chat.send_message(
                    genai.protos.Part(
                        function_response={
                            "name": "call_letter_counter_tool",
                            "response": {"result": tool_result},
                        }
                    )
                )
                print(f"Gemini: {response.text}")
        else:
            print(f"Gemini: {response.text}")


if __name__ == "__main__":
    main()