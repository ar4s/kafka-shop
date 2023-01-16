from fastapi import FastAPI

from .routes import router
from ..dependencies import producer

app = FastAPI(debug=True, title="Factory API")


app.include_router(router)

@app.on_event("shutdown")
async def shutdown_server():
    await producer.stop()


@app.on_event("startup")
async def start_server():
    await producer.start()
