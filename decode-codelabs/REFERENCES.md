# References

Access date for all entries: **14 November 2026**, Africa/Nairobi. Primary references resolve technical questions; current documentation does not override the pinned package APIs without an explicit migration. No signed-in cloud or Daraja session was accessed.

| Reference | Use and access result |
|---|---|
| [Local public-source counterpart](https://github.com/ngesa254/labsdotgde/tree/release/devfest_2026/decode) | Public GitHub retrieval unavailable (API HTTP 403; browser cache miss). Local checkout at recorded commit is authoritative; remote equality unknown. |
| [Google Codelabs tools](https://github.com/googlecodelabs/tools) | Confirmed repository archived 16 December 2025; no active upstream maintenance assumed. |
| [claat directory](https://github.com/googlecodelabs/tools/tree/main/claat) | Official command/tooling context; executable help also inspected locally. |
| [Markdown parser guide](https://github.com/googlecodelabs/tools/blob/main/claat/parser/md/README.md) / [raw guide](https://raw.githubusercontent.com/googlecodelabs/tools/main/claat/parser/md/README.md) | Metadata, step durations, fences and callout guidance. Observed binary differences recorded in TOOLCHAIN.md. |
| [Official v2.2.6 release asset](https://github.com/googlecodelabs/tools/releases/download/v2.2.6/claat-darwin-amd64) | Downloaded successfully and SHA-256 recorded; executed on macOS arm64 with compatibility support. |
| [Historical DEV article](https://dev.to/bpetetot/build-your-own-codelab-with-google-codelab-1hdi) | Benjamin Petetot, 9 January 2020. Historical Markdown/export/serve context only. Its Docker image and older installation assumptions were not adopted or tested. |
| [Solace codelab authoring guide](https://codelabs.solace.dev/codelabs/codelab-4-codelab/?index=..%2F..index#2) | Reviewed with local templates/init/watch files for focused steps, configuration context and authoring discipline. No Solace branding or contribution obligations imported. |
| [Cloud Run source deployment](https://cloud.google.com/run/docs/deploying-source-code) | Deployer, build identity, runtime identity, source build and Artifact Registry responsibilities. No deployment performed. |
| [Cloud Run service-to-service authentication](https://cloud.google.com/run/docs/authenticating/service-to-service) | Runtime ID token, receiving-service audience and authorization boundary. Code obtains a fresh token per bounded turn; cloud behavior unverified. |
| [Cloud Run MCP hosting](https://cloud.google.com/run/docs/host-mcp-servers) | Primary hosting/authentication context for remote MCP. |
| [Cloud Run secrets](https://cloud.google.com/run/docs/configuring/services/secrets) | Optional future versioned Secret Manager references and secret-level runtime access. No secret store accessed or created. |
| [ADK MCP tools](https://google.github.io/adk-docs/tools-custom/mcp-tools/) | Current conceptual integration; redirects to current ADK site and may differ from pinned 1.14.0 API. |
| [ADK 1.14.0 MCP toolset source](https://github.com/google/adk-python/blob/v1.14.0/src/google/adk/tools/mcp_tool/mcp_toolset.py) | Verified local installed API: `MCPToolset`, `tool_filter`, `get_tools`, `close`. Deprecation aliases are retained explicitly from the source edition. |
| [ADK 1.14.0 session manager](https://github.com/google/adk-python/blob/v1.14.0/src/google/adk/tools/mcp_tool/mcp_session_manager.py) | `StreamableHTTPConnectionParams`, static headers and asynchronous session ownership. No `header_provider` assumed in that version. |
| [FastMCP 2.12.4 source](https://github.com/jlowin/fastmcp/blob/v2.12.4/src/fastmcp/server/server.py) | Standalone distribution, `run`, HTTP transport/path, stateless server and tool registration. Installed source/imports checked. |
| [FastMCP server runtime](https://gofastmcp.com/deployment/running-server) | Current conceptual guide; pinned package source is the API authority. |
| [MCP 2025-06-18 transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) | Streamable HTTP, initialization and client/server lifecycle. Not a claim that this workshop implements every newer protocol capability. |
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) / [pinned 1.14.1 transport](https://github.com/modelcontextprotocol/python-sdk/blob/v1.14.1/src/mcp/server/streamable_http.py) | SDK dependency, observed closed-stream message-router diagnostic and compatibility scope. |
| [Gemini CLI MCP configuration](https://geminicli.com/docs/tools/mcp-server/) | `httpUrl`, headers and environment substitution. Existing CLI is an optional participant prerequisite; no model/CLI session run during authoring. |
| [Apigee Google authentication](https://cloud.google.com/apigee/docs/api-platform/security/google-auth/overview) | Future proxy-to-Cloud Run identity boundary; no proxy supplied. |
| [MCP in Apigee](https://cloud.google.com/apigee/docs/api-platform/apigee-mcp/apigee-mcp-overview) | Current extension context; the source architecture does not constitute configured integration. An earlier guessed MCP URL was unavailable; this verified page replaced it. |
| [Daraja M-Pesa Express](https://developer.safaricom.co.ke/apis/MpesaExpressSimulate) | Portal page reachable but dynamic/authenticated API fields not exposed in retrieved text. Source-derived endpoint/payload implementation retained for optional mocked integration, with explicit provider-verification gate. |
| [Daraja portal](https://daraja.safaricom.co.ke/) | Participant's sandbox app/configuration source; no sign-in, secret retrieval or API call performed. |
| [Model lifecycle](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions) | Lists `gemini-2.5-flash` retirement on 20 October 2026, `gemini-2.0-flash-lite` on 1 June 2026. Motivates documented migration instead of a retired default. |
| [Gemini 3.8 Flash model page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash) | Current listed replacement, function calling and `global` endpoint support. Project access and old-SDK model inference remain unverified. |

Package pins and imports are additionally evidenced by installed distribution metadata, per-lab dependency locks, `pip check`, unit tests and the local HTTP/ADK integration check. That local evidence is separate from the cloud/provider claims above.

## Locally bundled frontend follow-up

Accessed 14 November 2026. `site/vendor/claat/manifest.json` records exact source URLs and hashes for the bundled runtime and fonts. Codelab components/styles come from the official claat CDN; syntax highlighting comes from [Google code-prettify](https://github.com/google/code-prettify). Fonts come from [Google Fonts](https://github.com/google/fonts) and [Google Material Design Icons](https://github.com/google/material-design-icons). Corresponding upstream Apache-2.0/SIL OFL license notices are included. CDN/proxy failures during download were retried through approved networking; ordinary builds/previews now read these assets locally.
