def chunk_text(text, chunk_size=150):
    """Simple fixed-size text chunking."""
    sentences = text.split(". ")
    chunks = []

    curr = ""
    for s in sentences:
        if len(curr) + len(s) < chunk_size:
            curr += s + ". "
        else:
            chunks.append(curr.strip())
            curr = s + ". "

    if curr:
        chunks.append(curr.strip())

    return chunks