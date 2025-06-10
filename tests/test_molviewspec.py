import io
import os
import tempfile
import time
import json
from pathlib import Path
import biotite.database.rcsb as rcsb
import pytest
from biotite.structure.io import load_structure
import molecularnodes as mn
from molecularnodes.download import FileDownloadPDBError, StructureDownloader
from molecularnodes.molviewspec.molviewspec import MVSJ_Blender_Single_Tree, MVSJ_Blender
from .constants import codes


def test_load_minimal_mvsj():
    """Test loading and creating MVSJ_Blender_Single_Tree from minimal.mvsj file."""
    # Get the path to the test data file
    test_data_path = Path(__file__).parent / "data" / "molviewspec" / "minimal.mvsj"

    # Load the MVSJ file
    with open(test_data_path, 'r') as f:
        mvsj_data = json.load(f)

    # Create a MVSJ_Blender_Single_Tree instance
    single_tree = MVSJ_Blender(mvsj_data)

    # Basic assertions to verify the object was created
    assert single_tree is not None
    assert hasattr(single_tree, 'data')
    assert single_tree.data is not None

    # Save an Image
    single_tree.render()
