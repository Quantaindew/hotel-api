import json

from fastapi import FastAPI
from uagents import Model
from uagents.query import query

AGENT_ADDRESS = "agent1q2tcn9ssj55wfxq4qzuvgcx2cugfjgmnm328hvsqvyl28nmp2tv27ycg26z"


class TestRequest(Model):
    message: str


async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]


app = FastAPI()


@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/endpoint")
async def make_agent_call(req: TestRequest):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"