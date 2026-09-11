from docx import Document

from parser.word_reader import WordReader
from renderer.html_renderer import HTMLRenderer
from normalizers.blocks_normalizer import BlockNormalizer

class WordToHtmlConverter:
    def __init__(self, word_file_path, rules):
        self.word_file_path = word_file_path
        self.rules = rules
        
    def convert(self):
        
        doc = Document(self.word_file_path)
        
        reader = WordReader(self.rules)

        blocks = reader.parse_document(doc)

        normalizer = BlockNormalizer(blocks)
        normalized_blocks = normalizer.normalize()

        renderer = HTMLRenderer(self.rules)
        html_content = renderer.render_document(normalized_blocks)

        return html_content