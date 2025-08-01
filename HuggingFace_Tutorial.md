# 使用 Hugging Face Transformers 的簡易教學

本文件示範如何在 Python 中使用 [Hugging Face Transformers](https://huggingface.co/docs/transformers) 函式庫完成基本的文字情感分析。教學包含安裝步驟、範例程式碼說明以及如何更換模型。只要具備基礎的 Python 使用經驗，即可依照本文快速上手。

## 環境準備與安裝

1. **安裝 Python**：建議使用 Python 3.8 或以上版本。
2. **安裝依賴**：在終端機輸入以下指令安裝 Hugging Face Transformers 以及 PyTorch（Transformers 依賴 PyTorch 或 TensorFlow，若您習慣 TensorFlow 亦可將 `torch` 替換為 `tensorflow`）：

   ```bash
   pip install transformers torch
   ```

   第一次載入模型時會自動從 Hugging Face 伺服器下載權重檔並快取到本地端，後續使用會直接從快取載入。

## 範例程式：情感分析

以下程式碼檔案名為 `huggingface_example.py`，內含詳細註解，可直接執行以體驗 Hugging Face 的簡易用法。

```python
"""
This script demonstrates how to use the Hugging Face transformers library to
perform sentiment analysis on a piece of text. It loads a pre‑trained model
and tokenizer via the convenient ``pipeline`` API and then uses this pipeline
to classify the sentiment of an example sentence.
"""
from transformers import pipeline

def main() -> None:
    # 建立一個情感分析管道（pipeline）。如果不指定模型名稱，
    # Transformers 會自動選用預訓練好的 DistilBERT 模型。
    sentiment_pipeline = pipeline("sentiment-analysis")

    # 定義要分析的句子
    example_text = "I love using the Hugging Face transformers library!"

    # 執行情感分析；回傳值為結果的列表，每個元素包含
    # 'label'（預測的情感類別）與 'score'（信心水準）
    results = sentiment_pipeline(example_text)
    result = results[0]

    print(f"Text: {example_text}")
    print(f"Predicted sentiment: {result['label']}")
    print(f"Confidence: {result['score']:.4f}")

if __name__ == "__main__":
    main()
```

### 執行程式

在終端機中進入程式所在資料夾後，執行：

```bash
python huggingface_example.py
```

若一切順利，終端機會顯示分析文字及對應的情感結果，例如：

```
Text: I love using the Hugging Face transformers library!
Predicted sentiment: POSITIVE
Confidence: 0.9999
```

### 更換模型

使用 `pipeline` 時可以透過 `model` 參數替換成其他公開模型。例如，如果想使用以中文資料訓練的模型，可從 Hugging Face Hub 找到該模型名稱，例如 `ckiplab/bert-base-chinese`，並修改程式：

```python
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ckiplab/bert-base-chinese",
    tokenizer="ckiplab/bert-base-chinese"
)
```

多數模型文檔會標明適用語言與任務，選擇合適的模型可以提升分析效果。請注意不同模型可能需要安裝額外依賴，如 TensorFlow 或特定版本的 PyTorch。

## 除了情感分析，你還可以…

Hugging Face Transformers 不僅支援情感分析，還提供多種任務的管道，包括：

- **文本生成** (`text-generation`)：用於產生文章或對話。
- **翻譯** (`translation`)：支援多國語言翻譯。
- **摘要** (`summarization`)：自動整理長文摘要。
- **問答** (`question-answering`)：根據提供的段落回答問題。
- **零樣本分類** (`zero-shot-classification`)：無需微調即可進行情感或主題分類。

使用方式與本範例類似，只需將 `pipeline` 的任務名稱改為相對應的字串即可。

## 總結

本文示範了如何安裝並使用 Hugging Face Transformers 做簡易的情感分析。透過 `pipeline`，使用者可以在幾行程式碼內完成複雜的自然語言處理任務。欲深入學習其他功能與進階應用，可參考官方文件或社群提供的範例。祝你在 AI 的旅程中玩得愉快！