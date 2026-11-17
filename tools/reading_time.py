"""One reading clock for shell lessons and course registers (200 words/minute)."""
import re
from tools.lesson_check import Document, Node, BLOCK, excluded


def reading_words(page: str) -> int:
    chunks = []

    def visit(node):
        if (excluded(node) or node.tag in {'svg', 'canvas'}
                or node.classes.intersection({'topbar', 'kicker', 'hero-pos', 'hero-meta',
                                             'xq-ground', 'bet-ground', 'exam-ground'})):
            return
        if node.tag in BLOCK:
            chunks.append(' ')
        for child in node.children:
            if isinstance(child, Node):
                visit(child)
            else:
                chunks.append(child)
        if node.tag in BLOCK:
            chunks.append(' ')

    visit(Document(page).root)
    return len(re.findall(r'\b\w+\b', ''.join(chunks), re.UNICODE))


def reading_minutes(page: str) -> int:
    # Round half upwards to the nearest five minutes; a readable page gets at least five.
    return max(5, ((reading_words(page) + 500) // 1000) * 5)
