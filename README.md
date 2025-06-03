
# 📰 News Summarizer, Aggregator & Fake News Detector

A full-stack web application that helps users:

- ✂️ **Summarize** lengthy news articles using NLP.
- 🌐 **Aggregate** news from multiple sources for wide coverage.
- 🧪 **Detect fake news** using a fine-tuned RoBERTa machine learning model.

Built with a **Python Flask** backend and **React (TypeScript)** frontend, integrating state-of-the-art NLP and ML models for a seamless user experience.

---

## 🚀 Features

- **Text Summarization**  
  → Condenses long news articles into concise summaries using extractive NLP techniques.

- **News Aggregation**  
  → Fetches real-time news from various APIs and RSS feeds, storing them locally for efficient access.

- **Fake News Detection**  
  → Utilizes a fine-tuned **RoBERTa model** to classify news articles as real or fake with high accuracy.

- **Modern UI**  
  → Built with React + Tailwind CSS for a responsive, user-friendly experience.

---

## 🛠️ Tech Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Frontend  | React, TypeScript, Tailwind CSS                 |
| Backend   | Python, Flask, Flask-SQLAlchemy, Flask-Migrate |
| ML/NLP    | RoBERTa (HuggingFace), NLTK, pandas, numpy      |
| Summarizer | Sumy, Cosine Similarity                        |
| Scheduler | APScheduler                                     |
| Database  | SQLite                                          |
| Others    | dotenv, logging, feedparser                     |

---

---

## ⚙️ Installation Guide

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/KartikAmbupe/Mini-Project-Sem-VI.git
cd Mini-Project-Sem-VI
```

### 🔧 2. Backend Setup

```bash
pip install -r requirements.txt
flask db upgrade
flask run
```

### 🔧 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Open in Browser

- Frontend: [http://localhost:5173](http://localhost:5173)  
- Backend API: [http://localhost:5000](http://localhost:5000)

---

## 🧠 Machine Learning & NLP

### 🔍 Summarization

- **Type**: Extractive
- **Libraries**: `sumy` (LexRank), `NLTK`, `Scikit-learn`
- **Method**: Cosine similarity and sentence ranking

### ⚠️ Fake News Detection

- **Model**: Fine-tuned **RoBERTa-base**
- **Library**: `transformers` (HuggingFace)
- **Approach**: Binary classification (Real vs Fake)
- **Preprocessing**: Text cleaning, RoBERTa tokenizer
- **Training Data**: LIAR dataset, FakeNewsNet, Kaggle open-source datasets

### 📅 News Aggregation

- Uses `APScheduler` to run background jobs via `fetcher.py`
- Sources: NewsAPI, RSS feeds
- Storage: Local database (SQLite)

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/ceba5ad8-eb2e-4151-9101-9b1ff2f3c9b4)

![image](https://github.com/user-attachments/assets/357d233e-968d-4808-8ec6-2d32cbc8913e)

![image](https://github.com/user-attachments/assets/fbe48c0f-5146-49c9-82da-d0783dfb5207)

![image](https://github.com/user-attachments/assets/0ece49be-d0ad-488f-bc4f-03a843a8c7aa)


---

## 🙏 Acknowledgements

- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [NLTK](https://www.nltk.org/)
- [Sumy](https://github.com/miso-belica/sumy)
- [NewsAPI](https://newsapi.org/)
- [Tailwind UI](https://tailwindcss.com/)
- [Kaggle Datasets](https://www.kaggle.com/)

---

## 📌 Future Enhancements

- Add support for **abstractive summarization** using BART or T5
- Integrate **multilingual support**
- Enable **user authentication** for saved articles and feedback
- Add **interactive charts** for news trends and sources

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ by Kartik Ambupe, Neha Gade & Jiya Trivedi
