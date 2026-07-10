"""CLI question against the bookshelf."""
import argparse

from app.rag.pipeline import answer, retrieve


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("question")
    p.add_argument("-k", type=int, default=5)
    args = p.parse_args()

    chunks = retrieve(args.question, args.k)
    print("--- Retrieved (closest first) ---")
    for c in chunks:
        print(f"  [{c.distance:.3f}] {c.book} - {c.chapter}: {c.content[:80]!r}")
    print("\n--- Answer ---")
    print(answer(args.question, chunks))


if __name__ == "__main__":
    main()
