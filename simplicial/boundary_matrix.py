import warnings

import numpy as np

from itertools import combinations
from scipy.sparse import csc_matrix, find

class BoundaryMatrix:
    '''
    Representation of a simplicial complex via its boundary matrices.

    The p-th boundary matrix of a simplicial complex has a_i,j = 1 if
    the i-th (p-1)-simplex is a face of the j-th p-simplex; otherwise
    a_i,j = 0.

    This representation of the simplicial complex gives a simple
    approach to computing the ranks of the homology groups of a given
    complex (i.e. its Betti numbers) by examining the Smith normal forms
    of the boundary matrices.
    '''

    def __init__(self):
        self.boundary_matrices = dict()
        self.betti_numbers = []
    
    def add_boundary_matrix(self, dim, mat):
        '''
        Add a boundary matrix to the simplicial complex.

        Parameters:
        -----------
        dim : int
            Dimension of simplices described by matrix.
        mat : array-like
            2D array describing boundary relations between simplices and
            their faces.
        '''
        
        # Need lower dimensional simplices to be defined before
        # higher-dimensional simplies can be defined
        if dim > 0 and (dim - 1) not in self.boundary_matrices:
            raise ValueError(
                'Boundary matrix has no lower-dimensional precedent.'
            )
        
        # Rows of p-th boundary matrix must match columns of (p-1)-th
        # boundary matrix
        if dim > 0 and self.boundary_matrices[dim-1].shape[1] != mat.shape[0]:
            raise ValueError('Boundary matrix dimension mismatch.')
        
        self.boundary_matrices[dim] = np.array(mat)
    
    def get_boundary_matrix(self, dim):
        return self.boundary_matrices[dim]
    
    def _smith_normal_form(self, mat, x=0):
        '''
        Reduce matrix over Z2 to Smith normal form.

        Source: Edelsburnner & Harer - "Computational Topology: An
        Introduction"

        Parameters:
        -----------
        mat : ndarray
            Matrix to reduce.
        x : int, optional (default=0)
            Parameter tracking number of recursive iterations.
        
        Returns:
        --------
        mat : ndarray
            Reduced matrix.
        '''
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

            mat = self._smith_normal_form(mat, x+1)
        
        return mat
    
    # Compute Betti numbers by computing the SNF of each matrix
    def compute_betti_numbers(self):
        ranks_zp = np.array([])
        ranks_bp_1 = np.array([])

        for p in self.boundary_matrices:
            # Get the p-th boundary matrix
            mat = self.boundary_matrices[p]
            snf = self._smith_normal_form(mat)
            
            '''
            The rank of Z_p is equivalent to the number of zero columns
            in the Smith normal form of the p-th boundary matrix. The
            rank of B_(p-1) is the number of non-zero rows in Smith
            normal form of the p-th boundary_matrix.
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
    Reduced Betti numbers caputure the notion of a 0-dimensional "hole"
    (i.e. gives 1 when there is a gap between two disconnected vertices)
    '''
    def get_reduced_betti_numbers(self, recompute=False):
        if recompute or not self.betti_numbers:
            reduced = self.compute_betti_numbers()
        else:
            reduced = self.betti_numbers

        reduced[0] = reduced[0] - 1

        return reduced
    
    '''
    The Euler characteristic of a topological space can be given by the
    alternating sum of its Betti numbers
    '''
    def euler_characteristic(self):
        betti = self.get_betti_numbers()

        pos = betti[::2]
        neg = betti[1::2]

        return sum(pos) - sum(neg)



