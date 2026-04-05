import psutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SystemInfo")
print("Mcp started")
@mcp.tool()
def cpu_usage() -> str:
    """Get current CPU usage percentage."""
    return f"{psutil.cpu_percent(interval=1)}%"

@mcp.tool()
def memory_usage() -> str:
    """Get memory usage details."""
    mem = psutil.virtual_memory()
    return f"Total: {mem.total / (1024**3):.1f} GB, Used: {mem.used / (1024**3):.1f} GB ({mem.percent}%)"

@mcp.tool()
def disk_usage(path: str = "/") -> str:
    """Get disk usage for a given path."""
    disk = psutil.disk_usage(path)
    return f"Total: {disk.total / (1024**3):.1f} GB, Used: {disk.used / (1024**3):.1f} GB ({disk.percent}%)"

if __name__ == "__main__":
    mcp.run()

#python system_server.py