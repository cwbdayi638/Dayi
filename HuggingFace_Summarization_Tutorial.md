# Hugging Face Transformers：文字摘要教學

本文介紹如何使用 [Hugging Face Transformers](https://huggingface.co/docs/transformers) 函式庫進行文字摘要（summarization）。我們將示範簡單的 Python 程式碼，說明如何呼叫 `pipeline` 介面載入預訓練模型，並產生文章的精簡摘要。

## 安裝與環境設定

1. **安裝 Python**：建議使用 Python 3.8 以上版本。
2. **安裝 Transformers 與相依套件**：在命令列執行：

   ```bash
   pip install transformers torch
   ```

   第一次使用 `pipeline` 下載模型時會自動從 Hugging Face 伺服器下載權重並快取，之後重複使用同一模型會直接讀取本地快取。

## 範例程式：文章摘要

以下程式檔名為 `huggingface_summarization_example.py`。程式碼使用 `summarization` 任務的 `pipeline` 來產生文章摘要，並搭配詳細註解幫助理解流程。

```python
"""
This script demonstrates how to perform text summarization using the Hugging Face
Transformers library. It uses a pipeline to load a pre‑trained summarization
model and apply it to an example article.
"""
from transformers import pipeline

def main() -> None:
    # 建立摘要管道（pipeline）。不指定模型時，預設會選用
    # DistilBART 或 BART 類型的預訓練模型。
    summarizer = pipeline("summarization")

    # 欲摘要的長文章，可自行更換為其他段落或新聞稿。
    article = (
        "Transformer models and large language models (LLMs) have revolutionized"
        " natural language processing by enabling machines to understand and"
        " generate human‑like text. One of the key capabilities of these models"
        " is summarization, which condenses long passages into concise and"
        " informative summaries. The Hugging Face Transformers library provides"
        " a simple `pipeline` interface that abstracts away the complexity of"
        " loading pre‑trained models and tokenizers. In this example we show"
        " how to perform summarization on a short article using the pipeline API."
    )

    # 產生摘要，可調整 max_length 與 min_length 來控制摘要長度。
    summary_output = summarizer(
        article,
        max_length=60,
        min_length=20,
        do_sample=False,
    )

    summary_text = summary_output[0]["summary_text"]
    print("Original text:\n")
    print(article)
    print("\nGenerated summary:\n")
    print(summary_text)

if __name__ == "__main__":
    main()
```

### 執行方法

在終端機中進入程式所在資料夾後，輸入以下指令執行：

```bash
python huggingface_summarization_example.py
```

程式將輸出原始文章與模型生成的摘要。您可以自行修改 `article` 字串替換成不同的內容，例如新聞報導、報告段落或課程筆記，觀察模型如何將長文凝縮為重點摘要。

### 自訂模型與參數

`pipeline("summarization")` 會自動選用預設模型，如果您想使用特定的模型（例如以中文資料訓練的摘要模型），可指定 `model` 與 `tokenizer` 參數：

```python
summarizer = pipeline(
    "summarization",
    model="IDEA-CCNL/YuyuanHL-RoBERTa-ext-sum",
    tokenizer="IDEA-CCNL/YuyuanHL-RoBERTa-ext-sum"
)
```

並可依需求調整 `max_length` 與 `min_length` 控制輸出摘要的字數範圍，`do_sample=False` 表示採用貪婪搜尋而非隨機抽樣產生摘要。

## 結論

透過 Hugging Face Transformers 的 `pipeline` 介面，實作文字摘要變得非常簡單，只需少量程式碼便能產生高品質的文章摘要。您可以根據不同語言或領域選擇合適的預訓練模型，或自行微調模型以達到最佳效果。歡迎嘗試將本教學應用在您的研究報告、會議紀錄或長篇文章上，提升閱讀效率。