from __future__ import annotations

from dataclasses import dataclass


def triangular(value: float, left: float, peak: float, right: float) -> float:
    if value <= left or value >= right:
        return 0.0
    if value == peak:
        return 1.0
    if value < peak:
        return (value - left) / (peak - left)
    return (right - value) / (right - peak)


def left_shoulder(value: float, left: float, right: float) -> float:
    if value <= left:
        return 1.0
    if value >= right:
        return 0.0
    return (right - value) / (right - left)


def right_shoulder(value: float, left: float, right: float) -> float:
    if value <= left:
        return 0.0
    if value >= right:
        return 1.0
    return (value - left) / (right - left)


@dataclass
class RecommendationInput:
    math_interest: float
    programming_interest: float
    time_availability: float
    career_clarity: float


def _clamp(value: float) -> float:
    return max(0.0, min(10.0, value))


def fuzzify_score(value: float) -> dict[str, float]:
    score = _clamp(value)
    return {
        "low": left_shoulder(score, 2.5, 5.0),
        "medium": triangular(score, 3.0, 5.0, 7.0),
        "high": right_shoulder(score, 5.5, 8.0),
    }


def _difficulty_label(score: float) -> str:
    if score < 4.0:
        return "Beginner"
    if score < 7.0:
        return "Intermediate"
    return "Advanced"


def _suitability_label(score: float) -> str:
    if score < 4.5:
        return "Explore More"
    if score < 7.5:
        return "Good Fit"
    return "Excellent Fit"


def recommend_course(user_input: RecommendationInput) -> dict[str, object]:
    math_sets = fuzzify_score(user_input.math_interest)
    programming_sets = fuzzify_score(user_input.programming_interest)
    time_sets = fuzzify_score(user_input.time_availability)
    clarity_sets = fuzzify_score(user_input.career_clarity)

    web_score = max(
        min(programming_sets["medium"], time_sets["medium"]),
        min(programming_sets["high"], math_sets["low"]),
        min(clarity_sets["low"], time_sets["high"]),
    )
    data_score = max(
        min(math_sets["medium"], programming_sets["medium"]),
        min(math_sets["high"], time_sets["medium"]),
        min(clarity_sets["medium"], programming_sets["high"]),
    )
    ai_score = max(
        min(math_sets["high"], programming_sets["high"]),
        min(time_sets["high"], clarity_sets["high"]),
        min(math_sets["high"], clarity_sets["medium"]),
    )

    course_scores = {
        "Frontend Web Development": web_score,
        "Data Science Fundamentals": data_score,
        "AI and Machine Learning Foundations": ai_score,
    }

    recommended_course, confidence = max(course_scores.items(), key=lambda item: item[1])

    composite_score = (
        user_input.math_interest * 0.3
        + user_input.programming_interest * 0.3
        + user_input.time_availability * 0.2
        + user_input.career_clarity * 0.2
    )

    boosted_score = min(10.0, composite_score * (0.7 + confidence * 0.3))

    return {
        "recommended_course": recommended_course,
        "confidence": round(confidence, 2),
        "score": round(boosted_score, 2),
        "difficulty": _difficulty_label(boosted_score),
        "suitability": _suitability_label(boosted_score),
        "course_breakdown": {name: round(score, 2) for name, score in course_scores.items()},
        "memberships": {
            "math_interest": math_sets,
            "programming_interest": programming_sets,
            "time_availability": time_sets,
            "career_clarity": clarity_sets,
        },
    }
