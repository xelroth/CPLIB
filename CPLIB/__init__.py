from . import Cpanel

class Main(Cpanel.Cpanel,FileManager.FileManager):
    def __init__(self) -> None:
    super().__init__()
