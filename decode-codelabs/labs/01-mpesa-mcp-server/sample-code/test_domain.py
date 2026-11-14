import asyncio
import os
import unittest
from unittest.mock import patch
import httpx
from domain import calculate_order_total, validate_stk_push_payload, parse_stk_callback
from payments import initiate_stk_push

class DomainTests(unittest.TestCase):
    def test_basket(self):
        self.assertEqual(calculate_order_total([{"product_id": "conf-pass-001", "quantity": 2}])["order_total_kes"], 10)
        for quantity in (0, -1, True, "2", 1.5, 101):
            self.assertIn("error", calculate_order_total([{"product_id": "coffee-001", "quantity": quantity}]))
        self.assertIn("error", calculate_order_total([]))
        self.assertIn("error", calculate_order_total([{"product_id": "missing", "quantity": 1}]))
    def test_preparation(self):
        self.assertEqual(validate_stk_push_payload("254700000000", 10)["status"], "prepared_only")
        self.assertFalse(validate_stk_push_payload("2547abcdefgh", 10)["valid"])
        self.assertFalse(validate_stk_push_payload("254700000000", True)["valid"])
    def test_callback_not_evidence(self):
        self.assertFalse(parse_stk_callback({})["payment_verified"])
        r = parse_stk_callback({"Body": {"stkCallback": {"ResultCode": 0, "CheckoutRequestID": "fixture-checkout"}}})
        self.assertTrue(r["reported_success"])
        self.assertFalse(r["payment_verified"])
    def test_disabled_does_not_connect(self):
        with patch.dict(os.environ, {"ENABLE_SANDBOX_INITIATION": "false"}), patch("httpx.AsyncClient", side_effect=AssertionError("network forbidden")):
            self.assertEqual(asyncio.run(initiate_stk_push("254700000000", 10))["error"], "initiation_disabled")
    def test_sandbox_mocked_acceptance_and_uncertainty(self):
        # Every outgoing request goes to MockTransport, never a real socket.
        real_client = httpx.AsyncClient
        for timeout in (False, True):
            requests = []
            def respond(request):
                requests.append(request)
                if "/oauth/" in str(request.url):
                    return httpx.Response(200, json={"access_token": "fixture-token"})
                if timeout:
                    raise httpx.ReadTimeout("fixture timeout", request=request)
                return httpx.Response(200, json={"ResponseCode": "0", "CheckoutRequestID": "fixture-checkout"})
            env = {"ENABLE_SANDBOX_INITIATION": "true", "DARAJA_CONSUMER_KEY": "fixture-key", "DARAJA_CONSUMER_SECRET": "fixture-secret", "DARAJA_BUSINESS_SHORTCODE": "000000", "DARAJA_PASSKEY": "fixture-passkey", "DARAJA_CALLBACK_URL": "https://fixture.example/stk"}
            with patch.dict(os.environ, env), patch("payments.httpx.AsyncClient", side_effect=lambda **kw: real_client(transport=httpx.MockTransport(respond), **kw)):
                r = asyncio.run(initiate_stk_push("254700000000", 10))
            self.assertEqual(len(requests), 2)
            self.assertFalse(r["payment_verified"])
            self.assertNotIn("access_token", r)
            self.assertNotIn("request_body", r)
            if timeout:
                self.assertEqual(r["status"], "outcome_unknown")
            else:
                self.assertTrue(r["accepted_for_processing"])

if __name__ == "__main__":
    unittest.main()
