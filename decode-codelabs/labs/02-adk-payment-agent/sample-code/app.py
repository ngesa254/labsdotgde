"""Private Cloud Run teaching API; sessions are deliberately process-local."""
import asyncio
import os
from uuid import uuid4
from urllib.parse import urlparse
import google.auth.transport.requests
import google.oauth2.id_token
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import create_agent

app = FastAPI(title="DECODE merchant agent")
sessions = InMemorySessionService()

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=4000)

def remote_config():
    origin = os.environ["MCP_SERVICE_URL"].rstrip("/")
    parsed = urlparse(origin)
    if parsed.scheme != "https" or not parsed.hostname or parsed.path or parsed.query or parsed.fragment or parsed.username:
        raise ValueError("MCP_SERVICE_URL must be the HTTPS service origin, without /mcp")
    return origin

def identity_headers(origin):
    # Runtime service identity on Cloud Run. No service-account key file.
    # A fresh token is acquired per bounded turn; nothing is cached at import time.
    token = google.oauth2.id_token.fetch_id_token(google.auth.transport.requests.Request(), origin)
    return {"Authorization": f"Bearer {token}"}

@app.get("/health")
async def health():
    return {"status": "ok", "payment_execution": "disabled"}

@app.post("/chat")
async def chat(body: ChatRequest):
    # Each HTTP request is an independent session. IAM authenticates the caller;
    # this sample does not implement per-user session authorization or persistence.
    sid = uuid4().hex
    toolset = None
    try:
        async with asyncio.timeout(120):
            origin = remote_config()
            headers = await asyncio.to_thread(identity_headers, origin)
            agent, toolset = create_agent(origin + "/mcp", headers)
            await sessions.create_session(app_name="decode", user_id="workshop", session_id=sid)
            runner = Runner(agent=agent, app_name="decode", session_service=sessions)
            answer = []
            async for event in runner.run_async(user_id="workshop", session_id=sid,
                    new_message=types.Content(role="user", parts=[types.Part(text=body.message)])):
                if event.is_final_response() and event.content:
                    answer.extend(part.text for part in event.content.parts if part.text)
            return {"session_id": sid, "text": "\n".join(answer), "payment_execution": "disabled"}
    except TimeoutError:
        raise HTTPException(504, "Turn timed out; no payment operation is exposed.")
    except Exception:
        raise HTTPException(502, "Agent dependency failed. Check endpoint, identity and model configuration.")
    finally:
        # Close MCP transports in the same request task that opened them.
        if toolset is not None:
            await toolset.close()
        await sessions.delete_session(app_name="decode", user_id="workshop", session_id=sid)
