from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="./dist"), name="static")
templates = Jinja2Templates(directory="src/")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="pages/index.html")

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="pages/login.html")


@app.get("/chunks/{pagechunk_name}", response_class=HTMLResponse)
async def partials(request: Request, pagechunk_name: str):
    return templates.TemplateResponse(
        request=request, name=f"chunks/{pagechunk_name}.html"
    )
