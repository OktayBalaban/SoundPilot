import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.router import router

app = FastAPI(title="Project-AISound")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

app.include_router(router, prefix="/api/v1/processor")

if __name__ == "__main__":
    print(f"--- Project-AISound Backend ---")
    print(f"URL: http://127.0.0.1:8000")
    print(f"Static Files (Serving from): {OUTPUT_DIR} -> accessible via /static")
    uvicorn.run(app, host="127.0.0.1", port=8000)