from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request) -> HTMLResponse:
    """Render the home page with a red background and prominent text."""
    logger.info("Home page accessed.")
    return templates.TemplateResponse("home.html", {"request": request})