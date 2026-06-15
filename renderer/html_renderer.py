def render_content(content):

    html_content = ""
    
    for piece in content:
        
        if not piece["bold"]:
            
            html_content += piece["text"]
        else:
            html_content += f'<strong>{piece["text"]}</strong>'
            
    return html_content

def renderer_html(blocks, rules):
    
    html = ""
    open_section = False
    
    for block in blocks:
        
        if block["type"] in ["heading", "paragraph", "list"]:

            if not open_section:
                html += "<p>[open-section]</p>"
                open_section = True

        if block["type"] == "heading":
            html += f'<h{block["level"]}>{block["text"]}</h{block["level"]}>'
        
        elif block["type"] == "paragraph":
            
            paragraph_content = render_content(block["content"])
            
            html += f'<p>{paragraph_content}</p>'
        
        elif block["type"] == "list":
            
            list_items = ""
            
            for item in block["items"]:
                
                item_content = render_content(item)

                list_items += f"<li>{item_content}</li>"
                
            html += f"<ul>{list_items}</ul>" 
        
        elif block["type"] == "widget":
            
            if open_section:
                html+=f'<p>[close-section]</p>'
                open_section = False
            
            for widget in rules["widgets"]:
                if widget["id"] == block["widget_id"]:
                    html += f'<p>{widget["output"]}</p>'
                    break
    if open_section:
        html += f'<p>[close-section]</p>'
            
    return html