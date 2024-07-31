from fastapi import APIRouter, HTTPException, status
from typing import Optional
from bson import ObjectId
import datetime
from .database import db
from .models import Course, UpdateCourse, PatchCourse, PaginatedCourseResponse

router = APIRouter()


@router.post("/courses/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    try:
        course_dict = course.dict(by_alias=True)

        if "_id" in course_dict:
            del course_dict["_id"]

        course_dict["created_at"] = datetime.datetime.utcnow()
        course_dict["timestamp"] = datetime.datetime.utcnow()
        course_dict["StartDate"] = datetime.datetime.combine(
            course_dict["StartDate"], datetime.datetime.min.time()
        )
        course_dict["EndDate"] = datetime.datetime.combine(
            course_dict["EndDate"], datetime.datetime.min.time()
        )
        result = await db.courses.insert_one(course_dict)
        return str(result.inserted_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create course",
        )


@router.get("/courses/", response_model=PaginatedCourseResponse)
async def get_courses(search: Optional[str] = None, page: int = 1, size: int = 10):
    try:
        query = {}
        if search:
            query = {
                "$or": [
                    {"University": {"$regex": search, "$options": "i"}},
                    {"City": {"$regex": search, "$options": "i"}},
                    {"Country": {"$regex": search, "$options": "i"}},
                    {"CourseName": {"$regex": search, "$options": "i"}},
                    {"CourseDescription": {"$regex": search, "$options": "i"}},
                ]
            }
        total = await db.courses.count_documents(query)
        skip = (page - 1) * size
        cursor = db.courses.find(query).sort("created_at", -1).skip(skip).limit(size)
        courses = await cursor.to_list(length=size)
        formatted_courses = [
            {**course, "_id": str(course["_id"])} for course in courses
        ]
        return PaginatedCourseResponse(
            total=total, page=page, size=size, courses=formatted_courses
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch courses",
        )


def convert_to_datetime(date: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(date, datetime.datetime.min.time())


@router.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: str, course: UpdateCourse):
    try:
        update_data = {
            k: v for k, v in course.dict(by_alias=True).items() if v is not None
        }
        if "StartDate" in update_data:
            update_data["StartDate"] = convert_to_datetime(update_data["StartDate"])
        if "EndDate" in update_data:
            update_data["EndDate"] = convert_to_datetime(update_data["EndDate"])
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update provided",
            )
        result = await db.courses.update_one(
            {"_id": ObjectId(course_id)}, {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
            )
        updated_course = await db.courses.find_one({"_id": ObjectId(course_id)})
        updated_course["_id"] = str(updated_course["_id"])
        return Course(**updated_course)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update course",
        )


@router.patch("/courses/{course_id}", response_model=Course)
async def patch_course(course_id: str, course: PatchCourse):
    try:
        patch_data = {
            k: v for k, v in course.dict(by_alias=True).items() if v is not None
        }
        if "StartDate" in patch_data:
            patch_data["StartDate"] = datetime.datetime.combine(
                patch_data.pop("StartDate"), datetime.datetime.min.time()
            )
        if "EndDate" in patch_data:
            patch_data["EndDate"] = datetime.datetime.combine(
                patch_data.pop("EndDate"), datetime.datetime.min.time()
            )
        if not patch_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update provided",
            )
        result = await db.courses.update_one(
            {"_id": ObjectId(course_id)}, {"$set": patch_data}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
            )
        updated_course = await db.courses.find_one({"_id": ObjectId(course_id)})
        return Course(**updated_course)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to patch course",
        )


@router.delete("/courses/{course_id}", response_model=str)
async def delete_course(course_id: str):
    try:
        result = await db.courses.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
            )
        return course_id
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete course",
        )
