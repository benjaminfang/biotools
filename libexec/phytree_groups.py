#! /usr/bin/env python3

import ete3
import argparse


class CircleNode:

    def __init__(self, BaseInnerNode, CircleNodeName='', dist=1):
        self.name = CircleNodeName
        self.dist = dist
        self.base_inner_node = BaseInnerNode
        self.parent_link_bridge = [BaseInnerNode, None] #BaseInnerNode --> ParentNond
        self.children_link_bridge = []                  # InnerNode --> ChildrenNode

    def get_base_inner_node(self):
        return self.base_inner_node

    def get_down_stretch_inner_node(self):
        down_stretch_inner_node = []
        for bridge in self.children_link_bridge:
            down_stretch_inner_node.append(bridge[0])
        down_stretch_inner_node = list(set(down_stretch_inner_node))
        return down_stretch_inner_node

    def is_base_inner_node(self, node):
        if node == self.base_inner_node:
            return True
        else:
            return False

    def is_down_stretch_inner_node(self, node):
        if node in self.get_down_stretch_inner_node:
            return True
        else:
            return False

    def get_children_node(self):
        dt_out = []
        for bridge in self.children_link_bridge:
            dt_out.append(bridge[1])
        return dt_out

    def get_parent_node(self):
        dt_out = self.parent_link_bridge[1]
        return dt_out

    def add_child(self, parent_inner_link_node, child_circle_node):
        self.children_link_bridge.append([parent_inner_link_node, child_circle_node])
        child_circle_node.parent_link_bridge = [child_circle_node.base_inner_node, self]

    def link_to_parent(self, parent_inner_link_node, parent_circle_node):
        self.parent_link_bridge = [self.base_inner_node, parent_circle_node]
        parent_circle_node.children_link_bridge.append([parent_inner_link_node, self])

    def if_linked_directly(self, second_circle_node):
        all_out_stretch = self.children_link_bridge.append(self.parent_link_bridge)
        all_linked_circle_node = [bridge[1] for bridge in all_out_stretch]
        if second_circle_node in all_linked_circle_node:
            return True
        else:
            return False

    def get_link_bridge(self, second_circle_node):
        all_out_stretch = self.children_link_bridge.append(self.parent_link_bridge)
        link_bridge = None
        for bridge in all_out_stretch:
            if bridge[1] == second_circle_node:
                link_bridge = bridge
        return link_bridge

    def get_linker(self, second_circle_node):
        link_bridge = self.get_link_bridge(second_circle_node)
        dt_out = None
        if link_bridge:
            dt_out = [link_bridge[0]]
            for bridge in second_circle_node.children_link_bridge.append(\
                second_circle_node.parent_link_bridge):
                if self == bridge[1]:
                    dt_out.append(bridge[0])
        return dt_out

    def get_inner_node(self):

        def get_inner_node_recursive(parent, stop_node):
            dt_out = []
            dt_out.append(parent)
            for child in parent.children:
                if child not in stop_node:
                    dt_out += get_inner_node_recursive(child, stop_node)
            return dt_out

        base_inner_node = self.base_inner_node
        children = self.get_children_node()
        children_base_inner_node = [child.base_inner_node for child in children]
        inner_node = get_inner_node_recursive(base_inner_node, children_base_inner_node)
        return inner_node

    def is_leaf(self):
        if self.children_link_bridge:
            return True
        else:
            return False

    def is_root(self):
        if self.parent_link_bridge:
            return True
        else:
            return False

    def get_dist(self, node):
        return self.base_inner_node.get_distance(node.base_inner_node)

    def get_root_circle_node(self):
        root = self
        parent_link = root.parent_link_bridge
        while parent_link[1]:
            root = parent_link[1]
            parent_link = root.parent_link_bridge
        return root

    def make_profile_tree(self):

        def traverse_tree(circle_node, parent_node):
            for child in circle_node.get_children_node():
                child_node = ete3.TreeNode()
                child_node.name = child.name
                child_node.dist = child.get_dist(circle_node)
                parent_node.add_child(child_node)
                traverse_tree(child, child_node)
            return 0

        root_circle_node = self.get_root_circle_node()
        root = ete3.TreeNode()
        root.dist = 0
        root.name = root_circle_node.name
        traverse_tree(root_circle_node, root)
        return root


