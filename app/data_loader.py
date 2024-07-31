from fastapi import HTTPException, status
import pandas as pd
import datetime
from .database import db


async def load_initial_data():
    try:
        data_url = "https://api.mockaroo.com/api/501b2790?count=1000&key=8683a1c0"
        df = pd.read_csv(data_url)
        df_dict = df.to_dict(orient="records")
        timestamp = datetime.datetime.utcnow()
        for record in df_dict:
            record["timestamp"] = timestamp
            record["created_at"] = datetime.datetime.utcnow()
        await db.courses.insert_many(df_dict)
        await db.courses.create_index("timestamp", expireAfterSeconds=600)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load initial data",
        )


async def initialize_database():
    try:
        count = await db.courses.count_documents({})
        if count == 0:
            await load_initial_data()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize database",
        )
