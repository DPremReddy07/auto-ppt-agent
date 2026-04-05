# =============================================
# content_server.py  –  MCP Server #2: Content
# =============================================
# This server gives the agent 2 extra tools:
#   1. generate_outline  – plan all slide titles for a topic
#   2. enrich_slide      – generate bullet points for a slide
#
# Why a separate server?
#   The assignment requires ≥ 2 MCP servers for full marks.
#   This server handles "thinking about content" while ppt_server
#   handles "building the file". Clean separation of concerns!
#
# NOTE: This server does NOT call the internet.
#       It uses its built-in logic to generate content.
#       (In a real project you'd call a search API here.)
# =============================================

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("content-server")


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 1 – Generate a slide outline for any topic
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def generate_outline(
    topic: str,
    num_slides: int = 5,
    audience: str = "general"
) -> str:
    """
    Plans the slide titles for a presentation before any content is written.
    The agent MUST call this first (before add_slide) to satisfy the
    'planning before executing' requirement of the assignment.

    Args:
        topic:      The subject of the presentation (e.g. 'life cycle of a star')
        num_slides: How many slides to plan (including title + conclusion).
                    Minimum 3, maximum 10.
        audience:   Who will watch it – affects vocabulary level.
                    Options: 'children', 'middle school', 'high school',
                             'college', 'general', 'professional'

    Returns:
        A JSON object with:
          - presentation_title
          - filename  (suggested safe filename)
          - audience
          - slides: list of {slide_number, type, title, guidance}
    """
    num_slides = max(3, min(10, int(num_slides)))

    # Build a structured outline
    # Slide 1  = Title slide
    # Slide N  = Conclusion / Summary
    # Everything in between = content slides
    content_count = num_slides - 2  # subtract title + conclusion

    slides = []

    # ── Slide 1: Title ────────────────────────────────────────────────────────
    slides.append({
        "slide_number": 1,
        "type": "title",
        "title": topic.title(),
        "guidance": (
            f"Big bold title. Add a one-line subtitle describing the scope "
            f"and the target audience ({audience})."
        )
    })

    # ── Content slides ────────────────────────────────────────────────────────
    content_hints = _content_structure(content_count)
    for i, hint in enumerate(content_hints, start=2):
        slides.append({
            "slide_number": i,
            "type": "content",
            "title": f"[Write a title about: {hint} related to '{topic}']",
            "guidance": (
                f"Provide 3–5 factual bullet points about '{hint}' in the context "
                f"of '{topic}'. Tailor language for a {audience} audience. "
                "Each bullet should be a complete, informative sentence."
            )
        })

    # ── Last slide: Conclusion ────────────────────────────────────────────────
    slides.append({
        "slide_number": num_slides,
        "type": "content",
        "title": "Summary & Key Takeaways",
        "guidance": (
            "Recap the 3-5 most important facts from the entire presentation. "
            "End with one thought-provoking question or call-to-action."
        )
    })

    # Build safe filename from topic
    safe_name = topic.lower().strip()
    for ch in " /\\:*?\"<>|":
        safe_name = safe_name.replace(ch, "_")
    safe_name = safe_name[:40] + ".pptx"

    outline = {
        "presentation_title": topic.title(),
        "filename": safe_name,
        "audience": audience,
        "total_slides": num_slides,
        "slides": slides
    }

    return json.dumps(outline, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 2 – Generate bullet-point content for a specific slide
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def enrich_slide(
    topic: str,
    slide_title: str,
    audience: str = "general",
    num_bullets: int = 4
) -> str:
    """
    Generates a list of bullet points for a given slide title.
    Call this for each content slide to get structured bullet point ideas.

    Args:
        topic:       The overall presentation topic.
        slide_title: The title of this specific slide.
        audience:    Vocabulary level ('children', 'middle school', etc.)
        num_bullets: How many bullet points to generate (3–5 recommended).

    Returns:
        A JSON object with:
          - slide_title
          - bullets: list of bullet point strings
          - speaker_note: one sentence to help the presenter
    """
    num_bullets = max(3, min(5, int(num_bullets)))

    # Vocabulary guidance based on audience
    vocab_guide = {
        "children":       "Use very simple words (age 6-10). Short sentences. Fun examples.",
        "middle school":  "Use clear language (age 11-13). Relatable analogies. Avoid jargon.",
        "high school":    "Use proper terminology (age 14-17). Encourage critical thinking.",
        "college":        "Use academic language. Cite concepts precisely.",
        "general":        "Use plain English. Assume no prior knowledge.",
        "professional":   "Use domain-specific vocabulary. Be concise and data-driven.",
    }.get(audience, "Use plain English appropriate to the audience.")

    # Build template bullets — the agent will REPLACE these with real content
    bullet_templates = []
    for i in range(1, num_bullets + 1):
        bullet_templates.append(
            f"[Fact #{i}: Write one true, interesting fact about '{slide_title}' "
            f"in the context of '{topic}'. {vocab_guide}]"
        )

    result = {
        "slide_title": slide_title,
        "guidance": (
            f"Replace each placeholder below with actual knowledge about '{slide_title}'. "
            f"Audience: {audience}. {vocab_guide}"
        ),
        "bullets": bullet_templates,
        "speaker_note": (
            f"[Write one sentence you'd say out loud to introduce '{slide_title}' "
            f"to a {audience} audience.]"
        )
    }

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# Helper – distribute content slide themes across available slots
# ─────────────────────────────────────────────────────────────────────────────
def _content_structure(n: int) -> list:
    """
    Returns n content themes that work for almost any presentation topic.
    The agent uses these as a starting scaffold and replaces them with
    topic-specific titles.
    """
    all_themes = [
        "Introduction / What is it?",
        "How it works / The process",
        "Key stages or phases",
        "Important facts & examples",
        "Causes or origins",
        "Effects or impact",
        "Real-world applications",
        "Challenges or problems",
    ]
    # Cycle through themes if fewer slots than themes
    return [all_themes[i % len(all_themes)] for i in range(n)]


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🟢 Content MCP Server is running…", flush=True)
    mcp.run()