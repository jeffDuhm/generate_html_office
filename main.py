from docx import Document
import json
from parser.word_reader import read_word_document
from renderer.html_renderer import renderer_html
from normalizers.blocks_normalizer import normalize_blocks

doc = Document("./input/freeway_en.docx")

with open("config/freeway.json", "r", encoding="utf-8") as file:
    rules = json.load(file)
    
blocks = read_word_document(doc, rules)

normalized_blocks = normalize_blocks(blocks)

html_strings = renderer_html(normalized_blocks, rules)

print(html_strings)