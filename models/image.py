from models.file import File

class Image(File):
    def __init__(self, path, name, extension, format, height, width):
        super().__init__(path, name, extension, format)
        self.height = height
        self.width = width
