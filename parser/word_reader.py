from docx.text.run import Run
from docx.text.hyperlink import Hyperlink
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl

class WordReader:
    
    def __init__(self, rules):
        
        self.rules = rules
        
    def parse_document(self, doc):
        
        blocks = []
        
        for block in self._iter_document_blocks(doc):
            
            parse_block = self._parse_block(block)
            
            if parse_block:
                blocks.append(parse_block)
            
        return blocks
    
    def _parse_block(self, block):
        
        if isinstance(block, Paragraph):
            
            return self._parse_paragraph_block(block)

        elif isinstance(block, Table):
            
            return self._parse_table(block)
        
    def _parse_paragraph_block(self, block):
        
        if not block.text.strip():
    
            return None
    
        style = block.style.name
        
        if style.startswith("Heading"):
                    
            return self._parse_heading(block)
            
        elif style == "List Paragraph":
            
            return self._parse_list_item(block)
            
        elif style == "Normal":
            
            widget = self._parse_widget(block)
            
            if widget:
                
                return widget
            
            return self._parse_paragraph(block)

    def _iter_document_blocks(self, doc):
        
        for element in doc.element.body:

            if isinstance(element, CT_P):

                yield Paragraph(element, doc)

            elif isinstance(element, CT_Tbl):

                yield Table(element, doc)
    
    def _parse_heading(self, paragraph):
        
        style = paragraph.style.name
    
        # Obtiene el numero de nivel (ej: "Heading 2" -> 2)
        level = int(style.split()[-1])
        
        return {
            "type": "heading",
            "level": level,
            "text": paragraph.text
        }
    
    def _parse_paragraph(self, paragraph):
        
        content = self._extract_content(paragraph)

        return {
            "type": "paragraph",
            "content": content
        }
    
    def _parse_list_item(self, paragraph):
        
        content = self._extract_content(paragraph)
    
        return {
            "type": "list_item",
            "content": content
        }

    def _parse_widget(self, paragraph):
        
        widget = self._find_widget(paragraph.text)

        if not widget:
            return None
        
        return {
            "type": "widget",
            "widget_id": widget["id"],
        }
    
    def _parse_table(self, table):
        
        table_rows = []

        for row in table.rows:

            rows_cells = []
            
            for cell in row.cells:
                
                cell_paragraphs = []
                
                for paragraph in cell.paragraphs:
                    
                    paragraph_content = self._extract_content(paragraph)
                    
                    cell_paragraphs.append(paragraph_content)

                rows_cells.append(cell_paragraphs)
                    
            table_rows.append(rows_cells)
            
        return {
            "type": "table",
            "rows": table_rows
        }
    
    def _extract_content(self, paragraph):
        content = []

        for item in paragraph.iter_inner_content():
            
            if isinstance(item, Run):
            
                content.append(self._parse_run(item))
                
            elif isinstance(item, Hyperlink):
            
                content.append(self._parse_hyperlink(item))
        
        return content
    
    def _parse_run(self, item):
        
        return {
            "text": item.text,
            "bold": bool(item.bold),
            "link": False
        }
        
    def _parse_hyperlink(self, item):
        
        return {
            "text": item.text,
            "bold": False,
            "link": item.address
        }
    
    def _find_widget(self, text):
        
        text = text.lower().strip()
        
        for widget in self.rules["widgets"]:
            
            for match in widget["match"]:
            
                if text == match.lower().strip():
                    
                    return widget
                
        return None
