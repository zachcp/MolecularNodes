from copy import deepcopy
import molviewspec as mvs
from molviewspec import MVSJ
from molecularnodes import Molecule
from typing import List


class MVSJ_Blender(MVSJ):
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
    """
    self.data: MVSJ
    self.render_trees: List[]

    def ensure_single(self):
        """check to see there is only one representation to wrok on """
        pass

    def create_blender_name(self):
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
