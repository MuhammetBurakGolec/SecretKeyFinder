import re

def find_template_text(text):
    pattern = r"\$\{\{ [\w\W]+ \}\}"
    pattern_2 = r"\$\{\{[\w\W]+\}\}"
    match = re.search(pattern, text)
    match_2 = re.search(pattern_2, text)

    if match or match_2:
        return True
    else:
        return False