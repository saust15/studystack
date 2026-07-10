"""EPUB -> list of chapters."""
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


@dataclass
class Chapter:
    title: str
    text: str
    order: int


def _html_to_text(html: bytes) -> tuple[str | None, str]:
    """One XHTML doc -> (chapter_title, clean_text)."""
    soup = BeautifulSoup(html, "lxml")
    heading = soup.find(["h1", "h2"])
    title = heading.get_text(strip=True) if heading else None
    for tag in soup(["script", "style"]):  # strip non-content
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return title, text


def load_epub(path: str | Path) -> list[Chapter]:
    """An epub is a zip of XHTML docs; ebooklib iterates them in spine order."""
    book = epub.read_epub(str(path))
    chapters: list[Chapter] = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        title, text = _html_to_text(item.get_content())
        if len(text) < 200:  # covers, TOC, front matter
            continue
        chapters.append(Chapter(title=title or "Untitled", text=text, order=len(chapters)))
    return chapters
