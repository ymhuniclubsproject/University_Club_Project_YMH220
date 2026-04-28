from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

# Register all models to Base (must be imported before create_all) | Tüm modelleri Base'e kaydet (create_all'dan önce import edilmeli)
from app.models import * # noqa: F401, F403

from app.routers import (
    user_router, auth, clubs, event,
    memberships, event_archive, message,
    admin_panel, attendance, search,
    announcements
)

# Synchronize database schema | Veri tabanı şemasını senkronize et
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UniClub Backend API",
    description="University Club Management System - Core Backend",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing | Çapraz Kaynak Paylaşımı (CORS) ayarlarını yapılandır
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows access from any origin (restrict in production) | Herhangi bir kaynaktan erişime izin verir (canlıda kısıtlanmalı)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"]) # Simple endpoint to verify service availability | Servis kullanılabilirliğini doğrulamak için basit uç nokta
def health_check():
    return {"status": "ok", "message": "UniClub API is running"}

# Register application routers | Uygulama yönlendiricilerini (router) kaydet
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