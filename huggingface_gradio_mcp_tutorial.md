# Hugging Face Space + Gradio MCP 應用教學

## MCP 介紹

Model Context Protocol（MCP）是一套讓大型語言模型（LLM）透過標準化介面呼叫外部工具的協定。藉由設定 *MCP Server*，開發者可以將自定義函式轉換為 LLM 可以調用的工具【255889847180491†L158-L164】。Gradio 於 2025 年加入 MCP 支援後，只需幾行程式碼即可產生人類使用者的網頁介面與 MCP 伺服器，使函式既能在瀏覽器介面使用，也能被 LLM 以工具方式呼叫【255889847180491†L105-L145】。

## 安裝與準備

1. **安裝 Gradio MCP 版本**：透過 pip 安裝包含 MCP 支援的 Gradio。例如：
   ```bash
   pip install "gradio[mcp]"
   ```
2. **撰寫程式碼之前**，先確認本機或雲端環境可以存取 Python 以及必要的函式庫。
3. **選擇部署平臺**：本教學將程式推送至 Hugging Face Spaces，因此需要一個 Hugging Face 帳號。

## 建立簡易 MCP 伺服器（範例程式）

以下程式示範如何以 Gradio 建立 MCP 伺服器。本例為「字母計數器」：計算某一字母在輸入文字中出現的次數。程式同時產生人類使用者的介面與 MCP 伺服器【255889847180491†L105-L139】【893343144309553†L74-L108】。

```python
import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    計算 letter 在 word 中出現的次數。

    Args:
        word (str): 要搜尋的文字
        letter (str): 要計數的字元

    Returns:
        int: 出現次數
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

# 建立標準 Gradio 介面
app = gr.Interface(
    fn=letter_counter,
    inputs=["textbox", "textbox"],
    outputs="number",
    title="字母計數器",
    description="輸入文字與一個字母，計算該字母在文字中出現的次數"
)

# 啟動 Gradio 網頁介面與 MCP 伺服器
if __name__ == "__main__":
    app.launch(mcp_server=True)
```

程式中使用 `mcp_server=True` 啟動 MCP 伺服器【893343144309553†L106-L113】。啟動後，Gradio 會自動將 `letter_counter` 函式轉換為 MCP 工具，並在主控台顯示 MCP 伺服器的 URL【893343144309553†L108-L122】。使用者仍可透過瀏覽器操作介面，而 LLM 可以透過 `http://你的伺服器:port/gradio_api/mcp/sse` 對 MCP 伺服器發送 JSON‑RPC 訊息【893343144309553†L116-L120】。

### 背後運作原理

啟動 MCP 伺服器後，Gradio 會自動進行下列工作【255889847180491†L158-L164】：

1. **函式轉換** – 將每一個 Gradio 函式轉成 MCP 工具，並產生相應的名稱、描述與輸入/輸出結構。可在 `http://你的伺服器:port/gradio_api/mcp/schema` 查看工具與結構定義【255889847180491†L168-L170】。
2. **輸入/輸出對應** – 根據 `inputs` 和 `outputs` 定義生成工具參數與返回格式【255889847180491†L160-L163】。
3. **開啟 MCP 通訊** – Gradio 伺服器會開始監聽 MCP 訊息並透過 HTTP+SSE 提供 JSON‑RPC 通道【255889847180491†L158-L165】。
4. **檔案處理** – Gradio 會自動處理檔案與影像的 base64 編碼/解碼，並管理暫存檔案【255889847180491†L189-L194】。

## 在 Hugging Face Spaces 上部署 MCP 伺服器

部署流程如下：

1. **建立新 Space** – 登入 [Hugging Face Spaces](https://huggingface.co/spaces)，點選「Create new Space」，選擇 **Gradio** 作為 SDK，命名空間（例如 `letter-counter-mcp`）。
2. **準備檔案** – 將上述 Python 程式存成 `app.py`；建立 `requirements.txt`，內容包含:
   ```
   gradio[mcp]
   ```
3. **透過 Git 推送程式** – 在本地端執行以下指令，將程式推送至 Space 儲存庫【872688923069142†L209-L244】。
   ```bash
   git init
   git add app.py requirements.txt
   git commit -m "initial commit"
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/letter-counter-mcp
   git push -u origin main
   ```
   *註：建議使用 Hugging Face Access Token 作為密碼，以取代舊的帳號密碼驗證方式*。
4. **啟動與測試** – 部署完成後，Space 會自動啟動；訪問 Space 頁面即可看到 Gradio 介面。MCP 伺服器的端點通常為 `/gradio_api/mcp/sse`，可用於 LLM 工具呼叫【255889847180491†L146-L200】。

## 故障排除與建議

* **類型提示與文件字串**：為函式提供型別提示和完整的 docstring，並在 docstring 中使用 `Args:` 區塊說明參數，有助於生成正確的 MCP 工具描述【255889847180491†L205-L209】。
* **字串輸入**：若不確定輸入類型，建議將參數定義為 `str`，並在函式內進行型別轉換【255889847180491†L211-L213】。
* **SSE 相容性**：部分 MCP 客戶端尚不支援 SSE；可使用 Node.js 工具 `mcp-remote` 代理連線，並在 MCP 客戶端設定中指定 `command: "npx"` 及參數【255889847180491†L214-L229】。
* **使用 URL 傳送檔案**：MCP 客戶端對本地檔案處理有限，建議將輸入的檔案或圖片轉換為可公開存取的 URL【255889847180491†L189-L198】。

## 結論

Gradio 搭配 MCP 能快速將任何 Python 函式包裝成 LLM 可使用的工具，並透過 Hugging Face Spaces 提供免費託管的 MCP 伺服器。只要撰寫函式、建立 Gradio 介面並在 `launch` 時啟用 `mcp_server=True`，即可同時獲得視覺化網頁介面與 MCP 端點【893343144309553†L108-L122】。將程式部署到 Spaces 後，不僅方便使用者與 LLM 共享，亦可透過查看工具結構及端點，自行建立進階的代理或應用程式。
