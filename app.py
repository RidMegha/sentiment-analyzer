

'''

from flask import Flask, render_template, request
from sentiment.analyzer import analyze_sentiment
from database.mongo_handler import log_sentiment, get_all_reviews, get_sentiment_stats

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = None
    text = ''
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            sentiment = analyze_sentiment(text)  # must return list of 3 scores
            log_sentiment(text, sentiment)
    return render_template('index.html', sentiment=sentiment, text=text)

@app.route('/dashboard')
def dashboard():
    entries = get_all_reviews()
    sentiment_counts = get_sentiment_stats()

    latest_entry = entries[0] if entries else None
    latest_label = latest_entry.get("label", "") if latest_entry else ""
    latest_score = latest_entry.get("score", 0) if latest_entry else 0
    latest_all_scores = latest_entry.get("all_scores", []) if latest_entry else []

    return render_template(
        "dashboard.html",
        entries=entries,
        sentiment_counts=sentiment_counts,
        latest_label=latest_label,
        latest_score=latest_score,
        latest_all_scores=latest_all_scores
    )

if __name__ == '__main__':
    app.run(debug=True)

    '''

""""""

from flask import Flask, render_template, request, send_file, make_response, abort
from sentiment.analyzer import analyze_sentiment
from database.mongo_handler import log_sentiment, get_all_reviews, get_sentiment_stats, get_review_by_id

import csv
from io import StringIO, BytesIO
from bson import ObjectId
import pdfkit
# from utils.pdf_generator import generate_sentiment_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = None
    text = ''
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            sentiment = analyze_sentiment(text)
            log_sentiment(text, sentiment)
            # generate_sentiment_pdf(text, sentiment['label'], round(sentiment['score'], 2))
    return render_template('index.html', sentiment=sentiment, text=text)

@app.route('/download')
def download_pdf():
    return send_file("sentiment_report.pdf", as_attachment=True)

@app.route('/dashboard')
def dashboard():
    entries = get_all_reviews()
    sentiment_counts = get_sentiment_stats()
    latest_entry = entries[0] if entries else None
    latest_label = latest_entry["label"] if latest_entry else ""
    latest_score = latest_entry["score"] if latest_entry else 0
    latest_date = latest_entry["timestamp"].strftime('%Y-%m-%d') if latest_entry else ""

    return render_template(
        "dashboard.html",
        entries=entries,
        sentiment_counts=sentiment_counts,
        latest_label=latest_label,
        latest_score=latest_score,
        latest_date=latest_date
    )

# DISABLED - full table PDF export
@app.route('/export/pdf')
def export_pdf():
    return "Full table PDF export removed as requested.", 410

# KEEP - export single entry PDF
@app.route('/export/pdf/<entry_id>')
def export_single_pdf(entry_id):
    try:
        entry = get_review_by_id(ObjectId(entry_id))
        if not entry:
            abort(404)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Noto Sans', 'DejaVu Sans', sans-serif;
                    padding: 40px;
                    line-height: 1.6;
                }}
                h1 {{ color: #2c3e50; }}
                .label {{ font-size: 18px; color: #00695c; }}
                .confidence {{ color: #c62828; }}
                .input-text {{
                    background: #f9f9f9;
                    padding: 10px;
                    border: 1px solid #ccc;
                    margin-top: 10px;
                    font-size: 16px;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            <h1>📄 Sentiment Report</h1>
            <p class="label"><strong>Sentiment:</strong> {entry["label"]}</p>
            <p class="confidence"><strong>Confidence:</strong> {round(entry["score"] * 100, 2)}%</p>
            <p><strong>Original Text:</strong></p>
            <div class="input-text">{entry["text"]}</div>
        </body>
        </html>
        """

        pdf_bytes = pdfkit.from_string(html, False)

        return send_file(
            BytesIO(pdf_bytes),
            download_name=f"sentiment_entry_{entry_id}.pdf",
            as_attachment=True
        )
    except Exception as e:
        return f"PDF generation error: {e}", 500

@app.route('/export/csv')
def export_csv():
    entries = get_all_reviews()
    proxy = StringIO()
    writer = csv.writer(proxy)
    writer.writerow(["Text", "Sentiment", "Score", "Date"])
    for entry in entries:
        writer.writerow([
            entry["text"],
            entry["label"],
            round(entry["score"], 2),
            entry["timestamp"].strftime('%Y-%m-%d')  # Only date, no time
        ])
    response = make_response(proxy.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=sentiment_report.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

"""
if __name__ == '__main__':
    app.run(debug=True)
"""
if __name__ == '__main__':
    import os
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
