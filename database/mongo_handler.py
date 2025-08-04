from pymongo import MongoClient
from datetime import datetime



# Replace with your actual MongoDB URI
MONGO_URI = "mongodb+srv://sentimentUser:<riju07@>@sentiment-cluster.jnadqaa.mongodb.net/?retryWrites=true&w=majority&appName=sentiment-cluster"
client = MongoClient(MONGO_URI)

# MongoDB setup (local or MongoDB Atlas)
# client = MongoClient("mongodb://localhost:27017")
db = client["sentiment_db"]
collection = db["reviews"]

# Log a new sentiment result
def log_sentiment(text, result):
    doc = {
        "text": text,
        "label": result["label"].upper(),  # Make sure label is consistent (POSITIVE, etc.)
        "score": round(result["score"], 4),
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)

# Alias for compatibility with app.py
insert_sentiment = log_sentiment

# Get stats for chart visualizations
def get_sentiment_stats():
    pipeline = [
        {"$group": {"_id": "$label", "count": {"$sum": 1}}}
    ]
    results = list(collection.aggregate(pipeline))

    # Convert to dict format: {"POSITIVE": 3, "NEGATIVE": 1, ...}
    counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for r in results:
        label = r["_id"].upper()
        counts[label] = r["count"]
    return counts

# Get all entries sorted by timestamp (for dashboard listing)
def get_all_reviews(limit=15):
    return list(collection.find().sort("timestamp", -1).limit(limit))

# Get latest entry
def get_latest_entry():
    return collection.find_one(sort=[("timestamp", -1)])

# Get entry by ID
def get_review_by_id(entry_id):
    return collection.find_one({"_id": entry_id})

# Alias for compatibility with app.py (used in dashboard listing)
get_latest_sentiments = get_all_reviews





"""
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup (local or MongoDB Atlas)
client = MongoClient("mongodb://localhost:27017")
db = client["sentiment_db"]
collection = db["reviews"]

# Log a new sentiment result
def log_sentiment(text, result):
    doc = {
        "text": text,
        "label": result["label"].upper(),  # Make sure label is consistent (POSITIVE, etc.)
        "score": round(result["score"], 4),
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)

# Get stats for chart visualizations
def get_sentiment_stats():
    pipeline = [
        {"$group": {"_id": "$label", "count": {"$sum": 1}}}
    ]
    results = list(collection.aggregate(pipeline))

    # Convert to dict format: {"POSITIVE": 3, "NEGATIVE": 1, ...}
    counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for r in results:
        label = r["_id"].upper()
        counts[label] = r["count"]
    return counts

# Get all entries sorted by timestamp (for dashboard listing)
def get_all_reviews(limit=15):
    return list(collection.find().sort("timestamp", -1).limit(limit))

#get latest entry
def get_latest_entry():
    return collection.find_one(sort=[("timestamp", -1)])

def get_review_by_id(entry_id):
    return collection.find_one({"_id": entry_id})


"""