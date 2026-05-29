
def renderer_html(blocks):
    
    html = ""
    
    for block in blocks:
        
        if block["type"] == "heading":
            html += f'<h{block["level"]}>{block["text"]}</h{block["level"]}>'
        
        elif block["type"] == "paragraph":
            html += f'<p>{block["text"]}</p>'
        
        elif block["type"] == "list":
            
            list_items = ""
            
            for item in block["items"]:
                list_items += f"<li>{item}</li>"
                
            html += f"<ul>{list_items}</ul>"
            
    return html
            
