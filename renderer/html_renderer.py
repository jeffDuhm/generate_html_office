
def renderer_html(blocks):
    
    html = ""
    
    for block in blocks:
        
        if block["type"] == "heading":
            html += f"<h{block["level"]}>{block["text"]}</h{block["level"]}>"
        
        elif block["type"] == "paragraph":
            html += f"<p>{block["text"]}</p>"
            
    return html
            
