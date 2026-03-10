"""
Score Label Utility
Provides human-readable labels, emojis, and colors for 0-100 scores.
Used by agents, match score service, and the API layer.
"""
from typing import Dict, Any


# Score tier definitions (ordered high to low)
SCORE_TIERS = [
    {"min": 90, "max": 100, "label": "Excellent",      "emoji": "🟢", "color": "#10b981", "grade": "A+"},
    {"min": 75, "max": 89,  "label": "Good",            "emoji": "🟡", "color": "#22d3ee", "grade": "A"},
    {"min": 60, "max": 74,  "label": "Average",         "emoji": "🟠", "color": "#f59e0b", "grade": "B"},
    {"min": 40, "max": 59,  "label": "Below Average",   "emoji": "🔴", "color": "#f97316", "grade": "C"},
    {"min": 0,  "max": 39,  "label": "Poor",            "emoji": "⛔", "color": "#ef4444", "grade": "D"},
]


def get_score_label(score: int) -> Dict[str, Any]:
    """
    Returns a dict with human-readable label info for a 0-100 score.
    
    Example:
        get_score_label(85)
        # {'score': 85, 'label': 'Good', 'emoji': '🟡', 'color': '#22d3ee', 'grade': 'A'}
    """
    score = max(0, min(100, int(score)))
    
    for tier in SCORE_TIERS:
        if tier["min"] <= score <= tier["max"]:
            return {
                "score": score,
                "label": tier["label"],
                "emoji": tier["emoji"],
                "color": tier["color"],
                "grade": tier["grade"],
            }
    
    # Fallback (should never happen)
    return {
        "score": score,
        "label": "Unknown",
        "emoji": "❓",
        "color": "#9ca3af",
        "grade": "?",
    }


def get_label_text(score: int) -> str:
    """Shorthand: returns just the label string, e.g. 'Good'."""
    return get_score_label(score)["label"]


def get_grade(score: int) -> str:
    """Shorthand: returns just the grade string, e.g. 'A+'."""
    return get_score_label(score)["grade"]
