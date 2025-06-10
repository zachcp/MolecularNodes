"""

MVSJ has the following that needs to be translated to MN:

# Data Load:
# root
# └── download (fetch structure data)
#     └── parse (interpret file format: mmcif, pdb, etc.)
#         └── structure (create 3D structure: model, assembly, etc.)
#
#
# Select components and apply styles
# structure
# └── component (select atoms/residues/chains)
#     ├── representation (cartoon, ball_and_stick, surface, etc.)
#     │   ├── color (styling)
#     │   ├── label (annotations)
#     │   ├── tooltip (hover info)
#     │   └── opacity (transparency)
#     └── focus (camera targeting)
#
# Primitive Handling:
#  root (or any level)
# └── primitives (grouping container)
#     ├── primitive (individual shapes)
#     │   ├── tube, arrow, box, ellipse
#     │   ├── distance_measurement
#     │   └── angle_measurement
#     └── primitives_from_uri (load external primitives)
#
# Globals
# root
# ├── camera (viewpoint: position, target, up)
# ├── canvas (background color, etc.)
# ├── transform (coordinate transformations)
# └── volume (volumetric data like electron density)
#     └── volume_representation (isosurface)
"""

from copy import deepcopy
import molviewspec as mvs
from molviewspec import MVSJ, MVSData
from molecularnodes import Molecule, Canvas
from typing import List


class MVSJ_Blender(MVSJ):
    """
    This class converts MVSJ to unique, renderable components and also handles global rendering.

    # Handle Globals
    # ├── camera (viewpoint: position, target, up)
    # ├── canvas (background color, etc.)
    # ├── transform (coordinate transformations)

    """
    model_config = {"extra": "allow"}

    def __init__(self, data):
        super().__init__(data=data)
        self.render_trees: List[MVSJ_Blender_Single_Tree] = []
        self._deduplicate_tree()

    def _deduplicate_tree(self):
        # make a list of valid MVS datastructures
        # where each entry is a complete, unique description.
        data = self.data.model_dump()  # Convert Pydantic model to dict

        def paths(node, path=[]):
            path += [{k: v for k, v in node.items() if k != 'children'}]
            return [path] if not node.get('children') else [p for c in node['children'] for p in paths(c, path[:])]

        def tree(path):
            t = None
            for n in reversed(path):
                if t: n['children'] = [t]
                t = n
            return t

        root = data.get('root', data)
        base = {k: v for k, v in data.items() if k != 'root'}
        deduplicated_trees = [{'root': tree(deepcopy(p)), **base} if 'root' in data else tree(deepcopy(p)) for p in paths(root)]

        updated_trees = []

        for idx, data in enumerate(deduplicated_trees):
            print(idx, data)
            try:
                updated = MVSJ_Blender_Single_Tree(data)
                updated_trees.append(updated)
            except:
                raise ValueError(f"Issue with tree in idx {idx} and data {data}")


        self.render_trees = updated_trees

    def render(self):
        # render each tree
        print("In the Render")
        canvas = Canvas()

        for tree in self.render_trees:
            tree.plot_tree()
        canvas.snapshot("output.png")
        print("After snapshot")
        pass


class MVSJ_Blender_Single_Tree(MVSJ):
    """
    This class holds a tree representing one complete, single representation.


    # Data Load:
    #   - determine format:
    #       - Molecule
    #       - Trajectory
    #       - Volume


    # Select components
    # structure
    # └── component (select atoms/residues/chains)
    #

    # Apply styles
    #     ├── representation (cartoon, ball_and_stick, surface, etc.)
    #     │   ├── color (styling)
    #     │   ├── label (annotations)     # todo
    #     │   ├── tooltip (hover info)    # todo
    #     │   └── opacity (transparency)
    #     └── focus (camera targeting)     # todo
    #
    # Primitive Handling # todo.

    """
    model_config = {"extra": "allow"}

    def __init__(self, data):
        # Clean the data before passing to parent constructor
        cleaned_data = self._clean_data(data)
        # Pass data as the data parameter to parent constructor
        super().__init__(data=cleaned_data)
        self.render_trees: List = []

    def _clean_data(self, data):
        """Clean data structure to ensure compatibility with MVSJ"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                if key == 'params' and value is None:
                    # Skip None params or convert to empty dict
                    cleaned[key] = {}
                elif isinstance(value, dict):
                    cleaned[key] = self._clean_data(value)
                elif isinstance(value, list):
                    cleaned[key] = [self._clean_data(item) for item in value]
                else:
                    cleaned[key] = value
            return cleaned
        elif isinstance(data, list):
            return [self._clean_data(item) for item in data]
        else:
            return data

    def ensure_single(self):
        """check to see there is only one representation to wrok on """
        pass

    def create_blender_name(self):
        pass


    def _load(self):
        pass
    def _select(self):
        pass
    def _style(self):
        pass
    def _material(self):
        pass

    def plot_tree(self):
        # take our complete, unique descriptions and generate
        # an MN Node.
        #
        # Type:
        #   - Molecule
        #   - Trajectory
        #   - Volume
        #   - Other:
        #
        # create the molecule using
        # root -> download -> parse -> structure
        root = getattr(self.data, 'root', self.data)
        print(root)
        # download = root.children[0]
        # parse = download.children[0]

        # print(download.params['url'])
        canvas = Canvas()
        # mol = Molecule.load(download.params['url'])
        # print(mol)
        canvas.snapshot("output.png")
        print("After snapshot")

        # volume = parse.children[0]
        # volume_representation = volume.children[0]
        # color = volume_representation.children[0]
        # opacity = representation.children[0]
        # print(f"Download: {download.params}")
        # print(f"parse: {parse.params}")
        # print(f"structure: {structure.params}")
        # create Selections
        # structure = parse.children[0]
        # transform = structure.children[0] # optional
        # component = structure.children[0] # optional
        # component_from_uri = structure.children[0] # optional
        # representation = component.children[0]
        # color = representation.children[0]
        # color_from_URI = representation.children[0]
        # opacity = representation.children[0]
        # label = component.children[0]
        print("plot_tree called")
        pass
