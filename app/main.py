from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .courses import router as courses_router
from .data_loader import initialize_database
import ssl
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
cert_file = os.path.join(current_dir, "cert.pem")
key_file = os.path.join(current_dir, "key.pem")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

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
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl=ssl_context)
