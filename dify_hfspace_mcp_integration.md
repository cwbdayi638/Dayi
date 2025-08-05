# Dify 與 Hugging Face Space MCP 伺服器整合教學

## 前言

[Dify](https://dify.ai/) 是一個開源的 AI 應用平台，用戶可以透過「聊天機器人」或「工作流」來串接外部資料庫、模型與工具。自 2025 年 6 月起，Dify 對 **Model Context Protocol (MCP)** 有了兩種支援模式：

* **MCP Client**：在 Dify 應用內接入第三方 MCP 伺服器的工具，例如 Notion、Zapier 或 Hugging Face Space。使用者只需在管理介面加入 MCP 伺服器的 URL，Dify 便會自動發現可用工具、處理授權，並將工具加入代理人與工作流的節點選單【924566960771238†L168-L178】。
* **MCP Server**：將 Dify 自己的應用轉成 MCP 伺服器，讓外部系統（如 Claude Desktop 或 Cursor）可以呼叫 Dify 提供的工具【558075523798040†L124-L128】。若要將 Dify 變成 MCP 伺服器，可參考官方教學並啟用 MCP Server 模組【558075523798040†L137-L144】。

本文件聚焦第一種模式：**如何將 Hugging Face Space 上的 Gradio MCP 伺服器整合到 Dify**。這樣便能在 Dify 的代理人或工作流中調用由 Hugging Face 上部署的外部函式。

## 一、在 Hugging Face Space 建立 Gradio MCP 伺服器

若想在 Dify 使用外部工具，首先需要有一個符合 MCP 規範的伺服器。Gradio 自 2025 年起支援 MCP，只需在 `launch()` 時設定 `mcp_server=True` 便會同時啟動可視化介面與 MCP 伺服器【893343144309553†L108-L122】。以下示範如何建置「字母計數器」伺服器並部署至 Hugging Face Space：

1. **撰寫 `app.py`**：使用 Gradio 建立函式介面，並在啟動時開啟 MCP 服務。例如：

   ```python
   import gradio as gr

   def letter_counter(word: str, letter: str) -> int:
       """計算 letter 在 word 中出現的次數。"""
       return word.lower().count(letter.lower())

       
   app = gr.Interface(
       fn=letter_counter,
       inputs=["textbox", "textbox"],
       outputs="number",
       title="字母計數器",
       description="輸入文字與一個字母，計算該字母在文字中出現的次數"
   )

   if __name__ == "__main__":
       # 啟動網頁介面並同時開啟 MCP 伺服器
       app.launch(mcp_server=True)
   ```

   Gradio 會依據函式簽名與文件字串自動生成 MCP 工具描述與輸入/輸出結構【255889847180491†L158-L165】。啟動後可在終端機看到 MCP 伺服器的 URL，例如 `https://hf.space/yourslug/letter-counter-mcp/gradio_api/mcp`。

2. **建立 `requirements.txt`**：列出 `gradio[mcp]` 等必要套件。

3. **在 Hugging Face Spaces 建立新 Space**：選擇「Gradio」作為 SDK，將 `app.py` 和 `requirements.txt` 推送至該 Space。部署完成後，Space 頁面會提供互動式介面與 MCP API 端點【255889847180491†L146-L200】。

該 MCP 端點可供任何支援 MCP 的客戶端呼叫，包括 Dify、Claude Desktop、Cursor 等。

## 二、在 Dify 中註冊 Hugging Face MCP 伺服器

完成 MCP 伺服器部署後，需要將其加入 Dify，使工作流能調用這個字母計數工具。步驟如下：

1. **進入 MCP 伺服器管理介面**：在 Dify 工作區的左側選單點選 **Tools → MCP**，即可開啟 MCP 伺服器管理頁面【924566960771238†L144-L147】。

2. **新增 MCP 伺服器**：點選「Add MCP Server (HTTP)」。在彈出的表單中輸入：
   - **Server URL**：填入 Hugging Face Space 的 MCP 端點，例如 `https://hf.space/yourslug/letter-counter-mcp/gradio_api/mcp`【924566960771238†L152-L159】。
   - **Name & Icon**：自訂伺服器名稱（如「Letter Counter MCP」），可選擇圖示，便於在工具列表辨識【924566960771238†L156-L159】。
   - **Server Identifier**：指定一個唯一識別字串，例如 `hf_letter_counter`，僅能包含小寫字母、數字、底線或連字號，且最多 24 個字元【924566960771238†L158-L164】。

   伺服器識別符一旦建立便不可修改；若更改會導致既有代理人或工作流失效【924566960771238†L162-L164】。

3. **工具發現與授權**：提交後，Dify 會自動連線 MCP 伺服器來：
   1. 探索可用工具與功能【924566960771238†L168-L178】。
   2. 進行授權流程（若伺服器需要 OAuth 或其他驗證）【924566960771238†L168-L178】。
   3. 下載工具定義，並加入 Dify 的工具清單【924566960771238†L168-L178】。

   成功後，MCP 伺服器會以卡片方式顯示在列表中；點擊卡片可重新整理工具、重新授權或變更設定【924566960771238†L186-L194】。

4. **在應用中使用 MCP 工具**：當伺服器連線完成，它提供的工具會出現在代理人與工作流的工具選擇介面【924566960771238†L205-L223】。使用者可像使用內建工具一樣加入節點，例如在工作流中加入「hf_letter_counter » letter_counter」節點，並將參數繫結到變數或固定值。

5. **參數配置與自訂**：Dify 允許覆寫 MCP 工具的描述或預設參數。對於每個參數，可以選擇：
   - **Auto**：讓 AI 自行決定參數值；
   - **Fixed Value**：設置固定值，或綁定至工作流中的變數【924566960771238†L248-L259】。

   例如在字母計數範例中，可以固定 `letter` 參數為某個字母或由上游節點輸出；將 `word` 設為「Auto」，讓 AI 決定要計算哪串文字。

6. **工作流範例：** 使用者可參考附檔 `workflow-1.yml`，該檔代表一個 Dify 工作流，包含一個字串輸入節點與一個調用 MCP 工具 `MCP_1_letter_counter` 的節點。這個 MCP 工具在工作流中被命名為 `MCP_1_letter_counter`，並透過 `provider_name: gradio_MCP1` 指向外部 Gradio MCP 伺服器。輸入參數 `word` 來自上一節點的輸入字串，而 `letter` 在 YAML 中被設為固定值 `'h'`。使用者可依需求修改 YAML 或在可視化介面中配置參數。

## 三、實務建議

* **詳實描述工具與參數**：設計函式時，請為每個參數提供型別提示與文件字串，尤其是 `Args:` 區塊。清晰的描述有助於 Dify 生成精確的工具說明，使 AI 更容易正確調用【924566960771238†L241-L259】。
* **固定重要設定**：對於不希望 AI 調整的參數（如返回項數、模型版本等），可在 Dify 中將其設定為固定值【924566960771238†L248-L259】。
* **維持伺服器識別符與環境一致**：在不同環境間遷移或分享應用時，必須在目標環境中以相同的伺服器 ID 新增 MCP 伺服器，否則 YAML 配置中的引用會失效【924566960771238†L271-L276】。
* **注意延遲與錯誤處理**：MCP 協定僅負責傳輸層，若 Hugging Face Space 的函式執行時間較長，使用者可能感覺延遲。在設計 Gradio 應用時可考慮提供進度指示或將任務拆分成多步驟【558075523798040†L181-L191】。

## 結語

透過在 Hugging Face Space 部署 Gradio MCP 伺服器並在 Dify 中註冊，即可在工作流或代理人中使用自定義函式。這種整合方式不僅讓開發者擴充 Dify 工具庫，也讓 Hugging Face 的模型與程式能被自然語言代理人所調用。只需準備好 Space 程式碼、取得 MCP 伺服器 URL，並在 Dify 中完成設定，即可享受跨平台的協作與擴展能力。

## 進階：與 Gemini 模型結合

若希望透過 Google 的 Gemini 模型在本地端直接呼叫 Gradio MCP 工具，可以撰寫一個轉接程式將兩者串接起來。`mcp_gemini_demo.py` 為一個完整範例，它使用 `google-generativeai` 初始化 Gemini API，透過 `gradio_client` 呼叫部署於 Hugging Face Spaces 的 MCP 伺服器，再將結果回傳給模型。

重點步驟如下：

1. 先安裝必要套件並設定 `GOOGLE_API_KEY` 環境變數。
2. 使用 `gradio_client.Client(src=MCP_SERVER_URL)` 連線遠端 Gradio 應用，並呼叫 `predict(word, letter)` 執行 `letter_counter` 工具。
3. 將此函式包裝成 Gemini 的工具宣告，建立 `GenerativeModel` 時透過 `tools=[…]` 傳入。
4. 在對話過程中偵測 Gemini 是否要求呼叫此工具，若是則執行函式並把結果回傳給模型，讓它生成最終自然語言回覆。

完整程式碼請參考倉庫中的 [`mcp_gemini_demo.py`](./mcp_gemini_demo.py)。