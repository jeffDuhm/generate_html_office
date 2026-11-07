class SiteNotFoundError(Exception):
    def __init__(self):
        super().__init__("Site not found")

class SiteNameAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("A site with this name already exists")

class SiteHasRelatedRecordsError(Exception):
    def __init__(self):
        super().__init__("Site has related records and cannot be deleted. Deactivate it instead")

class SiteInvalidUpdateError(Exception):
    def __init__(self):
        super().__init__("Invalid fields to update")