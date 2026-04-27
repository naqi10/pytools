from __future__ import annotations

from pytools.dev.dead_imports import dead_imports


def test_finds_unused() -> None:
    src = "import os\nimport sys\nprint(sys.argv)\n"
    assert dead_imports(src) == [(1, "os")]


def test_no_dead() -> None:
    src = "import os\nprint(os.getcwd())\n"
    assert dead_imports(src) == []


def test_from_import() -> None:
    src = "from pathlib import Path, PurePath\nPath('.')\n"
    assert dead_imports(src) == [(1, "PurePath")]


def test_aliased_import() -> None:
    src = "import numpy as np\nimport pandas as pd\nnp.array([])\n"
    assert dead_imports(src) == [(2, "pd")]


def test_attribute_access_counts_as_use() -> None:
    src = "import os\nx = os.path.join('a', 'b')\n"
    assert dead_imports(src) == []


def test_star_import_ignored() -> None:
    src = "from os import *\n"
    assert dead_imports(src) == []
