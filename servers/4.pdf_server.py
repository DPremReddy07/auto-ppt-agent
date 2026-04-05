import PyPDF2
from pathlib import Path
from mcp.server.fastmcp import FastMCP

WORKSPACE = Path("workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)
mcp = FastMCP("PDFExtractor")

def safe_path(path: str) -> Path:
    resolved = (WORKSPACE / path).resolve()
    if WORKSPACE not in resolved.parents and resolved != WORKSPACE:
        raise PermissionError("Access denied")
    return resolved

@mcp.tool()
def extract_text(filename: str, max_pages: int = 10) -> str:
    """Extract text from a PDF file."""
    try:
        filepath = safe_path(filename)
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = []
            for i, page in enumerate(reader.pages):
                if i >= max_pages:
                    break
                text.append(page.extract_text())
        return "\n\n".join(text)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()

# Place a PDF file named report.pdf in the workspace directory.