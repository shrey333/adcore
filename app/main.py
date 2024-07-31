from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .courses import router as courses_router
from .data_loader import initialize_database

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await initialize_database()


app.include_router(courses_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
