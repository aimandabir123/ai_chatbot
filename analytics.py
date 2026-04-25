"""
analytics.py
Tracks messages, tool usage, sentiment, and feedback across sessions.
"""

import time
import datetime
from collections import defaultdict
from typing import Optional


class Analytics:

    def __init__(self):
        self._sessions: dict[str, dict] = {}
        self._g = {
            "total_messages":   0,
            "total_sessions":   0,
            "pos_feedback":     0,
            "neg_feedback":     0,
            "tool_counts":      defaultdict(int),
            "sentiment_scores": [],
            "hourly":           defaultdict(int),
        }
        self._start = time.time()

    def track(self, sid: str, user_msg: str, bot_msg: str,
              sentiment: dict, tools_used: list = None):
        now  = datetime.datetime.utcnow()
        hour = now.strftime("%Y-%m-%d %H:00")

        if sid not in self._sessions:
            self._sessions[sid] = {
                "messages":   [],
                "sentiments": [],
                "tools":      [],
            }
            self._g["total_sessions"] += 1

        s = self._sessions[sid]
        s["messages"].append({"user": user_msg, "bot": bot_msg})
        s["sentiments"].append(sentiment.get("score", 0.5))
        s["last_active"] = now.isoformat()

        self._g["total_messages"]      += 1
        self._g["sentiment_scores"].append(sentiment.get("score", 0.5))
        self._g["hourly"][hour]        += 1

        if tools_used:
            for t in tools_used:
                self._g["tool_counts"][t] += 1
            s["tools"].extend(tools_used)

    def record_feedback(self, sid: str, msg_id: str, rating: int):
        if rating > 0:
            self._g["pos_feedback"] += 1
        else:
            self._g["neg_feedback"] += 1

    def summary(self) -> dict:
        g      = self._g
        scores = g["sentiment_scores"]
        n      = len(scores) or 1
        total_fb = g["pos_feedback"] + g["neg_feedback"]
        sat      = round(g["pos_feedback"] / total_fb * 100, 1) if total_fb else None

        top_tools = sorted(
            g["tool_counts"].items(), key=lambda x: x[1], reverse=True
        )[:8]

        return {
            "overview": {
                "total_messages":  g["total_messages"],
                "total_sessions":  g["total_sessions"],
                "uptime_hours":    round((time.time() - self._start) / 3600, 2),
            },
            "feedback": {
                "positive":         g["pos_feedback"],
                "negative":         g["neg_feedback"],
                "satisfaction_pct": sat,
            },
            "sentiment": {
                "avg":     round(sum(scores) / n, 3) if scores else 0.5,
                "pos_pct": round(sum(1 for s in scores if s >= 0.65) / n * 100, 1),
                "neu_pct": round(sum(1 for s in scores if 0.35 <= s < 0.65) / n * 100, 1),
                "neg_pct": round(sum(1 for s in scores if s < 0.35) / n * 100, 1),
                "history": scores[-30:],
            },
            "top_tools": [{"tool": k, "count": v} for k, v in top_tools],
            "hourly":    dict(sorted(g["hourly"].items())[-12:]),
        }
