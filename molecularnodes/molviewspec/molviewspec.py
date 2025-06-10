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
from molviewspec import MVSJ
from molecularnodes import Molecule
from typing import List


class MVSJ_Blender(MVSJ):
    """
    This class converts MVSJ to unique, renderable components and also handles global rendering.

    # Handle Globals
    # ├── camera (viewpoint: position, target, up)
    # ├── canvas (background color, etc.)
    # ├── transform (coordinate transformations)

    """
    self.data: MVSJ
    self.render_trees: List[MVSJ_Blender_Single_Tree]

    def deduplicate_tree(self):
        # make a list of valid MVS datastructures
        # where each entry is a complete, unique description.
        data = self.data

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
        return [{'root': tree(deepcopy(p)), **base} if 'root' in data else tree(deepcopy(p)) for p in paths(root)]

    def render(self):
        # render each tree
        # set global options
        # return
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
    self.data: MVSJ
    self.render_trees: List[]

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
    def plot_tree(tree: mvs.MVSJ):
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
        root = tree.data.root
        download = root.children[0]
        parse = download.children[0]
        # volume = parse.children[0]
            # volume_representation = volume.children[0]
            # color = volume_representation.children[0]
            # opacity = representation.children[0]
        print(f"Download: {download.params}")
        print(f"parse: {parse.params}")
        print(f"structure: {structure.params}")
        # create Selections
        structure = parse.children[0]
        transform = structure.children[0] # optional
        component = structure.children[0] # optional
        component_from_uri = structure.children[0] # optional
            representation = component.children[0]
                color = representation.children[0]
                color_from_URI = representation.children[0]
                opacity = representation.children[0]
            label = component.children[0]
