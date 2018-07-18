from distutils.cmd import Command
from pathlib import Path

class UploadCommand(Command):
    description = "use Twine to upload your package."
    # TODO: Allow specifying +dist+ directory.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from twine.cli import dispatch as twine
        files = map(str, Path().glob("dist/*"))
        twine(["upload", *files])
