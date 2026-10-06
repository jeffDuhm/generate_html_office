from fastapi import FastAPI

app = FastAPI()


@app.get("/sample")
def sample():
    return {"status": "ok"}