from docx.text.run import Run
from docx.text.hyperlink import Hyperlink
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl

def extract_content(paragraph):
    content = []
    
    for item in paragraph.iter_inner_content():
        
        if isinstance(item, Run):
    
            content.append({
                "text": item.text,
                "bold": bool(item.bold),
                "link": False
            })
            
        elif isinstance(item, Hyperlink):
            
            content.append({
                "text": item.text,
                "bold": False,
                "link": item.address
            })
    
    return content

def find_widget(text,rules):
    
    text = text.lower().strip()
    
    for widget in rules["widgets"]:
        
        for match in widget["match"]:
        
            if text == match.lower().strip():
                
                return widget
            
    return None

def parse_heading(paragraph):
    
    style = paragraph.style.name
    
    # Obtiene el numero de nivel (ej: "Heading 2" -> 2)
    level = int(style.split()[-1])
    
    return {
        "type": "heading",
        "level": level,
        "text": paragraph.text
    }
    
def parse_list_item(paragraph):
    
    content = extract_content(paragraph)
    
    return {
        "type": "list_item",
        "content": content
    }

def parse_widget(paragraph, rules):
    
    widget = find_widget(paragraph.text, rules)
    
    if not widget:
        return None
    
    return {
        "type": "widget",
        "widget_id": widget["id"],
    }

def parse_paragraph(paragraph):
    
    content = extract_content(paragraph)
    
    return {
        "type": "paragraph",
        "content": content
    }
    
def parse_table(table):
    
    table_rows = []
    
    for row in table.rows:

        rows_cells = []
        
        for cell in row.cells:
            
            cell_paragraphs = []
            
            for paragraph in cell.paragraphs:
                
                paragraph_content = extract_content(paragraph)
                
                cell_paragraphs.append(paragraph_content)

            rows_cells.append(cell_paragraphs)
                
        table_rows.append(rows_cells)
        
    return {
        "type": "table",
        "rows": table_rows
    }
    
def iter_document_blocks(doc):
    
    for element in doc.element.body:

        if isinstance(element, CT_P):

            yield Paragraph(element, doc)

        elif isinstance(element, CT_Tbl):

            yield Table(element, doc)
    
def read_word_document(doc, rules):
    
    blocks = []
    
    for block in iter_document_blocks(doc):
        
        if isinstance(block, Paragraph):
            
        
            style = block.style.name
                    
            if not block.text.strip():
                continue
            
            if style.startswith("Heading"):
                
                blocks.append(parse_heading(block))
                
            elif style == "List Paragraph":
                
                blocks.append(parse_list_item(block))
                
            elif style == "Normal":
                
                widget = parse_widget(block, rules)
                
                if widget:
                    
                    blocks.append(widget)
                
                else:
            
                    blocks.append(parse_paragraph(block))
                    
        elif isinstance(block, Table):
            blocks.append(parse_table(block))
        
    return blocks
