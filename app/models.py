from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from bson import ObjectId


class Course(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    university: str = Field(..., alias="University")
    city: str = Field(..., alias="City")
    country: str = Field(..., alias="Country")
    course_name: str = Field(..., alias="CourseName")
    course_description: str = Field(..., alias="CourseDescription")
    start_date: datetime.date = Field(..., alias="StartDate")
    end_date: datetime.date = Field(..., alias="EndDate")
    price: float = Field(..., alias="Price")
    currency: str = Field(..., alias="Currency")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime.date: lambda v: v.isoformat(),
            datetime.datetime: lambda v: v.isoformat(),
        }


class UpdateCourse(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    university: str = Field(..., alias="University")
    city: str = Field(..., alias="City")
    country: str = Field(..., alias="Country")
    course_name: str = Field(..., alias="CourseName")
    course_description: str = Field(..., alias="CourseDescription")
    start_date: datetime.date = Field(..., alias="StartDate")
    end_date: datetime.date = Field(..., alias="EndDate")
    price: float = Field(..., alias="Price")
    currency: str = Field(..., alias="Currency")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime.date: lambda v: v.isoformat()}


class PatchCourse(BaseModel):
    university: Optional[str] = Field(None, alias="University")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")
    course_name: Optional[str] = Field(None, alias="CourseName")
    course_description: Optional[str] = Field(None, alias="CourseDescription")
    start_date: Optional[datetime.date] = Field(None, alias="StartDate")
    end_date: Optional[datetime.date] = Field(None, alias="EndDate")
    price: Optional[float] = Field(None, alias="Price")
    currency: Optional[str] = Field(None, alias="Currency")


class PaginatedCourseResponse(BaseModel):
    total: int
    page: int
    size: int
    courses: List[Course]
