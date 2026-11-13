import os
import sys
import hashlib
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from sqlalchemy.orm import Session

BASE_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_BACKEND_DIR not in sys.path:
    sys.path.insert(0, BASE_BACKEND_DIR)

from app.database import engine, Base, get_db
from app.models import Admin
from app.api import auth_api, dashboard_api, products_api, categories_api, customers_api, orders_api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — Full-Stack Edition", docs_url=None, redoc_url=None)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    try:
        from seed import seed_database
        seed_database()
    except Exception as e:
        print(f"Startup auto-seed check: {e}")

app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6781", "http://127.0.0.1:6781"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth_api.router)
app.include_router(dashboard_api.router)
app.include_router(products_api.router)
app.include_router(categories_api.router)
app.include_router(customers_api.router)
app.include_router(orders_api.router)

security = HTTPBasic(auto_error=False)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    pw_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == credentials.username,
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Shop Manager API")


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    pw_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == credentials.username,
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return app.openapi()


@app.get("/")
async def root():
    return RedirectResponse("/docs")
