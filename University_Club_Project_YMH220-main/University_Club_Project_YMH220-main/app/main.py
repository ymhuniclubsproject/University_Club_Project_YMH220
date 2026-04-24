from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import (
    user_router, auth, clubs, event, 
    memberships, event_archive, message, 
    admin_panel, attendance, search, 
    announcements
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UniClub Backend API",
    description="University Club Management System - Core Backend",
    version="1.0.0"
)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "UniClub API is running"}

app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(clubs.router)
app.include_router(event.router)
app.include_router(memberships.router)
app.include_router(message.router)
app.include_router(admin_panel.router)
app.include_router(attendance.router)
app.include_router(search.router)
app.include_router(event_archive.router)
app.include_router(announcements.router)