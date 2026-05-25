from docx import Document
import json

doc = Document("./input/test_office.docx")

with open("config/rules.json", "r") as file:
    rules = json.load(file)

def is_widget(text,rules):
    
    for widget in rules["widgets"]:
        
        if text in widget["match"]:
            return widget
    return None

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
        blocks.append({
            "type": "list_item",
            "text": text
        })
        
    elif style == "Normal":
        
        widget = is_widget(text, rules)
        
        if widget:
            blocks.append({
                "type": "widget",
                "widget_id": widget["id"],
            })
        
        else:
            
            blocks.append({
                "type": "paragraph",
                "text": text
            })
                
print(blocks)