class SparseBoundaryMatrix:
    '''
    Sparse matrix representation of a simplicial complex via its
    boundary matrices.

    The p-th boundary matrix of a simplicial complex has a_i,j = 1 if
    the i-th (p-1)-simplex is a face of the j-th p-simplex; otherwise
    a_i,j = 0.

    This representation of the simplicial complex gives a simple
    approach to computing the ranks of the homology groups of a given
    complex (i.e. its Betti numbers) by examining the Smith normal forms
    of the boundary matrices.

    Attributes:
    -----------
    boundary_matrices : dict
        Dictionary containing boundary matrices of the simplicial
        complex.

        boundary_matrices[p] returns the boundary matrix for
        p-dimensional simplices.
    
    betti_numbers : list
        Betti numbers of the complex, if computed.
    
    dimension : int
        The maximum dimension of simplices in the complex.
    '''

    def __init__(self):
        self.boundary_matrices = dict()
        self.betti_numbers = []
        self._index_maps = dict()

    def _find_many(self, test_elements, elements):
        '''
        Get indices of all occurrences of values in a query array.

        Parameters:
        -----------
        test_elements : array
            Array to search for values.
        elements : array
            Query array containing values to search for.
        
        Returns:
        --------
        res : array
            Array of indices at which values of elements were found in
            test_elements.
        '''
        test_elements = np.squeeze(test_elements)
        if len(test_elements.shape) < 2:
            return np.nonzero(elements[:, None] == test_elements)[1]
        return np.where((elements[:, None] == test_elements).all(-1))[-1]
    
    def _set_index_map(self, p, simplices):
        '''
        Helper function for setting index map arrays.
        '''
        index_map = np.unique(simplices, axis=0)
        self._index_maps[p] = index_map
        return index_map

    def _get_indices(self, p, simplices):
        '''
        Helper function for getting indices of simplices in boundary
        matrix.
        '''
        if p < 0:
            return np.zeros(simplices.shape[0]).astype(int)
        return self._find_many(self._index_maps[p], simplices)
    
    def _expand_indices(self, p, indices):
        '''
        Helper function for repeating index values for simplices of
        dimension p.
        '''
        return np.array([[i] * (p+1) for i in indices]).flatten()
    
    def _get_simplices(self, p, indices):
        '''
        Helper function for obtaining simlices given in terms of user-
        defined vertex labels given their indices in a boundary matrix.
        '''
        return self._index_maps[p][indices.flatten()].reshape(indices.shape)
    
    def _get_cofaces(self, simplices):
        '''
        Helper function for getting all cofaces of simplices.
        '''
        if len(simplices.shape) < 2:
            return np.zeros_like(simplices)
        q = simplices.shape[1] - 1
        cofaces = []
        for s in simplices:
            cofaces.extend(combinations(s, q))
        cofaces = np.array(cofaces).squeeze()

        return cofaces

    def add_simplices(self, simplices):
        '''
        Adds simplices to complex. If simplices of similar dimension are
        already present, these will be overwritten.

        Parameters:
        -----------        
        simplices : ndarray-like
            List of simplices to add.
        '''
        
        # Convert to numpy type if necessary
        if isinstance(simplices, list):
            simplices = np.array(simplices)
        
        # Get dimension of simplices
        p = 0 if len(simplices.shape) < 2 else simplices.shape[1] - 1

        # Need lower dimensional simplices to be defined before
        # higher-dimensional simplies can be defined
        if p > 0 and (p - 1) not in self.boundary_matrices:
            raise ValueError(
                'Boundary matrix has no lower-dimensional precedent.'
            )
        
        self._set_index_map(p, simplices)
        p_indices = np.unique(self._get_indices(p, simplices))
        p_indices = self._expand_indices(p, p_indices)

        q_simplices = self._get_cofaces(simplices)
        q_indices = self._get_indices(p-1, q_simplices)

        if q_indices.shape[0] != p_indices.shape[0]:
            raise ValueError(
                'Boundary matrix dimension mismatch. Check triangulation.'
            )

        # Use CSC sparse matrix format for fast column lookup
        matrix = csc_matrix((np.ones_like(p_indices), (q_indices, p_indices)))
        self.boundary_matrices[p] = matrix

    def get_boundary_matrix(self, p):
        '''
        Returns p-th boundary matrix.
        '''
        return self.boundary_matrices[p]
    
    @staticmethod
    def _sparse_mod2(mat):
        '''
        Helper function for performing sparse matrix mod 2 operation.
        '''
        mat.data %= 2
        return mat

    def _sparse_snf(self, mat, x=0):
        '''
        Reduce sparse matrix over Z2 to Smith normal form.

        Parameters:
        -----------
        mat : CSC sparse matrix
            Matrix to reduce.
        x : int, optional (default=0)
            Parameter tracking number of recursive iterations.
        
        Returns:
        --------
        mat : CSC sparse matrix
            Reduced matrix.
        '''
        
        # Prevent in-place operations on initially passed matrix
        if x < 1:
            mat = mat.copy()

        rows, cols = mat.shape[0], mat.shape[1]
        
        ones = mat[x:,x:].nonzero()
        ones_rows, ones_cols = ones[0], ones[1]

        if ones_rows.size:
            k,l = ones_rows[0]+x, ones_cols[0]+x

            # Swap rows x and k
            mat[[x,k]] = mat[[k,x]]
            # Swap columns x and l
            mat[:, [x,l]] = mat[:, [l,x]]

            for n in range(x+1, rows):
                if mat[n,x] == 1:
                    # Add row x to row n
                    mat[n,:] = self._sparse_mod2((mat[x,:] + mat[n,:]))
                    
            for n in range(x+1, cols):
                if mat[x,n] == 1:
                    # Add col x to col n
                    mat[:,n] = self._sparse_mod2((mat[:,x] + mat[:,n]))

            mat = self._sparse_snf(mat, x+1)

        return mat
    
    def compute_betti_numbers(self):
        '''
        Computes the Betti numbers of the simplicial complex.
        
        Returns:
        --------
        betti_numbers : list[int]
            The Betti numbers of the complex.
        '''
        ranks_zp = np.array([])
        ranks_bp_1 = np.array([])

        for p in self.boundary_matrices:
            # Get the p-th boundary matrix
            mat = self.boundary_matrices[p]

            with warnings.catch_warnings():
                # SciPy will warn us that csc access is slow, but the
                # speedup in arithmetic outweighs this so we don't care
                warnings.filterwarnings('ignore')
                snf = self._sparse_snf(mat)
            
            '''
            The rank of Z_p is equivalent to the number of zero columns
            in the Smith normal form of the p-th boundary matrix. The
            rank of B_(p-1) is the number of non-zerorows in Smith
            normal form of the p-th boundary_matrix.
            '''
            last_one_row = 0
            first_zero_col = snf.shape[1]

            one_rows = find(snf.sum(axis=1).astype(bool))[0]
            zero_cols = find(~snf.sum(axis=0).astype(bool))[1]

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
        reduced_numbers = ranks_zp - ranks_bp
        # Remove padding
        betti_numbers = reduced_numbers[:-1]
        # Convert reduced Betti number to actual
        betti_numbers[0] = reduced_numbers[0] + 1

        # Convert to list of integers
        betti_numbers = list(betti_numbers.astype(int))

        self.betti_numbers = betti_numbers

        return betti_numbers
    
    def get_betti_numbers(self, recompute=False):
        if recompute or not self.betti_numbers:
            return self.compute_betti_numbers()
        return self.betti_numbers
    
    '''
    Reduced Betti numbers caputure the notion of a 0-dimensional "hole"
    (i.e. gives 1 when there is a gap between two disconnected vertices)
    '''
    def get_reduced_betti_numbers(self, recompute=False):
        if recompute or not self.betti_numbers:
            reduced = self.compute_betti_numbers()
        else:
            reduced = self.betti_numbers

        reduced[0] = reduced[0] - 1

        return reduced
    
    '''
    The Euler characteristic of a topological space can be given by the
    alternating sum of its Betti numbers
    '''
    def euler_characteristic(self):
        betti = self.get_betti_numbers()

        pos = betti[::2]
        neg = betti[1::2]

        return sum(pos) - sum(neg)