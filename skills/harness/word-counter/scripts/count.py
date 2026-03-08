"""Word Counter — 텍스트 통계 분석 스크립트"""
import sys, os

def count_text(text: str) -> dict:
    lines = text.count('\n') + 1 if text else 0
    words = len(text.split()) if text else 0
    chars = len(text)
    chars_no_space = len(text.replace(' ', '').replace('\n', '').replace('\r', ''))
    return {"lines": lines, "words": words, "chars": chars, "chars_no_space": chars_no_space}

def main():
    if len(sys.argv) < 2:
        print("Usage: python count.py <file_path>")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: '{path}' not found")
        sys.exit(1)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='cp949') as f:
            text = f.read()
    stats = count_text(text)
    print(f"Lines:  {stats['lines']}")
    print(f"Words:  {stats['words']}")
    print(f"Chars:  {stats['chars']}")
    print(f"Chars (no space): {stats['chars_no_space']}")

if __name__ == "__main__":
    main()
