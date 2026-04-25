"""
sentiment.py
Per-message sentiment analysis.
Uses TextBlob if installed, falls back to keyword scoring.
"""

NEGATIVE = [
    "not working", "broken", "frustrated", "angry", "terrible", "worst",
    "hate", "awful", "useless", "stuck", "error", "failed", "crash",
    "freeze", "disappointed", "horrible", "garbage", "defective",
    "damaged", "wrong", "cant", "cannot", "doesnt work", "wont", "bad",
    "not charging", "dead", "black screen",
]
POSITIVE = [
    "thank", "thanks", "great", "works", "fixed", "perfect", "amazing",
    "excellent", "love", "awesome", "resolved", "helpful", "fantastic",
    "happy", "pleased", "good", "nice", "clear", "easy", "smooth", "fast",
]
URGENT = [
    "urgent", "emergency", "asap", "immediately", "nothing works",
    "completely broken", "lost everything", "critical",
]


def analyze(text: str) -> dict:
    """Return sentiment dict: score (0-1), label, emoji, color, is_urgent."""
    tl = text.lower()

    try:
        from textblob import TextBlob
        score = (TextBlob(text).sentiment.polarity + 1.0) / 2.0
    except ImportError:
        pos   = sum(1 for w in POSITIVE if w in tl)
        neg   = sum(1 for w in NEGATIVE if w in tl)
        total = pos + neg
        score = (pos / total) if total else 0.5

    for w in NEGATIVE:
        if w in tl:
            score -= 0.10
    for w in POSITIVE:
        if w in tl:
            score += 0.10

    score = round(max(0.0, min(1.0, score)), 3)

    if score >= 0.65:
        label, emoji, color = "positive", "😊", "#30d158"
    elif score >= 0.35:
        label, emoji, color = "neutral",  "😐", "#ff9500"
    else:
        label, emoji, color = "negative", "😟", "#ff453a"

    return {
        "score":     score,
        "label":     label,
        "emoji":     emoji,
        "color":     color,
        "is_urgent": any(w in tl for w in URGENT),
    }
