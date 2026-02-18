import re

class SecureRedactor:
    def __init__(self):
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "IPV4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "API_KEY": r'(?i)(api[-_]?key|secret|token)\s*[:=]\s*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?',
            "DB_URI": r'(postgresql|mysql|mongodb)://\S+'
        }

    def redact(self, text):
        redacted_text = text
        for label, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f'<{label}_REDACTED>', redacted_text)
        return redacted_text

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact sensitive information from text or files.")
    parser.add_argument("file", nargs="?", help="File to redact (optional). If not provided, reads from stdin.")
    parser.add_argument("--output", "-o", help="Output file to write to. Defaults to stdout.")
    args = parser.parse_args()

    redactor = SecureRedactor()
    
    # Read input
    if args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        # Demo mode if no input provided
        content = """
    Fix the bug in the database connector.
    Connection string: postgresql://admin:SuperSecretPassword123@localhost:5432/production_db
    API Token: sk-proj-1234567890abcdef1234567890abcdef
    """
        print("--- DEMO MODE (No input file or pipe detected) ---", file=sys.stderr)

    # Redact
    redacted_content = redactor.redact(content)

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(redacted_content)
        print(f"Redacted content written to {args.output}", file=sys.stderr)
    else:
        print(redacted_content)
