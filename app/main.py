from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers.index import all_routers
from app.db import engine
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
print(os.getenv("DATABASE_URL"))


app = FastAPI(
    title="FastAPI Backend (Python 3.11)",
    docs_url="/docs",
    redoc_url=None,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": False,
        "clientId": "default",  # just placeholder, can be ignored
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def check_db():
    if engine is None:
        print("Warning: Database engine is not configured. Check your .env file.")

@app.get("/", response_class=HTMLResponse)
def root():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "../templates/index.html")
    with open(html_path, encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

for router in all_routers:
    app.include_router(router)