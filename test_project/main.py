from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello to the OpenAI community"}
