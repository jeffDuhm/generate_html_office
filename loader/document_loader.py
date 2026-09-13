from docx import Document
from pathlib import Path

class DocumentLoader:
    
    def __init__(self, input_dir):
        self.input_dir = input_dir
        
    def load(self):
        input_path = Path(self.input_dir)
        
        for file in input_path.glob("*.docx"):
            doc = Document(file)
            yield file, doc