from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Initialize the FastAPI application
app = FastAPI()

# Set up the Jinja2 template engine
templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request) -> HTMLResponse:
    """Renders the home page with a red background and prominent text."""
    return templates.TemplateResponse("home.html", {"request": request})