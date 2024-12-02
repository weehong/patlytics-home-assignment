import re
from pydantic import BaseModel, Field, field_validator


class PatentRequest(BaseModel):
    patent_id: str = Field(
        ..., description="Patent identification number", min_length=1
    )
    company_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("patent_id")
    def validate_patent_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Patent ID cannot be null or empty")

        patent = r"^US-[A-Z0-9]+-[A-Z0-9]+$"
        if not re.match(patent, v):
            raise ValueError(
                "Invalid Patent ID format. Must match format: US-XXXXXX-XX"
            )
        return v

    @field_validator("company_name")
    def validate_company_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Company name cannot be null or empty")
        return v

    class Config:
        json_schema_extra = {
            "example": {"patent_id": "PTN123", "company_name": "Tech Corp"}
        }
