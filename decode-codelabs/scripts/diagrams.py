"""Render accessible SVGs from editable, code-native diagram definitions."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def diagram(name,title,rows):
 h=110+len(rows)*108
 s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{h}" viewBox="0 0 900 {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><rect width="900" height="{h}" rx="20" fill="#f3f7f5"/><style>text{{font-family:Arial,sans-serif;fill:#16362c}}.title{{font-size:25px;font-weight:bold}}.label{{font-size:21px;font-weight:bold}}.detail{{font-size:18px}}</style><text x="32" y="47" class="title">{escape(title)}</text>']
 for i,(label,detail) in enumerate(rows):
  y=78+i*108
  s.append(f'<rect x="32" y="{y}" width="836" height="76" rx="9" fill="white" stroke="#b7cec2"/><text x="52" y="{y+29}" class="label">{i+1}. {escape(label)}</text><text x="52" y="{y+56}" class="detail">{escape(detail)}</text>')
  if i<len(rows)-1:s.append(f'<path d="M450 {y+80} v22 m-7 -7 l7 7 7 -7" fill="none" stroke="#167552" stroke-width="2"/>')
 s.append('</svg>')
 for lab in ['01-mpesa-mcp-server','02-adk-payment-agent']:
  (ROOT/'labs'/lab/'assets'/f'{name}.svg').write_text(''.join(s))
diagram('architecture','Two labs: reasoning, tools and trust boundaries',[
 ('Developer / Gemini CLI → private MCP, or developer → private ADK','HTTPS + Google ID token; each Cloud Run service checks IAM invoker.'),
 ('Lab 2: ADK Runner → Gemini on Vertex AI','Network model inference via ADC; model requests structured tool calls.'),
 ('ADK → Lab 1: FastMCP /mcp','Network: Streamable HTTP + ID token, audience = MCP service origin.'),
 ('FastMCP → domain.py','In-process validation, catalog prices, totals and preparation; no payment.'),
 ('Optional payments.py → Daraja sandbox','Network: OAuth Basic exchange, then Bearer-authenticated STK request.'),
 ('Asynchronous outcome outside the core path','No callback receiver, reconciliation database, order store or Apigee proxy.')])
diagram('payment-flow','Preparation is not payment confirmation',[
 ('Core: validate input → prepared_only','In-process; illustrative payload returned; no credentials or network needed.'),
 ('Optional: operator enables sandbox initiation','Code gate; fixed sandbox host; server controls shortcode and callback.'),
 ('MCP server → Daraja OAuth endpoint','HTTPS GET with app key + secret (Basic); token remains server-private.'),
 ('MCP server → Daraja STK endpoint','HTTPS POST once; ResponseCode 0 = accepted for processing only.'),
 ('Daraja → merchant callback (not implemented here)','Future HTTPS receiver must establish provenance, correlation and amount.'),
 ('Unknown outcome → reconcile before resubmitting','No automatic retry, durable idempotency, callback receiver or status query.')])
diagram('agent-sequence','One bounded ADK turn: who does what?',[
 ('Caller → Cloud Run /chat','HTTPS + caller ID token; IAM authorization happens before the app.'),
 ('app.py → runtime identity provider','Obtain MCP-audience ID token at turn start, not module import.'),
 ('app.py → Runner → Gemini','In-process orchestration, then network model inference with runtime ADC.'),
 ('MCPToolset → FastMCP /mcp','Network initialize → tools/list → tools/call; IAM checks agent identity.'),
 ('FastMCP → domain tool → MCPToolset → Gemini','Local execution, network result, then model inference for the reply.'),
 ('app.py → caller; close transports','Return text; close toolset in same task; delete process-local session.')])
diagram('apigee','Apigee extension: design only, not deployed',[
 ('Future caller → Apigee proxy','Authenticate client; authorize tools; quotas and rate policies.'),
 ('Future Apigee identity → protected MCP origin','Separate trust boundary: mint Google ID token; grant service-level invoker.'),
 ('Existing MCP origin → server validation','Do not confuse gateway policy with payment consent or validation.'),
 ('Extension acceptance criteria','Streaming, headers, audience, denial tests, policy tests and bypass controls.'),
 ('Core path remains direct Cloud Run IAM','No proxy bundle, Apigee org, policy configuration or gateway test supplied.')])
