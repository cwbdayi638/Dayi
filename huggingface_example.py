"""
This script demonstrates how to use the Hugging Face transformers library to
perform sentiment analysis on a piece of text. It loads a pre‑trained model
and tokenizer via the convenient ``pipeline`` API and then uses this pipeline
to classify the sentiment of an example sentence. The script is written in a
self‑contained way so that you can run it directly after installing the
required dependencies (see the accompanying ``HuggingFace_Tutorial.md`` for
installation instructions).

Steps performed in this script:

1. Import the ``pipeline`` factory from ``transformers``.  The ``pipeline``
   function simplifies common use cases such as sentiment analysis,
   translation, summarization, etc.  Under the hood it automatically
   downloads the appropriate model weights and tokenizer the first time you
   call it (if they are not already cached locally).
2. Instantiate a sentiment analysis pipeline.  We do not specify a model
   name here; the transformers library will choose a reasonable default
   (currently ``distilbert-base-uncased-finetuned-sst-2-english``).  You can
   provide your own model name if you wish to customize the behaviour.
3. Define an example text for classification.  Feel free to change this to
   any sentence you would like to analyze.
4. Call the pipeline on the text to obtain predictions.  The result is a
   list of dictionaries, each containing a predicted label and a confidence
   score between 0 and 1.
5. Print the input text along with the predicted sentiment label and
   confidence.

To execute this script from the command line simply run::

    python huggingface_example.py

The output will show the sentiment classification for your example sentence.
"""

from transformers import pipeline


def main() -> None:
    """Entry point for the script.

    Creates a sentiment analysis pipeline and applies it to an example
    sentence. The results are printed to the console. If you would like to
    analyze multiple sentences, you can supply a list of strings to the
    pipeline instead of a single string; the API will return one result per
    input item.
    """
    # Create a pipeline for sentiment analysis.  When called without
    # arguments, this uses a default English sentiment classification model
    # (currently DistilBERT fine‑tuned on the SST‑2 dataset).  You can
    # override the model by passing a ``model`` keyword argument with the
    # identifier of a model from the Hugging Face hub.
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Example text to analyze.  You can replace this with any text you want
    # to classify.  The pipeline will return a list of results even for a
    # single sentence.
    example_text = "I love using the Hugging Face transformers library!"

    # Apply the pipeline to the text.  The result is a list of dictionaries
    # with keys 'label' (the predicted class) and 'score' (the confidence).
    results = sentiment_pipeline(example_text)

    # Unpack the first (and only) result.  For multiple inputs, iterate over
    # the results list.
    result = results[0]
    label = result["label"]
    score = result["score"]

    # Print the results.  We format the confidence score to four decimal
    # places for readability.
    print(f"Text: {example_text}")
    print(f"Predicted sentiment: {label}")
    print(f"Confidence: {score:.4f}")


if __name__ == "__main__":
    main()