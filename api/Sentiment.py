from flask import Blueprint, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from models import db
from models.review import Review
from sqlalchemy import func

# Blueprint untuk API Sentiment Analysis
sentiment_bp = Blueprint('sentiment', __name__ , url_prefix='/api/sentiment')

# Load model dan tokenizer
model_path = 'D:\sentiment_analysis'
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

# Route untuk memproses sentiment analysis dan menyimpan review
@sentiment_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    review_text = data.get("text", "").strip()
    if not review_text:
        return jsonify({"error": "Review text is required"}), 400

    sentiment = predict_sentiment(review_text)

    # Simpan ke database
    new_review = Review(text=review_text, sentiment=sentiment)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({
        "id": new_review.id,
        "text": new_review.text,
        "sentiment": new_review.sentiment,
        "created_at": new_review.created_at.isoformat()
    }), 201

# Route untuk mendapatkan semua review
@sentiment_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    reviews_data = [
        {
            "id": review.id,
            "text": review.text,
            "sentiment": review.sentiment,
            "created_at": review.created_at.isoformat()
        }
        for review in reviews
    ]
    return jsonify(reviews_data), 200


@sentiment_bp.route('/sentiments', methods=['GET'])
def get_sentiment_data():
    sentiments = db.session.query(
        func.lower(Review.sentiment), db.func.count(Review.sentiment)
    ).group_by(func.lower(Review.sentiment)).all()

    # Debug log
    print("Sentiment Query Result:", sentiments)

    sentiment_data = {sentiment: count for sentiment, count in sentiments}
    sentiment_data = {
        "Positive": sentiment_data.get("positive", 0),
        "Negative": sentiment_data.get("negative", 0),
        "Neutral": sentiment_data.get("neutral", 0),
    }

    return jsonify(sentiment_data)
