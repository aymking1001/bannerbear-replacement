import sys
import json


def main():
    if len(sys.argv) != 2:
        print("Usage: python renderer.py <input.json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Template 1 renderer")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