class CircleNodeTree:

    def __init__(self, treefile, edge_len_cutoff):

        def find_down_linker(parent_node, edge_len_cutoff):
            dt_out = []
            for child in parent_node.children:
                if child.dist > edge_len_cutoff:
                    dt_out.append([parent_node, child])
                else:
                    sub_dt = find_down_linker(child, edge_len_cutoff)
                    dt_out += sub_dt
            return dt_out

        def link_circle_node(parent_circle_node, edge_len_cutoff):
            nonlocal i
            down_linker = find_down_linker(parent_circle_node.base_inner_node, edge_len_cutoff)
            for linker in down_linker:
                i += 1
                parent_inner_link_node = linker[0]
                child_base_inner_node = linker[1]
                child_circle_node_name = 'CircleNode_' + str(i)
                child_circle_node = CircleNode(child_base_inner_node, child_circle_node_name, \
                    child_base_inner_node.get_distance(parent_circle_node.base_inner_node))
                parent_circle_node.add_child(parent_inner_link_node, child_circle_node)
                link_circle_node(child_circle_node, edge_len_cutoff)

        self.original_tree = ete3.Tree(treefile)
        i = 0
        root_circle_node = CircleNode(self.original_tree, 'CircleNode_0', 0)
        link_circle_node(root_circle_node, edge_len_cutoff)
        self.circle_node_tree =  root_circle_node



def getargs(args_in):
    args = argparse.ArgumentParser(description="This is a utility to cluster a tree's \
        node according to length of edge.", prog='phytree_groups')
    args.add_argument('treefile', type=str, help='file name of newike tree.')
    args.add_argument('edge_len_cutoff', type=float, help='cutoff of edge length to \
        make a circlal cluster.')
    args.add_argument('-f_cluster_res', type=str, default='cluster.fasta', help='\
        file name to output cluster result, default is "cluster.fasta".')
    args.add_argument('-f_profile_tree', type=str, default='profile.nwk', help='\
        CircleNode Tree profile tree file. default is "profile.nwk".')
    if args_in:
        args =args.parse_args(args_in)
    else:
        args = args.parse_args()
    treefile, edge_len_cutoff, f_cluster_res, f_profile_tree = args.treefile, \
        args.edge_len_cutoff, args.f_cluster_res, args.f_profile_tree
    return treefile, edge_len_cutoff, f_cluster_res, f_profile_tree


def print_cluster_res(circle_node_tree, f_cluster_res):

    def traverse_tree(circle_node_tree, f_out):
        print('>' + circle_node_tree.name, file=f_out)
        inner_node = circle_node_tree.get_inner_node()
        for node in inner_node:
            if node.name != '':
                print(node.name, file=f_out)
        for child in circle_node_tree.get_children_node():
            traverse_tree(child, f_out)
        return 0

    f_out = open(f_cluster_res, 'w')
    traverse_tree(circle_node_tree, f_out)
    f_out.close()
    return 0


def main(name='phytree_groups', args=[]):
    myname = 'phytree_groups'
    if name == myname:
        treefile, edge_len_cutoff, f_cluster_res, f_profile_tree = getargs(args)
        circle_node_tree = CircleNodeTree(treefile, edge_len_cutoff)
        circle_node_tree = circle_node_tree.circle_node_tree
        profile_tree = circle_node_tree.make_profile_tree()
        print(profile_tree.write(), file=open(f_profile_tree, 'w'))
        print_cluster_res(circle_node_tree, f_cluster_res)
    return 0


if __name__ == '__main__':
    main()
