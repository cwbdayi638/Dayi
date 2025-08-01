"""
This script demonstrates how to perform text summarization using the Hugging Face
Transformers library.  It leverages the built‑in ``pipeline`` API to load a
pre‑trained summarization model and tokenizer from the Hugging Face Hub and
applies it to an example article.  The default model chosen by the pipeline
for the ``summarization`` task is typically a variant of BART fine‑tuned on
the CNN/DailyMail dataset (e.g. ``sshleifer/distilbart-cnn-12-6``).  You can
replace it with any other summarization model by specifying the ``model`` and
``tokenizer`` parameters.

Steps in this script:

1. Import the ``pipeline`` function from the transformers library.
2. Instantiate a summarization pipeline.  The first call will download model
   weights and cache them locally if they are not already present.
3. Define a long piece of text to summarize.  You can experiment with any
   paragraph or article you like.  The model expects input under a certain
   token limit (around 1,024 tokens for the default model), so extremely
   long texts may need to be truncated or summarized in chunks.
4. Call the pipeline on the text with optional ``max_length`` and
   ``min_length`` arguments to control the length of the generated summary.
5. Print both the original text and the resulting summary.

Run this script from the command line::

    python huggingface_summarization_example.py

You should see a condensed summary of the input text printed to stdout.
"""

from transformers import pipeline


def main() -> None:
    """Run a summarization example using a Hugging Face pipeline."""
    # Create a summarization pipeline. Without specifying a model, this
    # defaults to a DistilBART or BART model fine‑tuned for summarization.
    summarizer = pipeline("summarization")

    # Long text to be summarized. You can replace this with any text; the
    # summarization model works best on news articles or formal documents.
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

    # Generate a summary.  The max_length and min_length arguments control
    # the length of the generated summary in tokens.  Adjust these values
    # depending on the desired level of detail.
    summary_output = summarizer(
        article,
        max_length=60,
        min_length=20,
        do_sample=False,
    )

    # The pipeline returns a list of dictionaries; extract the summary text.
    summary_text = summary_output[0]["summary_text"]

    # Print the original article and its summary.
    print("Original text:\n")
    print(article)
    print("\nGenerated summary:\n")
    print(summary_text)


if __name__ == "__main__":
    main()