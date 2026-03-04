import textwrap

def build_prompt(text: str) -> str:
    prompt = f"""\
You are an academic assistant.

Tasks:
1. Write a concise summary (bullet points only, no prose, 5–7 bullets, 1–2 lines max each, focused on definitions, syntax, and key concepts)
2. Create 5–6 quiz questions with short answers (use a numbered list with bold Question/Answer labels)
3. Give exactly 3 YouTube search terms (numbered list of search terms only)

Rules:
- Use only the provided text
- Be concise and technical
- Avoid repetition
- If the text contains insufficient content to generate meaningful notes, respond with only: "### Skipped\\nInsufficient content."

Text:
{text}

Format strictly as Markdown:

### Summary
- point 1
- point 2

### Quiz
1. **Question:** ...
   **Answer:** ...
2. **Question:** ...
   **Answer:** ...

### YouTube Search Terms
1. Search Term 1
2. Search Term 2
3. Search Term 3
"""
    return prompt