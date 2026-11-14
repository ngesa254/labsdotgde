"""No network: model events, tokens, and remote toolsets are replaced."""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import app
from agent import SAFE_TOOLS, create_agent

class AgentTests(unittest.TestCase):
    def test_allowlist_and_factory(self):
        with patch.dict(os.environ, {"MODEL": "fixture-model"}):
            agent, toolset = create_agent("https://mcp.example.invalid/mcp", {})
        self.assertEqual(agent.name, "decode_merchant")
        self.assertNotIn("initiate_stk_push", SAFE_TOOLS)
        self.assertEqual(toolset.tool_filter, SAFE_TOOLS)
    def test_origin(self):
        for url in ("http://localhost:8080", "https://host/mcp", "https://host?x=1"):
            with patch.dict(os.environ, {"MCP_SERVICE_URL": url}):
                with self.assertRaises(ValueError): app.remote_config()
        with patch.dict(os.environ, {"MCP_SERVICE_URL": "https://host/"}):
            self.assertEqual(app.remote_config(), "https://host")
    def test_health_and_input(self):
        with TestClient(app.app) as client:
            self.assertEqual(client.get("/health").json()["status"], "ok")
            self.assertEqual(client.post("/chat", json={"message": ""}).status_code, 422)
    def test_cleanup_and_new_token_each_turn(self):
        toolset = SimpleNamespace(close=AsyncMock())
        async def events(**kwargs):
            yield SimpleNamespace(is_final_response=lambda: True,
                content=SimpleNamespace(parts=[SimpleNamespace(text="fixture response")]))
        runner = SimpleNamespace(run_async=events)
        with patch("app.identity_headers", return_value={"Authorization": "Bearer fixture"}) as token, \
             patch("app.create_agent", return_value=(object(), toolset)), \
             patch("app.Runner", return_value=runner), \
             patch.dict(os.environ, {"MCP_SERVICE_URL": "https://host"}):
            with TestClient(app.app) as client:
                first = client.post("/chat", json={"message": "catalog"})
                second = client.post("/chat", json={"message": "basket"})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()["text"], "fixture response")
        self.assertNotEqual(first.json()["session_id"], second.json()["session_id"])
        self.assertEqual(token.call_count, 2)
        self.assertEqual(toolset.close.await_count, 2)
    def test_failure_closes_toolset(self):
        toolset = SimpleNamespace(close=AsyncMock())
        with patch("app.identity_headers", return_value={}), \
             patch("app.create_agent", return_value=(object(), toolset)), \
             patch("app.Runner", side_effect=RuntimeError("fixture dependency failure")), \
             patch.dict(os.environ, {"MCP_SERVICE_URL": "https://host"}):
            with TestClient(app.app) as client:
                response = client.post("/chat", json={"message": "catalog"})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("fixture dependency failure", response.text)
        toolset.close.assert_awaited_once()

if __name__ == "__main__": unittest.main()
