class NoFilesError(Exception):
    def __init__(self):
        super().__init__("No files were uploaded")

class InvalidFileTypeError(Exception):
    def __init__(self):
        super().__init__("Only .docx files are allowed")