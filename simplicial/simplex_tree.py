from simplicial.boundary_matrix import SparseBoundaryMatrix

class SimplexNode:
    '''
    A helper class for representing nodes within a SimplexTree.
    '''
    
    def __init__(self, label=None, parent=None, children=None):
        self.label = label
        self.parent = parent
        self.children = children if children is not None else dict()

        self.depth = self._initialize_depth()
        self.dimension = self.depth - 1
        self.linked_node = self._initialize_linked_node()

        pass

    def _initialize_depth(self):
        '''
        Computes the depth of self within the Simplex Tree.
        '''
        return 0 if self.parent is None else (self.parent.depth+1)
    
    def _initialize_linked_node(self):
        '''
        Obtains a pointer to the next node in a circular linked list of
        all nodes at the same depth as self with a shared label.
        '''
        root = self
        while root.parent is not None:
            root = root.parent
        
        to_visit = [root]
        while to_visit:
            node = to_visit.pop(0)
            to_visit.extend(node.children.values())
            if node.depth != self.depth or node is self:
                continue
            if node.label == self.label:
                # Using any viable node as an entry point, get the linked list
                all_linked_nodes = node.get_linked_nodes()
                last_linked_node = all_linked_nodes[-1]

                # Point the last linked node to self
                last_linked_node.linked_node = self
                
                # Point self to the first linked node (close the list)
                return node
        
        return self
    
    def get_vertex_list(self):
        if self.parent is None:
            return []
        vertex_list = self.parent.get_vertex_list()
        vertex_list.append(self.label)
        return vertex_list
    
    def _get_verbose_label(self):
        '''
        Generates a label which enumerates the vertices of the simplex
        corresponding to self.
        '''
        label_list = [str(v) for v in self.get_vertex_list()]
        return ','.join(label_list)
    
    def get_linked_nodes(self):
        '''
        Obtains the circular linked list of all nodes at the same depth
        as self with a shared label.
        '''
        linked_nodes = [self]
        node = self.linked_node
        while node is not self:
            linked_nodes.append(node)
            node = node.linked_node
        return linked_nodes

    def _to_dict(self):
        if not self.children:
            return {}
        return {k:v._to_dict() for k,v in self.children.items()}

    def __repr__(self) -> str:
        return f'SimplexNode({self._get_verbose_label()})'

