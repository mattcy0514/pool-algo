import numpy as np

def mirror_table(node_rr:np.matrix, node_ij:np.matrix):
    x_reflect = np.matrix([[1, 0], [0, -1]])
    y_reflect = np.matrix([[-1, 0], [0, 1]])

    coordinate_rr = np.matrix((50, 25))

    node_diff = node_ij - node_rr

    cy = abs(node_diff[0, 0] % 2)
    cx = abs(node_diff[0, 1] % 2)

    if cy:
        node_diff[0, 0] = node_diff[0, 0] + 1
    if cx:
        node_diff[0, 1] = node_diff[0, 1] + 1

    comp_mat = x_reflect ** cx * y_reflect ** cy

    coordinate_ij = comp_mat * coordinate_rr.T + 100 * node_diff.T
    print(coordinate_ij)

def main():
    mirror_table(np.matrix((3, 3)), np.matrix((5, 3)))
    
if __name__ == '__main__':
    main()