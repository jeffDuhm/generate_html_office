
# Normaliza estructura de datos por tipos
def normalize_blocks(blocks):
    
    normalized_blocks = []

    current_list_items = []
    
    for block in blocks:

        if block["type"] == "list_item":
            
            current_list_items.append(block["text"])
            
        else:
            
            if current_list_items:
                
                normalized_blocks.append({
                    "type": "list",
                    "items": current_list_items
                })
                
                current_list_items = []
                
            normalized_blocks.append(block)
            
    if current_list_items:
        
        normalized_blocks.append({
            "type": "list",
            "items": current_list_items
        })
    
    return normalized_blocks