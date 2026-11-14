"""Local HTTP MCP+ADK compatibility check; no model, IAM or Daraja network calls."""
import asyncio
import json
import os
from pathlib import Path
import socket
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'labs/01-mpesa-mcp-server/sample-code'),str(ROOT/'labs/02-adk-payment-agent/sample-code')]
os.environ['ENABLE_SANDBOX_INITIATION']='false'
os.environ['MODEL']='fixture-model'
from fastmcp import Client
import uvicorn
from server import mcp
from agent import create_agent

async def main():
    sock=socket.socket();sock.bind(('127.0.0.1',0));sock.listen(128)
    url=f'http://127.0.0.1:{sock.getsockname()[1]}/mcp'
    app=mcp.http_app(path='/mcp',stateless_http=True)
    server=uvicorn.Server(uvicorn.Config(app,log_level='error'))
    task=asyncio.create_task(server.serve(sockets=[sock]))
    try:
        while not server.started:
            if task.done(): await task
            await asyncio.sleep(.05)
        async with Client(url) as client:
            tools=await client.list_tools()
            assert len(tools)==6
            total=await client.call_tool('calculate_order_total',{'items':[{'product_id':'conf-pass-001','quantity':2}]})
            assert total.data['order_total_kes']==10
            invalid=await client.call_tool('calculate_order_total',{'items':[{'product_id':'coffee-001','quantity':0}]})
            assert 'error' in invalid.data
        agent,toolset=create_agent(url,{})
        try:
            discovered=await toolset.get_tools()
            assert len(discovered)==6 and 'initiate_stk_push' not in [t.name for t in discovered]
            for tool in discovered:
                assert tool._get_declaration().name == tool.name
            basket_tool=next(tool for tool in discovered if tool.name=='calculate_order_total')
            adk_result=await basket_tool.run_async(args={'items':[{'product_id':'conf-pass-001','quantity':2}]}, tool_context=None)
            assert adk_result.structuredContent['order_total_kes']==10
        finally: await toolset.close()
        result={'transport':'local Streamable HTTP /mcp','catalog_tools':6,'basket_total_kes':10,
                'invalid_basket':'rejected','adk_discovery':'six safe tools; Gemini declarations generated; ADK basket invocation returned KES 10','cleanup':'toolsets closed',
                'cloud_IAM':'not tested','model_inference':'not tested','Daraja':'not called'}
        (ROOT/'evidence/integration-results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    finally:
        server.should_exit=True
        await task

asyncio.run(main())
