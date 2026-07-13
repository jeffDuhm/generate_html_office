def find_special_button(text, rules):
    
    text = text.lower().strip()
    
    for button in rules["special_buttons"]:
        
        for match in button["match"]:

            if text == match.lower().strip():
            
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

    html_content = []
    
    for piece in content:
        
        link = piece["link"]
        text = piece["text"]
        
        if link:
            
            special_button = find_special_button(text, rules)
            
            if special_button:
    
                html_content.append(
                    f'<button class="js-hero-home-more-button">'
                    f'{text}'
                    f'</button>'
                )
            
            elif is_phone_link(link):
                
                html_content.append(f'<a href="{link}">{text}</a>')
                
            else:
                
                new_url = transform_link(link, rules)
            
                html_content.append(f'<a href="{new_url}" target="_blank">{text}</a>')
        
        elif piece["bold"]:
            
            html_content.append(f"<strong>{text}</strong>")
            
        else:
            
            html_content.append(text)
            
    return "".join(html_content)

def render_heading(block):
    
    return f'<h{block["level"]}>{block["text"]}</h{block["level"]}>'

def render_paragraph(block, rules):
    
    paragraph_content = render_content(block["content"], rules)
    
    return f'<p>{paragraph_content}</p>'

def render_list(block, rules):
    
    list_items = []
    
    for item in block["items"]:
        
        item_content = render_content(item, rules)
        
        list_items.append(f"<li>{item_content}</li>")
    
    return f"<ul>{''.join(list_items)}</ul>"

def render_table(block, rules):
    
    rows_html = []
    
    for row_index, row in enumerate(block["rows"]):
        
        cells_html = []
        
        cell_tag = "th" if row_index == 0 else "td"
        
        for cell in row:
            
            paragraphs_html = []
            
            for paragraph in cell:
                
                paragraph_content = render_content(paragraph, rules)
                
                paragraphs_html.append(f"<p>{paragraph_content}</p>")
            
            cells_html.append(f"<{cell_tag}>{''.join(paragraphs_html)}</{cell_tag}>")
        
        rows_html.append(f"<tr>{''.join(cells_html)}</tr>")
    
    return f"<table><tbody>{''.join(rows_html)}</tbody></table>"

def render_widget(block, rules):
    
    for widget in rules["widgets"]:
        
        if widget["id"] == block["widget_id"]:
            
            return f"<p>{widget['output']}</p>"

    return ""
    
def renderer_html(blocks, rules):
    
    html = []
    open_section = False
    use_sections = rules["use_sections"]
    
    for block in blocks:
        
        if (
            use_sections
            and block["type"] in ["heading", "paragraph", "list"]
        ):

                if not open_section:
                    
                    html.append("<p>[open-section]</p>")
                    
                    open_section = True

        if block["type"] == "heading":
            
            html.append(render_heading(block))
        
        elif block["type"] == "paragraph":
            
            html.append(render_paragraph(block, rules))
        
        elif block["type"] == "list":
            
            html.append(render_list(block, rules))
        
        elif block["type"] == "table":
            
            html.append(render_table(block, rules))
            
        elif block["type"] == "widget":
            
            if use_sections and open_section:
                
                html.append(f'<p>[close-section]</p>')
                
                open_section = False
            
            html.append(render_widget(block, rules))
                
    if use_sections and open_section:
        
        html.append(f"<p>[close-section]</p>")
            
    return "".join(html)