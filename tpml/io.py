from pathlib import Path
import sexpdata

BASE_PATH = Path(__file__).parent.parent.absolute()


def load_scm(filename):
    with (BASE_PATH / filename).open() as f:
        result = sexpdata.load(f)
    return result
