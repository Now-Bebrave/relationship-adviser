# Illustration rules

Generate PNG or SVG illustrations only when a diagram or conceptual image improves comprehension. Record the image purpose, alt text, generator or source, and a Markdown/table fallback.

If image generation is unavailable, continue with the same conclusion, steps, reactions, and responses in text. Visual output never replaces an actionable recommendation.

## Portable request contract

The dependency-free helper `tools/visual_output.py` provides the shared contract:

- `should_render_visual(...)` triggers a visual for more than two branches, multiple time points, three or more options, or an abstract concept;
- `build_illustration_request(...)` requires purpose, alt text, source, prompt, and a fallback;
- `render_text_fallback(...)` produces a Markdown table with the same branches.

Adapters may pass the request to a platform image tool. If that tool is unavailable, they must return the generated fallback and keep the same conclusion and actions.
