from blocks.list import ListBlock
from blocks.paragraph import ParagraphBlock
from blocks.heading import HeadingBlock
from blocks.table import TableBlock
from blocks.widget import WidgetBlock

class HTMLRenderer:
    
    def __init__(self, rules):
        self.rules = rules
        
    def render_document(self, blocks):
    
        html = []
        open_section = False
        use_sections = self.rules["use_sections"]
        
        for block in blocks:
            
            if (
                use_sections
                and isinstance(block, (HeadingBlock, ParagraphBlock, ListBlock))
            ):
                if not open_section:
                    
                    html.append("<p>[open-section]</p>")
                        
                    open_section = True
            
            if isinstance(block, ParagraphBlock):
                
                html.append(self._render_paragraph(block))
                
            elif isinstance(block, HeadingBlock):
                
                html.append(self._render_heading(block))
            
            elif isinstance(block, ListBlock):
                
                html.append(self._render_list(block))
            
            elif isinstance(block, TableBlock):
                
                html.append(self._render_table(block))
                
            elif isinstance(block, WidgetBlock):
                
                if use_sections and open_section:
                    
                    html.append(f'<p>[close-section]</p>')
                    
                    open_section = False
                
                html.append(self._render_widget(block))
                    
        if use_sections and open_section:
            
            html.append(f"<p>[close-section]</p>")
                
        return "".join(html)
    
    def _render_content(self, content):

        html_content = []
        
        for piece in content:
            
            link = piece["link"]
            text = piece["text"]
            
            if link:
                
                special_button = self._find_special_button(text)
                
                if special_button:
        
                    html_content.append(
                        f'<button class="js-hero-home-more-button">'
                        f'{text}'
                        f'</button>'
                    )
                
                elif self._is_phone_link(link):
                    
                    html_content.append(f'<a href="{link}">{text}</a>')
                    
                else:
                    
                    new_url = self._transform_link(link)
                
                    html_content.append(f'<a href="{new_url}" target="_blank">{text}</a>')
            
            elif piece["bold"]:
                
                html_content.append(f"<strong>{text}</strong>")
                
            else:
                
                html_content.append(text)
                
        return "".join(html_content)

    def _render_heading(self, block):
        
        return f'<h{block.level}>{block.text}</h{block.level}>'

    def _render_paragraph(self, block):
        
        paragraph_content = self._render_content(block.content)
        
        return f'<p>{paragraph_content}</p>'

    def _render_list(self, block):
        
        list_items = []
        
        for item in block.items:
            
            item_content = self._render_content(item)
            
            list_items.append(f"<li>{item_content}</li>")
        
        return f"<ul>{''.join(list_items)}</ul>"

    def _render_table(self, block):
        
        rows_html = []
        
        for row_index, row in enumerate(block.rows):
            
            cells_html = []
            
            cell_tag = "th" if row_index == 0 else "td"
            
            for cell in row:
                
                paragraphs_html = []
                
                for paragraph in cell:
                    
                    paragraph_content = self._render_content(paragraph)
                    
                    paragraphs_html.append(f"<p>{paragraph_content}</p>")
                
                cells_html.append(f"<{cell_tag}>{''.join(paragraphs_html)}</{cell_tag}>")
            
            rows_html.append(f"<tr>{''.join(cells_html)}</tr>")
        
        return f"<table><tbody>{''.join(rows_html)}</tbody></table>"

    def _render_widget(self, block):
        
        for widget in self.rules["widgets"]:
            
            if widget["id"] == block.id:
                
                return f"<p>{widget['output']}</p>"

        return ""

    def _find_special_button(self, text):
        
        text = text.lower().strip()
        
        for button in self.rules["special_buttons"]:
            
            for match in button["match"]:

                if text == match.lower().strip():
                
                    return button
            
        return None
    
    def _is_phone_link(self, url):
        
        return url.startswith("tel:")

    def _transform_link(self, url):
        
        for replacement in self.rules["link_replacements"]:
            
            if url.startswith(replacement["from"]):
                
                url = url.replace(
                    replacement["from"], 
                    replacement["to"]
                )
                
                break
                
        return url


        
