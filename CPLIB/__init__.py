from . import Cpanel
from .Cpanel import FileManager

class Main(Cpanel.Cpanel, FileManager.FileManager):
    def __init__(self):
        super().__init__()
