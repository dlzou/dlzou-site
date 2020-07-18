from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home() -> list:
    summaries = ['foo', 'bar']
    return summaries
