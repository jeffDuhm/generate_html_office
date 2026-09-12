from parser.word_reader import WordReader
from renderer.html_renderer import HTMLRenderer
from normalizers.blocks_normalizer import BlockNormalizer

class WordToHtmlConverter:
    def __init__(self, document, rules):
        self.document = document
        self.rules = rules
        
    def convert(self):
        
        reader = WordReader(self.rules)

        blocks = reader.parse_document(self.document)

        normalizer = BlockNormalizer(blocks)
        normalized_blocks = normalizer.normalize()

        renderer = HTMLRenderer(self.rules)
        html_content = renderer.render_document(normalized_blocks)

        return html_content