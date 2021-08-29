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
        self.betti_numbers = []
    
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
    def compute_betti_numbers(self):
        ranks_zp = np.array([])
        ranks_bp_1 = np.array([])

        for p in self.boundary_matrices:
            # Get the p-th boundary matrix
            mat = self.boundary_matrices[p]
            snf = smith_normal_form(mat)
            
            '''
            The rank of Z_p is equivalent to the number of zero columns in the Smith normal
            form of the p-th boundary matrix. The rank of B_(p-1) is the number of non-zero
            rows in Smith normal form of the p-th boundary_matrix.
            '''
            last_one_row = 0
            first_zero_col = snf.shape[1]

            one_rows = np.where(np.any(snf, axis=1))[0]
            zero_cols = np.where(~np.any(snf, axis=0))[0]

            if one_rows.size:
                last_one_row = one_rows[-1]
            if zero_cols.size:
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
        # Remove padding
        betti = betti[:-1]
        # Convert reduced Betti number to actual
        betti[0] = betti[0] + 1

        # Convert to list of integers
        betti = list(betti.astype(int))

        self.betti_numbers = betti

        return betti
    
    def get_betti_numbers(self, recompute=False):
        if recompute or not self.betti_numbers:
            return self.compute_betti_numbers()
        return self.betti_numbers
    
    '''
    Reduced Betti numbers caputure the notion of a 0-dimensional "hole" (i.e. gives 1 when there is a gap
    between two disconnected vertices).
    '''
    def get_reduced_betti_numbers(self, recompute=False):
        if recompute or not self.betti_numbers:
            reduced = self.compute_betti_numbers()
        else:
            reduced = self.betti_numbers

        reduced[0] = reduced[0] - 1

        return reduced

    
    '''
    The Euler characteristic of a topological space can be given by the alternating sum of its Betti numbers
    '''
    def euler_characteristic(self):
        betti = self.get_betti_numbers()

        pos = betti[::2]
        neg = betti[1::2]

        return sum(pos) - sum(neg)

'''
Reduce matrix over Z2 to Smith normal form.

Source: Edelsburnner & Harer - "Computational Topology: An Introduction"
'''
def smith_normal_form(mat, x=0):
    # Prevent in-place operations on initially passed matrix
    if x < 1:
        mat = mat.copy()

    rows, cols = mat.shape[0], mat.shape[1]

    ones = np.where(mat[x:, x:] == 1)

    if ones[0].size:
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