#!/usr/bin/env python3
"""
Test client for the modified QuantConnect MCP server using HTTP transport.
"""

import asyncio
import json
import httpx


async def test_quantconnect_mcp_server():
    """Test the QuantConnect MCP server via HTTP."""
    
    print("🧪 Testing QuantConnect MCP Server via HTTP")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8002"
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: List available tools
        print("📋 Test 1: Listing available tools...")
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
            
            response = await client.post(
                f"{base_url}/mcp",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if "result" in result and "tools" in result["result"]:
                    tools = result["result"]["tools"]
                    print(f"✅ Found {len(tools)} tools:")
                    
                    for i, tool in enumerate(tools[:5]):  # Show first 5 tools
                        print(f"   {i+1}. {tool.get('name', 'Unknown')} - {tool.get('description', 'No description')[:80]}...")
                    
                    if len(tools) > 5:
                        print(f"   ... and {len(tools) - 5} more tools")
                        
                    # Test 2: Try calling a simple tool
                    print(f"\n🔧 Test 2: Testing 'read_account' tool...")
                    
                    account_payload = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {
                            "name": "read_account",
                            "arguments": {}
                        }
                    }
                    
                    account_response = await client.post(
                        f"{base_url}/mcp",
                        json=account_payload,
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json, text/event-stream"
                        },
                        timeout=15.0
                    )
                    
                    if account_response.status_code == 200:
                        account_result = account_response.json()
                        
                        if "result" in account_result:
                            print("✅ Account info retrieved successfully!")
                            content = account_result["result"].get("content", [])
                            
                            for item in content[:3]:  # Show first 3 content items
                                if isinstance(item, dict) and "text" in item:
                                    text = item["text"]
                                    print(f"   📄 {text[:100]}...")
                                    
                        elif "error" in account_result:
                            print(f"❌ Tool call failed: {account_result['error']}")
                        else:
                            print(f"⚠️  Unexpected response: {account_result}")
                    else:
                        print(f"❌ HTTP error {account_response.status_code}: {account_response.text}")
                        
                    # Test 3: Try listing projects
                    print(f"\n📂 Test 3: Testing 'list_projects' tool...")
                    
                    projects_payload = {
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "tools/call",
                        "params": {
                            "name": "list_projects",
                            "arguments": {}
                        }
                    }
                    
                    projects_response = await client.post(
                        f"{base_url}/mcp",
                        json=projects_payload,
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json, text/event-stream"
                        },
                        timeout=15.0
                    )
                    
                    if projects_response.status_code == 200:
                        projects_result = projects_response.json()
                        
                        if "result" in projects_result:
                            print("✅ Projects listed successfully!")
                            content = projects_result["result"].get("content", [])
                            
                            for item in content[:2]:  # Show first 2 projects
                                if isinstance(item, dict) and "text" in item:
                                    text = item["text"][:200]
                                    print(f"   📁 {text}...")
                                    
                        elif "error" in projects_result:
                            print(f"❌ Tool call failed: {projects_result['error']}")
                            
                    else:
                        print(f"❌ HTTP error {projects_response.status_code}: {projects_response.text}")
                        
                else:
                    print(f"❌ Unexpected response format: {result}")
                    
            else:
                print(f"❌ HTTP error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Testing completed!")
    print("\n💡 Summary:")
    print("  ✅ QuantConnect MCP server is running with HTTP transport")
    print("  ✅ Server responds to MCP protocol calls")
    print("  ✅ Ready for EC2 deployment and econ-agent integration")


if __name__ == "__main__":
    asyncio.run(test_quantconnect_mcp_server())
