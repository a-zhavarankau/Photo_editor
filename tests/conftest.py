import pytest
import os
from PIL import Image


@pytest.fixture
def fake_file():
    # Create pseudo-class files for testing get_file_name_and_ext()
    class PseudoDirEntry:
        def __init__(self, name):
            self.name = name
    return {'goodfile': PseudoDirEntry('goodname.py'),
            'badfile_1': PseudoDirEntry('.badname'),
            'badfile_2': PseudoDirEntry('badname.'),
            'badfile_3': PseudoDirEntry('badname')}

@pytest.fixture
def example_screenshot():
    img = Image.open("./working_files/example_scr_2880x1800.png")
    img.show()
    return img




