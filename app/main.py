from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import auth, products, orders
from app.db import engine
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

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

@app.on_event("startup")
async def check_db():
    if engine is None:
        print("Warning: Database engine is not configured. Check your .env file.")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>FastAPI Backend Project</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #f7f9fb; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 60px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.07); padding: 40px 32px; text-align: center; }
            h1 { color: #2d6cdf; margin-bottom: 0.5em; }
            p, li { color: #444; font-size: 1.1em; margin-bottom: 1.2em; text-align: left; }
            ul { padding-left: 1.2em; text-align: left; }
            .docs-link { display: inline-block; background: #2d6cdf; color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-size: 1.1em; font-weight: 600; transition: background 0.2s; }
            .docs-link:hover { background: #174ea6; }
            .footer { margin-top: 2em; color: #aaa; font-size: 0.95em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FastAPI Backend (Python 3.11)</h1>
            <p>This API supports:</p>
            <ul>
                <li>User authentication with JWT</li>
                <li>Product listing with pagination</li>
                <li>Order creation with receipt</li>
                <li>CSV import for products</li>
                <li>Swagger UI for testing endpoints</li>
            </ul>
            <a class="docs-link" href="/docs">Open Swagger UI Docs</a>
            <div class="footer">Powered by Python 3.11 · FastAPI · <a href="https://fastapi.tiangolo.com/" style="color:#2d6cdf;">Docs</a></div>
        </div>
    </body>
    </html>
    """

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=app.title,
#         version="1.0.0",
#         description="API for Game Item Store with JWT Auth using JSON body",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT"
#         }
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi