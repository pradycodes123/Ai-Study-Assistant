import re
from typing import List
from urllib.parse import quote_plus

def chunk_text(text: str, target_size: int = 4000) -> List[str]:
    """
    Splits text into chunks of approximately target_size characters,
    respecting word boundaries to avoid cutting words in half.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        # +1 for the space
        if current_length + len(word) + 1 > target_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        
        current_chunk.append(word)
        current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks


def youtube_links(result: str) -> str:
    """
    Detects lines that look like YouTube search terms and adds links.
    Expects lines in the 'YOUTUBE:' section to be like '1. Search Term'
    """
    lines = result.splitlines()
    formatted = []
    in_youtube_section = False

    item_pattern = re.compile(r"^(\d+)\.\s+(.+)$")

    for line in lines:
        stripped = line.strip()
        
        # Simple detection of the "YOUTUBE" section header
        if "youtube" in stripped.lower() and (stripped.endswith(":") or stripped.startswith("#")):
            in_youtube_section = True
            formatted.append(line)
            continue
        
        if in_youtube_section:
            match = item_pattern.match(stripped)
            if match:
                number = match.group(1)
                title = match.group(2).strip()
                # Create a search link
                query = quote_plus(title)
                link = f"{number}. [{title}](https://www.youtube.com/results?search_query={query})"
                formatted.append(link)
                continue
            
            if stripped.startswith("#"):
                in_youtube_section = False
                formatted.append(line)
                continue
                
        formatted.append(line)

    return "\n".join(formatted)
