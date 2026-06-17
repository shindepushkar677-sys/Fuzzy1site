from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from fuzzy_logic import RecommendationInput, recommend_course


class StudentProfile(BaseModel):
    math_interest: float = Field(..., ge=0, le=10, description="Interest in math from 0 to 10")
    programming_interest: float = Field(
        ..., ge=0, le=10, description="Interest in programming from 0 to 10"
    )
    time_availability: float = Field(
        ..., ge=0, le=10, description="Available study time from 0 to 10"
    )
    career_clarity: float = Field(
        ..., ge=0, le=10, description="Clarity about career goals from 0 to 10"
    )


class RecommendationResponse(BaseModel):
    recommended_course: str
    confidence: float
    score: float
    difficulty: str
    suitability: str
    course_breakdown: dict[str, float]
    memberships: dict[str, dict[str, float]]


app = FastAPI(
    title="Fuzzy Course Recommender API",
    description="Suggests a course path using simple fuzzy-logic rules.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Fuzzy Course Recommender API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def create_recommendation(profile: StudentProfile) -> RecommendationResponse:
    result = recommend_course(
        RecommendationInput(
            math_interest=profile.math_interest,
            programming_interest=profile.programming_interest,
            time_availability=profile.time_availability,
            career_clarity=profile.career_clarity,
        )
    )
    return RecommendationResponse(**result)
