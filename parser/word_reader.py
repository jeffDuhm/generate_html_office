def extract_content(paragraph):
    content = []
        
    for run in paragraph.runs:
        
        content.append({
            "text": run.text,
            "bold": bool(run.bold)
        })
    
    return content

def find_widget(text,rules):
    
    for widget in rules["widgets"]:
        
        if text in widget["match"]:
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
