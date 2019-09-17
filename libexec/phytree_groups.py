#! /usr/bin/env python3

import argparse
from biolib.CircleNode import CircleNodeTree


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
    f_out = open(f_cluster_res, 'w')
    circle_node_tree.split_inner_tree()
    for node in circle_node_tree.traverse():
        print('>' + node.name, file=f_out)
        print('@' + node.base_inner_node.write(), file=f_out)
        inner_node = node.get_inner_node()
        for inner_node_ele in inner_node:
            if inner_node_ele.name != '':
                print(inner_node_ele.name, file=f_out)
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
