import torch
from transformers import BertTokenizer, BertForSequenceClassification
from models import db
from models.review import Review

# Load model dan tokenizer
model_path = '"D:\sentiment_analysis"'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# Pastikan model berada di mode evaluasi
model.eval()

# Jika menggunakan GPU, pindahkan model ke GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Fungsi untuk prediksi sentiment
def predict_sentiment(text):
    # Tokenisasi input
    encodings = tokenizer(
        [text],
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )
    encodings = {key: val.to(device) for key, val in encodings.items()}

    # Prediksi dengan model
    with torch.no_grad():
        outputs = model(**encodings)
        prediction = torch.argmax(outputs.logits, dim=-1).item()

    # Mapping label prediksi
    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    return label_map.get(prediction, "unknown")

# Fungsi untuk menyimpan review ke database
def save_review_to_db(text, sentiment):
    new_review = Review(text=text, sentiment=sentiment)
    db.session.add(new_review)
    db.session.commit()
    return new_review

# Fungsi untuk mendapatkan semua review
def get_all_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return [
        {
            "id": review.id,
            "text": review.text,
            "sentiment": review.sentiment,
            "created_at": review.created_at.isoformat()
        }
        for review in reviews
    ]

# Fungsi untuk mendapatkan statistik sentimen
def get_sentiment_stats():
    sentiments = db.session.query(
        Review.sentiment, db.func.count(Review.sentiment)
    ).group_by(Review.sentiment).all()

    sentiment_data = {sentiment: count for sentiment, count in sentiments}

    return {
        "Positive": sentiment_data.get("Positive", 0),
        "Negative": sentiment_data.get("Negative", 0),
        "Neutral": sentiment_data.get("Neutral", 0),
    }