class SimplexTree:
    '''
    A shoddy implementation of the simplex tree data structure.

    Simplex trees are an operation-efficient data structure for
    representing general (filtered) simplicial complexes. They were
    originally introduced by Boissonnat and Maria in the paper:
    https://arxiv.org/pdf/2001.02581

    '''
    
    def __init__(self):
        
        self.root = SimplexNode()
        self.dimension = -1

        pass
    
    def search_simplex(self, *simplex, from_node=None):
        '''
        Find a simplex in the simplex tree and return its node. If not
        found, returns None.

        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        
        Returns:
        --------
        node : SimplexNode
            If found, the SimplexNode object representing the simplex.
        '''
        if from_node is None:
            node = self.root
        else:
            node = from_node

        for vertex in simplex:
            if vertex not in node.children:
                return None
            else:
                node = node.children[vertex]
        
        return node

    def insert_simplex(self, *simplex):
        '''
        Insert a simplex into the SimplexTree.

        Requires that the simplex's faces are already present in the
        SimplexTree, per the defninition of a simplicial complex.

        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        '''

        simplex_partial = simplex[:-1]
        node = self.search_simplex(*simplex_partial)

        if node is None:
            raise ValueError(f'Simplex {simplex_partial} is not in complex.')
        
        last = simplex[-1]
        if last in node.children:
            # Simplex already exists
            return
        
        new_node = SimplexNode(
            label=last,
            parent=node,
        )
        node.children[last] = new_node

        if len(simplex) >  self.dimension + 1:
            self.dimension = len(simplex) - 1
        
        return
    
    def insert_simplices(self, simplices):
        for simplex in simplices:
            self.insert_simplex(*simplex)
    
    def _insert_full_simplex(self, *simplex, node=None):
        '''
        Helper function for simplex insertion. Inserts the simplex into
        the SimplexTree at the given node, creating new nodes and
        recursing as needed.
        
        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        node : SimplexNode
            The SimplexNode object at which to insert the given simplex.
        '''
        if node is None:
            node = self.root
        
        for i, vertex in enumerate(simplex):
            if vertex not in node.children:
                new_node = SimplexNode(
                    label=vertex,
                    parent=node
                )
                node.children[vertex] = new_node
                self._insert_full_simplex(*simplex[i+1:], node=new_node)
            else:
                self._insert_full_simplex(
                    *simplex[i+1:],
                    node=node.children[vertex]
                )
        
        if len(simplex) >  self.dimension + 1:
            self.dimension = len(simplex) - 1
        
        return
    
    def insert_full_simplex(self, *simplex):
        '''
        Insert a simplex into the SimplexTree. Inserts any faces of the
        simplex that are not already present.

        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        '''
        self._insert_full_simplex(*simplex)
        return
    
    def insert_full_simplices(self, simplices):
        for simplex in simplices:
            self.insert_full_simplex(*simplex)

    def remove_simplex(self, *simplex):
        '''
        Remove a simplex from the SimplexTree. Removes any cofaces of
        the simplex that are also present.

        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        '''
        cofaces = self.locate_cofaces(*simplex)
        for coface in cofaces:
            removed_node = coface.parent.children.pop(coface.label, None)
            del removed_node

        simplex_node = self.search_simplex(*simplex)
        removed_node = simplex_node.parent.children.pop(simplex_node.label, None)
        del removed_node
        
        pass

    def _locate_external_cofaces(self, *simplex):
        '''
        Locates cofaces of the given simplex that are not contained in
        the subtree of that simplex's corresponding node.
        
        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        
        Returns:
        --------
        cofaces : list[SimplexNode]
            List of external cofaces of the given simplex.
        '''
        last = simplex[-1]
        min_depth = len(simplex) + 1

        # Find nodes of depth at least len(simplex) which contain last(simplex)
        all_linked_nodes = []
        to_visit = [self.root]
        visited_depths = []
        while to_visit:
            node = to_visit.pop(0)
            if node.depth < min_depth:
                to_visit.extend(node.children.values())
                continue
            if node.depth in visited_depths:
                continue
            if node.label == last:
                all_linked_nodes.extend(node.get_linked_nodes())
                visited_depths.append(node.depth)
            to_visit.extend(node.children.values())

        # Perform upward traversals from each such node and check if coface
        coface_roots = []
        for linked_node in all_linked_nodes:
            
            vertex_list = list(reversed(simplex))
            node = linked_node
            while node.parent is not None:
                if not vertex_list:
                    coface_roots.append(linked_node)
                    break
                if node.label == vertex_list[0]:
                    vertex_list.pop(0)
                node = node.parent

        # Traverse subtree at each coface root to enumerate all cofaces
        cofaces = []
        for root in coface_roots:
            to_visit = [root]
            while to_visit:
                node = to_visit.pop(0)
                cofaces.append(node)
                to_visit.extend(node.children.values())
        
        return cofaces
    
    def locate_cofaces(self, *simplex):
        '''
        Locates all cofaces of the given simplex.
        
        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        
        Returns:
        --------
        cofaces : list[SimplexNode]
            List of cofaces of the given simplex.
        '''

        simplex_node = self.search_simplex(*simplex)
        if simplex_node is None:
            raise ValueError(f'Simplex {simplex} is not in complex.')

        cofaces = []
        to_visit = list(simplex_node.children.values())
        while to_visit:
            node = to_visit.pop(0)
            cofaces.append(node)
            to_visit.extend(node.children.values())
        
        cofaces.extend(self._locate_external_cofaces(*simplex))

        return cofaces

    def locate_facets(self, *simplex):
        '''
        Locates all facets of the given simplex.
        
        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        
        Returns:
        --------
        facets : list[SimplexNode]
            List of facets of the given simplex.
        '''
        simplex_node = self.search_simplex(*simplex)
        if simplex_node is None:
            raise ValueError(f'Simplex {simplex} is not in complex.')

        facets = [simplex_node.parent]
        node = simplex_node.parent.parent
        for i in reversed(range(len(simplex))):
            if node is None:
                continue
            target_simplex = simplex[i:]
            result = self.search_simplex(*target_simplex, from_node=node)
            if result is not None:
                facets.append(result)
            node = node.parent
            
        return facets

    def elementary_collapse(self, *simplex):
        '''
        Perform an elementary collapse of the given simplex.

        Parameters:
        -----------
        simplex :  list[Any]
            Simplex given as an enumeration of its vertices.
        '''
        
        facets = self.locate_facets(*simplex)
        
        for facet in facets:
            facet = facet.get_vertex_list()
            cofaces = self.locate_cofaces(*facet)
            if len(cofaces) != 1:
                continue
            if tuple(cofaces[0].get_vertex_list()) == simplex:
                self.remove_simplex(*facet)
                return
        
        raise ValueError(f'Simplex {simplex} is not collapsible.')

    def boundary_matrix(self):
        
        boundary_matrix = SparseBoundaryMatrix()

        level = list(self.root.children.values())
        while any(level):
            level_simplices = [node.get_vertex_list() for node in level]
            if len(level_simplices[0]) == 1:
                level_simplices = [s[0] for s in level_simplices]
            boundary_matrix.add_simplices(level_simplices)
            level = [child for node in level for child in node.children.values()]

        return boundary_matrix

    def betti_numbers(self):
        boundary_matrix = self.boundary_matrix()
        return boundary_matrix.compute_betti_numbers()

    def to_dict(self):
        return self.root._to_dict()

    def __repr__(self):
        res = 'SimplexTree('
        vertices = [str(vert) for vert in self.root.children.keys()]
        if len(vertices) > 5:
            res += ','.join(vertices[:2])
            res += ',...,'
            res += ','.join(vertices[-2:])
        else:
            res += ','.join(vertices)
        res += ')'
        return res

if __name__ == '__main__':

    s = SimplexTree()
    s.insert_full_simplex(0,1,2)
    s.remove_simplex(0,1,2,)
    print(s.betti_numbers())

    s = SimplexTree()
    s.insert_full_simplex(0,1,4)
    s.insert_full_simplex(0,2,3)
    s.insert_full_simplex(0,2,5)
    s.insert_full_simplex(0,3,4)
    s.insert_full_simplex(1,2,5)
    s.insert_full_simplex(1,4,5)

    print(s.betti_numbers())