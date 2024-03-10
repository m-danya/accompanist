from fastapi import FastAPI

app = FastAPI(
    title="Accompanist",
)


@app.get("/hello_world")
def hello_world():
    return "yay"
