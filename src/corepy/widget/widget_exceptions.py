class WidgetNotFoundError(Exception):
    def __init__(self):
        super().__init__("Widget not found")

class WidgetShortcodeAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("A widget with this shortcode already exists in this site")
        
class WidgetHasRelatedRecordsError(Exception):
    def __init__(self):
        super().__init__("Widget has related records and cannot be deleted. Deactive it instead")
        
class WidgetInvalidUpdateError(Exception):
    def __init__(self):
        super().__init__("Invalid fields to update")