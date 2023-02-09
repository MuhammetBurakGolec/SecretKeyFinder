import re

def find_template_text(text):
    pattern = r"\$\{\{ [a-zA-Z0-9_]+ \}\}"
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False