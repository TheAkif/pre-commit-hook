import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.pre_start import init

init()  # Wait for db + create superuser

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}{settings.API_V1_STR}/openapi.json",
)


@app.get("/", response_class=HTMLResponse, tags=["Home"])
async def get_landing_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FAST API COOKIE CUTTER</title>
        <style>
            body {
                background-image: url('/static/cool-background.png'); /* Path to the local image */
                background-size: cover;
                background-position: center;
                height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
            }
            h1 {
                color: #FFFFFF;
                font-size: 36px;
                background-color: rgba(0, 0, 0, 0.7);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            a {
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <a href="/docs">
            <img src='https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png' alt="Header Image" />
        </a>
    </body>
    </html>
    """
    return html_content


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
