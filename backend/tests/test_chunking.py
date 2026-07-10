from app.rag.chunking import chunk_text


def test_short_text_is_single_chunk():
    assert chunk_text("hello world", max_chars=100) == ["hello world"]


def test_empty_text_returns_empty_or_single_blank_free_list():
    assert chunk_text("", max_chars=100) in ([], [""])


def test_chunks_respect_max_chars():
    text = "word " * 2000
    for c in chunk_text(text, max_chars=500, overlap=50):
        assert len(c) <= 500


def test_chunks_overlap():
    text = "".join(f"line {i}\n" for i in range(400))
    chunks = chunk_text(text, max_chars=600, overlap=150)
    assert len(chunks) > 1
    # some tail of chunk[0] should appear in chunk[1]
    tail = chunks[0][-50:]
    assert tail[:20] in text  # sanity
    assert any(tail[i : i + 30] in chunks[1] for i in range(0, 20))


def test_loop_terminates_on_text_without_newlines():
    text = "x" * 10_000
    chunks = chunk_text(text, max_chars=1000, overlap=100)
    assert len(chunks) >= 10
