from fastmcp import FastMCP

# initialize mcp

mcp = FastMCP("math")

# start mcp service, set transport to stdio
if __name__ == "__main__":
    mcp.run(transport="stdio")