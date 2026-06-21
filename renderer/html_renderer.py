def find_special_button(text, rules):
    
    for button in rules["special_buttons"]:
        
        if text.lower().strip() in button["match"]:
            
            return button
        
    return None

def is_phone_link(url):
    
    return url.startswith("tel:")

def transform_link(url, rules):
    
    for replacement in rules["link_replacements"]:
        
        if url.startswith(replacement["from"]):
            
            url = url.replace(
                replacement["from"], 
                replacement["to"]
            )
            
            break
            
    return url

def render_content(content, rules):

    html_content = ""
    
    for piece in content:
        
        if piece["link"]:
            
            button = find_special_button(piece["text"], rules)
            
            if button:
    
                html_content += (
                    f'<button class="js-hero-home-more-button">'
                    f'{piece["text"]}'
                    f'</button>'
                )
            
            elif is_phone_link(piece["link"]):
                
                html_content += f'<a href="{piece["link"]}">{piece["text"]}</a>'
                
            else:
                
                new_url = transform_link(piece["link"], rules)
            
                html_content += f'<a href="{new_url}" target="_blank">{piece["text"]}</a>'
        
        elif piece["bold"]:
            
            html_content += f'<strong>{piece["text"]}</strong>'
            
        else:
            
            html_content += piece["text"]
            
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
            
            paragraph_content = render_content(block["content"], rules)
            
            html += f'<p>{paragraph_content}</p>'
        
        elif block["type"] == "list":
            
            list_items = ""
            
            for item in block["items"]:
                
                item_content = render_content(item, rules)

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