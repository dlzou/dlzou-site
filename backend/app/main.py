from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home():
    summaries = ['foo', 'bar']
    return summaries
