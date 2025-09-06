#!/usr/bin/env python3
"""
Proper MCP HTTP client for testing QuantConnect MCP server.
Uses the official MCP SDK for proper session management.
"""

import asyncio
import logging
from mcp.client.streamable_http import StreamableHTTPClientTransport
from mcp.client import Client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_quantconnect_mcp_http():
    """Test QuantConnect MCP server via HTTP with proper MCP client."""
    
    print("🧪 Testing QuantConnect MCP Server via HTTP (Official MCP SDK)")
    print("=" * 60)
    
    # Create the HTTP transport
    transport = StreamableHTTPClientTransport("http://127.0.0.1:8002/mcp")
    
    # Create MCP client
    client = Client(
        client_info={
            "name": "quantconnect-test-client",
            "version": "1.0.0"
        },
        capabilities={}
    )
    
    try:
        print("🔗 Connecting to QuantConnect MCP server...")
        
        # Connect to the server
        await client.connect(transport)
        print("✅ Connected successfully!")
        
        # List available tools
        print("\n📋 Listing available tools...")
        tools_result = await client.list_tools()
        
        if tools_result and tools_result.tools:
            print(f"✅ Found {len(tools_result.tools)} tools:")
            
            # Show first 10 tools
            for i, tool in enumerate(tools_result.tools[:10]):
                print(f"   {i+1:2d}. {tool.name} - {tool.description[:60]}...")
            
            if len(tools_result.tools) > 10:
                print(f"   ... and {len(tools_result.tools) - 10} more tools")
                
            # Test calling a simple tool
            print(f"\n🔧 Testing 'read_account' tool...")
            
            account_result = await client.call_tool(
                name="read_account",
                arguments={}
            )
            
            if account_result:
                print("✅ Account tool call successful!")
                if hasattr(account_result, 'content') and account_result.content:
                    for item in account_result.content[:2]:
                        if hasattr(item, 'text'):
                            print(f"   📄 {item.text[:80]}...")
            else:
                print("❌ Account tool call failed")
                
            # Test listing projects
            print(f"\n📂 Testing 'list_projects' tool...")
            
            projects_result = await client.call_tool(
                name="list_projects", 
                arguments={}
            )
            
            if projects_result:
                print("✅ Projects tool call successful!")
                if hasattr(projects_result, 'content') and projects_result.content:
                    for item in projects_result.content[:2]:
                        if hasattr(item, 'text'):
                            print(f"   📁 {item.text[:80]}...")
            else:
                print("❌ Projects tool call failed")
                
        else:
            print("❌ No tools found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Detailed error information:")
        
    finally:
        try:
            await client.close()
            print("\n🔚 Connection closed")
        except:
            pass
    
    print("\n🎉 HTTP Transport Test Completed!")
    print("\n💡 Results:")
    print("  ✅ If tools were listed successfully, HTTP transport is working")
    print("  ✅ Server can then be used with any HTTP-capable MCP client")
    print("  ✅ Ready for econ-agent integration via HTTP")


if __name__ == "__main__":
    asyncio.run(test_quantconnect_mcp_http())
