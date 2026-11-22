# for time checking mcp

TIME_MCP_CONNECTION = {
    "time": {
        "transport": "stdio",
        "command": "uvx",
        "args": [
            "mcp-server-time",
            "--local-timezone=Asia/Shanghai"
        ]
    },
}