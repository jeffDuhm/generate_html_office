class WidgetMatchNotFoundError(Exception):
    def __init__(self):
        super().__init__("Widget match not found")

class WidgetMatchConflictError(Exception):
    def __init__(self):
        super().__init__("This text is already used by another widget of the same site")
        
class WidgetNotFoundError(Exception):
    def __init__(self):
        super().__init__("Widget not found or inactive")
        
class InvalidWidgetMatchUpdateError(Exception):
    def __init__(self):
        super().__init__("Invalid fields to update")
        
class WidgetMatchInUseError(Exception):
    def __init__(self):
        super().__init__("Widget match in use")