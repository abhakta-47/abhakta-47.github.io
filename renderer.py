import re
import os

INCLUDE_PATTERN = re.compile(r'{%\s*include\s+"([^"]+)"\s*%}')

def render_template(filepath, basedir=None):
    basedir = basedir or os.path.dirname(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def include_replacer(match):
        included_file = match.group(1)
        included_path = os.path.join(basedir, included_file)
        if not os.path.isfile(included_path):
            return f"<!-- Included file not found: {included_file} -->"
        return render_template(included_path, basedir)

    # Recursively replace includes
    while INCLUDE_PATTERN.search(content):
        content = INCLUDE_PATTERN.sub(include_replacer, content)

    return content

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python simple_template.py index.html")
        sys.exit(1)

    output = render_template(sys.argv[1])
    print(output)
