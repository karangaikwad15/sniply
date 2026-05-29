import secrets
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Sniply")
_store: dict[str, str] = {}   # in-memory for now; swapped for Postgres next

class ShortenRequest(BaseModel):
    url: HttpUrl

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/api/shorten")
def shorten(body: ShortenRequest):
    code = secrets.token_urlsafe(5)
    _store[code] = str(body.url)
    return {"code": code, "short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str):
    url = _store.get(code)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url)
