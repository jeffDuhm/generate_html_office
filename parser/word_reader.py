from docx.text.run import Run
from docx.text.hyperlink import Hyperlink

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
    
def read_word_document(doc, rules):
    
    blocks = []
    
    for paragraph in doc.paragraphs:
    
        style = paragraph.style.name
                
        if not paragraph.text.strip():
            continue
        
        if style.startswith("Heading"):
            
            blocks.append(parse_heading(paragraph))
            
        elif style == "List Paragraph":
            
            blocks.append(parse_list_item(paragraph))
            
        elif style == "Normal":
            
            widget = parse_widget(paragraph, rules)
            
            if widget:
                
                blocks.append(widget)
            
            else:
        
                blocks.append(parse_paragraph(paragraph))

    return blocks
