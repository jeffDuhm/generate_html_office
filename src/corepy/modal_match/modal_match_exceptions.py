class ModalMatchNotFoundError(Exception):
    def __init__(self):
        super().__init__("Modal match not found")

class ModalMatchConflictError(Exception):
    def __init__(self):
        super().__init__("This text is already used by another modal match of the same site")

class SiteNotFoundError(Exception):
    def __init__(self):
        super().__init__("Site not found or inactive")

class InvalidModalMatchUpdateError(Exception):
    def __init__(self):
        super().__init__("Invalid fields to update")