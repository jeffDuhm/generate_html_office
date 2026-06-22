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

def read_word_document(doc, rules):
    
    blocks = []
    
    for paragraph in doc.paragraphs:
    
        style = paragraph.style.name
        text = paragraph.text
                
        if not text.strip():
            continue
        
        if style == "Heading 2":
            blocks.append({
                "type": "heading",
                "level": 2,
                "text": text
            })
            
        elif style == "Heading 3":
            blocks.append({
                "type": "heading",
                "level": 3,
                "text": text
            })
            
        elif style == "List Paragraph":
            
            content = extract_content(paragraph)
            
            blocks.append({
                "type": "list_item",
                "content": content
            })
            
        elif style == "Normal":
            
            widget = find_widget(text, rules)
            
            if widget:
                blocks.append({
                    "type": "widget",
                    "widget_id": widget["id"],
                })
            
            else:
                
                content = extract_content(paragraph)
        
                blocks.append({
                        "type": "paragraph",
                        "content": content
                    })
                
    return blocks
