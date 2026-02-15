from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.router import router
from api.config import settings
import uvicorn

app = FastAPI(title="Project-AISound")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Uncle Bob'un Error Handling prensibi: Hatayı tek noktada yakala ve 
    kullanıcıya tutarlı bir JSON dön.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": f"Audio processing failed: {str(exc)}"},
    )

# Rotaları bağla
app.include_router(router)

if __name__ == "__main__":
    # DOĞRUDAN app nesnesini veriyoruz, tırnak içinde string değil!
    # Bu yöntemle reload=True kullanılamaz, dolayısıyla test yaparken 
    # sunucu kendi kendine reset atıp durmaz.
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port
    )