from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")
# model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")

# def legal_text_summarizer(input_text, min_length=400, max_length=1300):
#     input_text = input_text[:55000]  
#     input_tokenized = tokenizer(input_text, return_tensors='pt', truncation=True, padding="max_length", max_length=1024)

#     summary_ids = model.generate(
#         input_tokenized['input_ids'], 
#         num_beams=9,
#         no_repeat_ngram_size=3,
#         length_penalty=2.0,
#         min_length=min_length,
#         max_length=max_length,
#         early_stopping=True
#     )

#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    
#     return summary

import spacy
import nltk
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, pipeline

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

# Ensure you have the necessary NLTK data
nltk.download('punkt')

def legal_text_summarizer(input_text, min_len, max_len):
    model_name = 'nsi319/legal-pegasus'  

    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    summary_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)
    summary = summary_pipeline(input_text, max_length=max_len, min_length=min_len, truncation=True)

    return summary[0]['summary_text']


def short_summary(input_text):
    return legal_text_summarizer(input_text, 400, 600)

def medium_summary(input_text):
    return legal_text_summarizer(input_text, 850, 1000)

def long_summary(input_text):
    return legal_text_summarizer(input_text, 1200, 1500)

