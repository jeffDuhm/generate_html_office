class UrlReplacementNotFoundError(Exception):
    def __init__(self):
        super().__init__("URL replacement not found")

class UrlReplacementAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("A URL replacement with this source_url already exists")

class InvalidUrlReplacementUpdateError(Exception):
    def __init__(self):
        super().__init__("No valid fields to update")
        
class UrlReplacementDeleteError(Exception):
    def __init__(self):
        super().__init__("URL replacement could not be deleted")