import numpy as np

'''
Representation of a simplicial complex via its boundary matrices.

The p-th boundary matrix of a simplicial complex has a_i,j = 1 if
the i-th (p-1)-simplex is a face of the j-th p-simplex; otherwise a_i,j = 0.

This representation of the simplicial complex gives a simple approach to computing
the ranks of the homology groups of a given complex (i.e. its Betti numbers) by
examining the Smith normal forms of the boundary matrices.
'''
class SimplicialComplex:

    def __init__(self):
        self.boundary_matrices = dict()
    
    def add_boundary_matrix(self, dim, mat):
        # Need lower dimensional simplices to be defined before higher-dimensional simplies can be defined
        if dim > 0 and (dim - 1) not in self.boundary_matrices:
            raise ValueError('Boundary matrix has no lower-dimensional precedent.')
        # Rows of p-th boundary matrix must match columns of (p-1)-th boundary matrix
        if dim > 0 and self.boundary_matrices[dim-1].shape[1] != mat.shape[0]:
            raise ValueError('Boundary matrix dimension mismatch.')
        
        self.boundary_matrices[dim] = np.array(mat)
    
    def get_boundary_matrix(self, dim):
        return self.boundary_matrices[dim]
    
    # Compute Betti numbers by computing the SNF of each matrix
    def betti_numbers(self):
        ranks_zp = np.array([])
        ranks_bp_1 = np.array([])
        betti = []

        for p in self.boundary_matrices:
            # Get the p-th boundary matrix
            mat = self.boundary_matrices[p]
            snf = smith_normal_form(mat.copy(), 0)
            
            '''
            The rank of Z_p is equivalent to the number of zero columns in the Smith normal
            form of the p-th boundary matrix. The rank of B_(p-1) is the number of non-zero
            rows in Smith normal form of the p-th boundary_matrix.
            '''
            last_one_row = 0
            first_zero_col = snf.shape[1]

            one_rows = np.where(np.any(snf, axis=1))[0]
            zero_cols = np.where(~np.any(snf, axis=0))[0]

            if len(one_rows) > 0:
                last_one_row = one_rows[-1]
            if len(zero_cols) > 0:
                first_zero_col = zero_cols[0]
            
            rank_zp = snf.shape[1] - first_zero_col
            rank_bp_1 = last_one_row + 1

            ranks_zp = np.append(ranks_zp, rank_zp)
            ranks_bp_1 = np.append(ranks_bp_1, rank_bp_1)

        # Add padding for roll
        ranks_zp = np.append(ranks_zp, 0)
        ranks_bp_1 = np.append(ranks_bp_1, 0)

        # Shift lower-dimencional ranks into place
        ranks_bp = np.roll(ranks_bp_1, -1)

        # rankH_p = rankZ_p - rankB_p
        betti = ranks_zp - ranks_bp
        # Cut off padding
        betti = betti[:-1]
        # Convert reduced Betti number to actual
        betti[0] = betti[0] + 1

        return betti

'''
Reduce matrix over Z2 to Smith normal form.

Source: Edelsburnner & Harer - "Computational Topology: An Introduction"
'''
def smith_normal_form(mat, x):
    rows, cols = mat.shape[0], mat.shape[1]

    ones = np.where(mat[x:, x:] == 1)

    if len(ones[0]) > 0:
        k,l = ones[0][0]+x, ones[1][0]+x

        # Swap rows x and k
        mat[[x,k]] = mat[[k,x]]
        # Swap columns x and l
        mat[:, [x,l]] = mat[:, [l,x]]

        for n in range(x+1, rows):
            if mat[n,x] == 1:
                # Add row x to row n
                mat[n,:] = (mat[x,:] + mat[n,:]) % 2
        
        for n in range(x+1, cols):
            if mat[x,n] == 1:
                # Add col x to col n
                mat[:,n] = (mat[:,x] + mat[:,n]) % 2

        mat = smith_normal_form(mat, x+1)
    
    return mat