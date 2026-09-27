# TnCSimplifier: Decipher & Decide

**Summarises Terms & Conditions and privacy policies into plain, short, multilingual summaries.**

CSE508 Information Retrieval, Group 27, IIIT Delhi

📽️ **Project walkthrough (Canva):** https://canva.link/nd5sg7wociijmc1
Start with the presentation to get the big picture, then use this README to find your way around the code.

---

## The problem

Most people click "I agree" without reading privacy policies. The documents are long and full of
legal jargon, so users grant camera, microphone, contacts or location access without knowing how that
data will be used. **Decipher & Decide** closes this gap. You paste a policy (or upload a screenshot
of one) and get back a concise summary in the length and language you choose, so you can decide
whether to accept.

## What it does

| Feature | How |
|---|---|
| **Summarise policy text** | Abstractive summarisation with **Legal-PEGASUS** (`nsi319/legal-pegasus`), a PEGASUS model fine-tuned on legal text |
| **Image input (OCR)** | Upload a PNG/JPG/GIF screenshot; text is extracted with **Tesseract** (`pytesseract`) |
| **Adjustable length** | Small / Medium / Long summaries (≈400–600, 850–1000, 1200–1500 tokens) |
| **Multilingual output** | Summaries are translated into 100+ languages with `deep-translator` (Google Translate) |
| **Policy database** | MySQL database of **49 popular apps** (WhatsApp, Instagram, Spotify, Zomato, Uber, GPay, …) with full policy text, the permissions each app requests and why, and a feature→app mapping |
| **Q&A chatbot (prototype)** | `chatbot.py` answers questions such as *"Does WhatsApp use my camera?"* with Google Gemini |

## How it works

```
 ┌──────────────┐   text    ┌───────────────┐   ┌──────────────────────┐   ┌──────────────┐
 │  Web UI      │──────────▶│ Pre-processing │──▶│ Legal-PEGASUS        │──▶│ Translation  │──▶ Summary
 │ (Flask)      │   image   │ URLs/HTML strip│   │ summariser (S/M/L)   │   │ (optional)   │
 │              │──▶ OCR ──▶│ NER-safe clean │   └──────────────────────┘   └──────────────┘
 └──────────────┘ Tesseract └───────────────┘
```

**Pre-processing** (`27_MidtermReview1/ir 2/your_script.py`) removes URLs, HTML tags and entities.
It protects named entities with spaCy placeholders so they aren't split, strips special characters, and
re-segments sentences with NLTK before the text reaches the model.

## Project timeline

| Stage | What was done | Where |
|---|---|---|
| **Baseline** | Built the dataset and database. Compared 5 summarisers (3 × T5 variants, BART, PEGASUS) by cosine similarity; PEGASUS won | `27_baseline.pdf`, `Data/` |
| **Mid-term** | Summarised every policy with `google/pegasus-large` and stored the results in a `generated_data_pegasus` table. Added pre-processing and a first Flask prototype | `27_MidtermReview1/`, `midterm_evaluation.ipynb` |
| **Final** | Switched to domain-specific **Legal-PEGASUS**. Added OCR, summary-length control, translation, a redesigned UI and the Gemini chatbot | `mobby_update/`, `IR_final_database.ipynb`, `final_evaluation.ipynb` |

## Results

The generated summaries were scored against the original policy text of all 49 apps.

| Metric | Mid-term (`pegasus-large`) | Final (`legal-pegasus`) |
|---|---:|---:|
| TF-IDF cosine similarity | 0.37 | **0.75** |
| ROUGE-1 F | 0.09 | **0.27** |
| ROUGE-2 F | 0.04 | **0.17** |
| ROUGE-L F | 0.09 | **0.27** |
| BERTScore precision | **0.873** | 0.868 |
| BERTScore recall | 0.804 | **0.856** |
| BERTScore F1 | 0.837 | **0.862** |

The legal-domain model keeps much more of the policy's content: recall-driven metrics roughly triple.
Precision stays high, so the summaries remain faithful to the source.

## Repository structure

