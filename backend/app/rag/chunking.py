"""Split chapter text into overlapping chunks."""


def chunk_text(text: str, max_chars: int = 1800, overlap: int = 200) -> list[str]:
    """Sliding window with newline-aware breaks and overlap between chunks."""
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start, n = 0, len(text)
    while start < n:
        end = min(start + max_chars, n)
        window = text[start:end]
        if end < n:
            # prefer breaking at a paragraph/line boundary in the back half
            nl = window.rfind("\n")
            if nl > max_chars // 2:
                end = start + nl
                window = text[start:end]
        piece = window.strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start = max(end - overlap, start + 1)  # always advance -> no infinite loop
    return chunks


def build_chunk(book_title: str, chapter_title: str, chunk: str) -> str:
    """Breadcrumb prefix so the embedding carries book/chapter context."""
    return f"{book_title} > {chapter_title}:\n{chunk}"
