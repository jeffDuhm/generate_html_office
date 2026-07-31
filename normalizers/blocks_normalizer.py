from blocks.list import ListBlock
from blocks.list_item import ListItemBlock

# Normaliza estructura de datos por tipos
def normalize_blocks(blocks):
    
    normalized_blocks = []

    current_list_items = []
    
    for block in blocks:

        if isinstance(block, ListItemBlock):
            
            current_list_items.append(block.content)
            
        else:
            
            if current_list_items:
                
                normalized_blocks.append(ListBlock(current_list_items))
                
                current_list_items = []
                
            normalized_blocks.append(block)
            
    if current_list_items:
        
        normalized_blocks.append(ListBlock(current_list_items))
    
    return normalized_blocks