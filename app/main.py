from fastapi import FastAPI

app = FastAPI(title="Sniply")

@app.get("/healthz")
def health():
    return {"status": "ok"}
