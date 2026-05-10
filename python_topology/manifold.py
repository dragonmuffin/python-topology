from abc import ABC, abstractmethod
from python_topology import Graph, Thickening


class Manifold(ABC):
    """
    Abstract class for manifolds
    """
    @abstractmethod
    def euler_characteristic(self) -> int:
        """Euler characteristic of manifold"""
        raise NotImplementedError()

    @abstractmethod
    def get_orientable_genus(self) -> int:
        """Genus orientable manifold"""
        raise NotImplementedError()

    def is_realizable(self, graph: Graph | Thickening) -> bool:
        """Realizability of manifold"""
        target_g = self.get_orientable_genus()
        if isinstance(graph, Thickening):
            return graph.handles() <= target_g

        if not graph.connected():
            raise ValueError('Graph must be connected.')

        for k in range(graph.get_number_of_thickenings()):
            if Thickening(graph, k).handles() <= target_g:
                return True
        return False

    @abstractmethod
    def get_boundaries_count(self) -> int:
        """Amount of holes"""
        raise NotImplementedError()

    @abstractmethod
    def is_orientable(self) -> bool:
        """Orientable manifold"""
        raise NotImplementedError()

    def is_homeomorphic_to(self, other: "Manifold") -> bool:
        """Homeomorphism of manifolds"""
        return (self.is_orientable() == other.is_orientable() and
                self.euler_characteristic() == other.euler_characteristic() and
                self.get_boundaries_count() == other.get_boundaries_count())

class SphereWithHandles(Manifold):
    """
    Class for SphereWithHandles manifold. Not implemented for non-orientable hieroglyphs
    """
    def __init__(self, genus : int, holes : int, nonorientable_genus : int = 0) -> None:
        self._g = genus
        self._h = holes
        self._nonorientable_genus = nonorientable_genus

    def __str__(self) -> str:
        """
        String representation of SphereWithHandles manifold
        """
        return f'Manifold({self._g}, {self._h})'

    def __add__(self, other: Manifold) -> "SphereWithHandles":
        if isinstance(self, SphereWithHandles) and isinstance(other, SphereWithHandles):
            new_g = self.get_genus() + other.get_genus()
            new_h = self.get_holes() + other.get_holes()
            new_n = self.get_nonorientable_genus() + other.get_nonorientable_genus()

            if new_n > 0:
                new_n += 2 * new_g
                new_g = 0

            return SphereWithHandles(new_g, new_h, new_n)
        raise NotImplementedError("Add implemented only for SphereWithHandles")

    def euler_characteristic(self) -> int:
        """Get euler characteristic of this manifold"""
        return 2 - 2 * self._g - self._nonorientable_genus - self._h

    def get_genus(self) -> int:
        """Get the genus of this manifold"""
        return self._g

    def get_holes(self) -> int:
        """Get count of holes of this manifold"""
        return self._h

    def get_nonorientable_genus(self) -> int:
        """Get non-orientable genus of this manifold"""
        return self._nonorientable_genus

    def get_orientable_genus(self) -> int:
        """Get orientable genus of this manifold"""
        return self._g

    def glue_disk(self, disks : int = 1) -> None:
        """Glue the disks of this manifold"""
        if disks >= self._h:
            self._h = 0
        else:
            self._h -= disks

    def puncture(self, holes : int = 1) -> None:
        """Puncture this manifold with holes"""
        self._h += holes

    def get_boundaries_count(self) -> int:
        """Amount of holes"""
        return self._h

    def is_orientable(self) -> bool:
        """Orientable manifold"""
        return self._nonorientable_genus == 0

class Hieroglyph(Manifold):
    """
    Class for hieroglyphs
    Uppercase letters denote inverse ribbons (e.g., A = a^-1).
    """
    def __init__(self, word : str) -> None:
        self._word = word
        self._matrix = []
        for i in range(len(self._word) // 2):
            self._matrix.append([0] * (len(self._word) // 2))

        letter_counter = {}
        q = []
        ind = 0
        letter_indices = {}
        ribbons = 0
        twisted_ribbons = 0
        first_occ_case = {}
        for i in word:
            base = i.lower()
            if base not in letter_counter:
                q.append(base)
                letter_counter[base] = 1
                letter_indices[base] = ind
                first_occ_case[base] = i.islower()
                ind += 1
            elif letter_counter[base] == 1:
                letter_counter[base] += 1
                q.remove(base)

                if first_occ_case[base] == i.islower():
                    twisted_ribbons += 1

                if q:
                    ind1 = letter_indices[base]
                    for j in q:
                        ind2 = letter_indices[j]
                        self._matrix[ind1][ind2] = 1
                        self._matrix[ind2][ind1] = 1
                        ribbons += 1
            else:
                raise ValueError('Incorrect word. 1 letter cannot appear more than 2 times')

        if q:
            raise ValueError('Incorrect word. 1 letter is extra')

        self._cross_ribbons = ribbons
        self._ribbons = len(self._word) // 2
        self._twisted_ribbons = twisted_ribbons

    def __str__(self) -> str:
        """
        String representation of Hieroglyph manifold
        """
        return f'Hieroglyph({self._word})'

    def get_boundary_circles(self) -> int:
        """Get boundary circles, count of components of edge"""
        if self._twisted_ribbons == 0:
            return self._ribbons - 2 * self._cross_ribbons + 1

        l = len(self._word)
        parent = list(range(l))

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            r_i, r_j = find(i), find(j)
            if r_i != r_j:
                parent[r_i] = r_j

        positions = {}
        for i, char in enumerate(self._word):
            base = char.lower()
            if base not in positions: positions[base] = []
            positions[base].append((i, char.islower()))

        for occurrences in positions.values():
            i1, is_lower1 = occurrences[0]
            i2, is_lower2 = occurrences[1]
            if is_lower1 != is_lower2:
                union(i1, (i2 + 1) % l)
                union((i1 + 1) % l, i2)
            else:
                union(i1, i2)
                union((i1 + 1) % l, (i2 + 1) % l)

        return len(set(find(i) for i in range(l)))

    def euler_characteristic(self) -> int:
        """Get euler characteristic of this manifold"""
        return 1 - self._ribbons

    def get_ribbons(self) -> int:
        """Get count of ribbons of this manifold"""
        return self._ribbons

    def get_twisted_ribbons(self) -> int:
        """Get count of twisted ribbons"""
        return self._twisted_ribbons

    def get_cross_ribbons(self) -> int:
        """Get count of pairs of ribbons which crosses each other"""
        return self._cross_ribbons

    def get_orientable_genus(self) -> int:
        """Get orientable genus of this manifold"""
        return self._cross_ribbons

    def get_boundaries_count(self) -> int:
        """Amount of holes"""
        return self.get_boundary_circles()

    def is_orientable(self) -> bool:
        """Orientable manifold"""
        return self._twisted_ribbons == 0