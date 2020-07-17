from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home() -> list:
    summaries = ['foo', 'bar']
    return summaries
