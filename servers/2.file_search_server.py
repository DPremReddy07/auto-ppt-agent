import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

WORKSPACE = Path("/home/user/workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)

mcp = FastMCP("FileSearch")

def safe_path(path: str) -> Path:
    resolved = (WORKSPACE / path).resolve()
    if WORKSPACE not in resolved.parents and resolved != WORKSPACE:
        raise PermissionError("Access denied")
    return resolved

@mcp.tool()
def find_by_name(pattern: str, directory: str = ".") -> str:
    """Find files whose name contains pattern."""
    try:
        target = safe_path(directory)
        results = []
        for root, dirs, files in os.walk(target):
            for file in files:
                if pattern in file:
                    rel = os.path.relpath(os.path.join(root, file), WORKSPACE)
                    results.append(rel)
        return "\n".join(results[:20]) or "No matches"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def find_by_content(text: str, directory: str = ".") -> str:
    """Find files containing text (grep style)."""
    try:
        target = safe_path(directory)
        results = []
        for root, dirs, files in os.walk(target):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        if text in f.read():
                            results.append(os.path.relpath(filepath, WORKSPACE))
                except:
                    continue
        return "\n".join(results[:20]) or "No matches"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()


# python file_search_client.py