```
.
├── mobby_update/mobby_update/mobby/     ★ FINAL web application (run this)
│   ├── app.py                           Flask server: routes, file upload, pipeline glue
│   ├── summarise.py                     Legal-PEGASUS summariser (small / medium / long)
│   ├── ocr_code.py                      Tesseract OCR for image input
│   ├── language.py                      Translation via deep-translator
│   ├── templates/                       index.html (landing), page1.html (summariser)
│   └── static/assets/                   CSS/JS/images (Mobirise-based front end)
│
├── chatbot.py                           Gemini-powered Q&A prototype
│
├── Data/                                MySQL dump (database `IR_policy`)
│   ├── App_data.sql                     apps_data: App_Id, Type_, App_Name, Privacy_policy, ISPaid
│   ├── Permission_Mapping.sql           app → permission (Camera, Microphone, SMS, …) + how it is used
│   └── Feature_Mapping.sql              app → feature (send messages, food delivery, …)
│
├── IR_final_database.ipynb              Generates Legal-PEGASUS summaries for every app and stores them in the DB
├── midterm_evaluation.ipynb             Cosine / ROUGE / BERTScore for the PEGASUS-large summaries
├── final_evaluation.ipynb               Same metrics for the final Legal-PEGASUS summaries
│
├── 27_MidtermReview1/                   Mid-term submission
│   ├── 27_Midterm1.pdf                  Mid-term report
│   ├── IR_midterm (1).ipynb             PEGASUS-large summarisation + pre-processing
│   ├── Generated_data.csv               Generated summaries (appid, summary)
│   └── ir 2/                            First Flask prototype (text in → summary out)
│
├── front_end_IR/mobi/                   Static HTML/CSS export of the front end
└── 27_baseline.pdf                      Baseline report: problem statement, literature survey, model comparison
```

## Running the web app

**1. Install system dependency:** Tesseract OCR.

```bash
brew install tesseract            # macOS
sudo apt install tesseract-ocr    # Ubuntu/Debian
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
```

**2. Install Python packages** (Python 3.10 recommended):

```bash
pip install flask flask-cors werkzeug transformers torch sentencepiece \
            spacy nltk pytesseract pillow deep-translator google-generativeai
python -m spacy download en_core_web_sm
```

**3. Start the server:**

```bash
cd mobby_update/mobby_update/mobby
python3 app.py
```

Open http://127.0.0.1:5000, click through to the summariser, then paste text or upload an image.
Pick a summary length and language, and submit. The first request downloads the Legal-PEGASUS
weights (~2 GB) from Hugging Face, so it takes a while.

> `ocr_code.py` sets the temp directory to `C:\Temp` (the app was developed on Windows).
> On macOS/Linux, change that line or remove it.

## Rebuilding the database and evaluation (optional)

```bash
mysql -u root -p < Data/App_data.sql
mysql -u root -p IR_policy < Data/Permission_Mapping.sql
mysql -u root -p IR_policy < Data/Feature_Mapping.sql
pip install mysql-connector-python rouge bert-score scikit-learn
```

Update the connection details (`host`, `user`, `password`) at the top of the notebooks. Then run
`IR_final_database.ipynb` to generate summaries and `final_evaluation.ipynb` to score them.

## Chatbot

```bash
export GOOGLE_API_KEY="your-key"
python chatbot.py
```

`chatbot.py` needs a Google Gemini API key. Read it from an environment variable rather than
hard-coding it in the source.

## Team

| | |
|---|---|
| Devansh Goswami | devansh21460@iiitd.ac.in |
| Ritisha Singh | ritisha21089@iiitd.ac.in |
| Samanyu Kamra | samanyu21487@iiitd.ac.in |
| Shriya Verma | shriya21490@iiitd.ac.in |

## References

1. T. Perera and T. Perera, "Barrister: Processing and Summarization of Terms & Conditions / Privacy Policies," I2CT, 2021.
2. G. Erkan and D. Radev, "LexRank: Graph-based Lexical Centrality as Salience in Text Summarization," JAIR, 2004.
3. A. Ghimire, R. Shrestha and J. Edwards, "Too Legal; Didn't Read (TLDR): Summarization of Court Opinions," IETC, 2023.
4. J. Zhang, Y. Zhao, M. Saleh and P. J. Liu, "PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization," ICML, 2020.
5. M. Keymanesh, M. Elsner and S. Parthasarathy, "Toward Domain-Guided Controllable Summarization of Privacy Policies," 2020.
6. S. Dalal, A. Singhal and B. Lall, "LexRank and PEGASUS Transformer for Summarization of Legal Documents."
