from transformers import PegasusTokenizer, PegasusForConditionalGeneration, pipeline
import re
import spacy

from nltk.tokenize import sent_tokenize

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Ensure you have the necessary NLTK data
import nltk
nltk.download('punkt')
def summarise_pegasus(input_text):
    model_name = 'google/pegasus-large'

    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    summary_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)
    summary = summary_pipeline(input_text, max_length=300, min_length=50, truncation=True)

    return summary[0]['summary_text']


def preprocess_text(text):
    """
    Preprocess the text for the PEGASUS summarization model, focusing on handling named entities
    and intelligent chunking for terms and conditions simplification. Named entities are preserved
    in their original form, and the output is a single string of text suitable for summarization.

    Args:
    text (str): The input text to preprocess.

    Returns:
    str: The preprocessed text ready for the PEGASUS model.
    """

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Decode HTML entities (e.g., '&amp;' to '&')
    text = re.sub(r'&[a-z]+;', '', text)

    # Temporarily replace named entities with placeholders to avoid splitting them
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        placeholder = f"__{ent.label_}__"
        entities[placeholder] = ent.text
        text = text.replace(ent.text, placeholder)

    # Remove special characters, keeping alphabets, common punctuation, and placeholders for entities
    text = re.sub(r'[^a-zA-Z.,;!?\'"__\s]', ' ', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    # Split the text into sentences and rejoin to ensure proper sentence boundaries
    sentences = sent_tokenize(text)
    text = ' '.join(sentences)

    # Restore named entities in the text by replacing placeholders with original entities
    for placeholder, original in entities.items():
        text = text.replace(placeholder, original)

    return text
