from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")
model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")

def legal_text_summarizer(input_text, min_length=400, max_length=1300):
    """
    Summarizes legal texts using a pre-trained model. The function allows specifying the minimum and maximum lengths
    for the summary.

    Parameters:
        input_text (str): The legal document text to be summarized.
        min_length (int): Minimum length of the summary in terms of the number of tokens.
        max_length (int): Maximum length of the summary in terms of the number of tokens.

    Returns:
        str: The generated summary of the input text.
    """
    input_text = input_text[:55000]  
    input_tokenized = tokenizer(input_text, return_tensors='pt', truncation=True, padding="max_length", max_length=1024)

    summary_ids = model.generate(
        input_tokenized['input_ids'], 
        num_beams=9,
        no_repeat_ngram_size=3,
        length_penalty=2.0,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    
    return summary


def short_summary(input_text):
    return legal_text_summarizer(input_text, 400, 600)

def medium_summary(input_text):
    return legal_text_summarizer(input_text, 850, 1000)

def long_summary(input_text):
    return legal_text_summarizer(input_text, 1200, 1500)

