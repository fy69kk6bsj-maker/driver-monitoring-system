from fastapi import FastAPI
from routers import image, audio, gps, fusion, decision, response, user

app = FastAPI(title="Driver Monitoring System")

app.include_router(image.router,    prefix="/image")
app.include_router(audio.router,    prefix="/audio")
app.include_router(gps.router,      prefix="/gps")
app.include_router(fusion.router,   prefix="/fusion")
app.include_router(decision.router, prefix="/decision")
app.include_router(response.router, prefix="/response")
app.include_router(user.router,     prefix="/user")

@app.get("/")
def root():
    return {"status": "ok", "message": "Driver Monitoring System"}
