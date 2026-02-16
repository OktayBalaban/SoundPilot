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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Audio processing failed: {str(exc)}"},
    )

app.include_router(router, prefix="/api/v1/processor")

if __name__ == "__main__":
    print(f"--- Project-AISound Backend ---")
    print(f"URL: http://127.0.0.1:8000")
    print(f"Static Files: {OUTPUT_DIR} -> /static")
    uvicorn.run(app, host="127.0.0.1", port=8000)