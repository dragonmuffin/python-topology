from abc import ABC, abstractmethod


class Manifold(ABC):
    """
    Abstract class for manifolds
    """
    @abstractmethod
    def euler_characteristic(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def is_homeomorphic_to(self, other : "Manifold") -> bool:
        raise NotImplementedError()

class SphereWithHandles(Manifold):
    """
    Class for SphereWithHandles manifold. Not implemented for non-orientable hieroglyphs
    """
    def __init__(self, genus : int, holes : int, nonorientable_genus : int = 0) -> None:
        self._g = genus
        self._h = holes
        self._nonorientable_genus = nonorientable_genus

    def is_homeomorphic_to(self, other : Manifold) -> bool:
        """Homeomorphism of manifolds"""
        if isinstance(other, SphereWithHandles):
            if self._nonorientable_genus != 0:
                if other._nonorientable_genus == 0:
                    return False
                return (self._nonorientable_genus + self._g == other.get_genus() + other._nonorientable_genus
                        and self._h == other.get_holes())
            return self._g == other.get_genus() and self._h == other.get_holes()
        elif isinstance(other, Hieroglyph):
            if self._nonorientable_genus != 0:
                raise NotImplementedError()
            return self._g == other.get_cross_ribbons() and self._h == other.get_boundary_circles()
        raise TypeError(f"Cannot check homeomorphism between SphereWithHandles and {type(other).__name__}")

    def euler_characteristic(self) -> int:
        """Get euler characteristic of this manifold"""
        return 2 - 2 * self._g - self._h

    def get_genus(self) -> int:
        """Get the genus of this manifold"""
        return self._g

    def get_holes(self) -> int:
        """Get count of holes of this manifold"""
        return self._h

    def get_nonorientable_genus(self) -> int:
        """Get non-orientable genus of this manifold"""
        return self._nonorientable_genus


class Hieroglyph(Manifold):
    """
    Class for hieroglyphs
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
        for i in word:
            if i not in letter_counter:
                q.append(i)
                letter_counter[i] = 1
                letter_indices[i] = ind
                ind += 1
            elif letter_counter[i] == 1:
                letter_counter[i] += 1
                q.remove(i)
                if q:
                    ind1 = letter_indices[i]
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

    def is_homeomorphic_to(self, other : Manifold) -> bool:
        """
        Homeomorphism of manifolds. Not implemented for non-orientable hieroglyphs

        other : Manifold for homeomorphism
        """
        if isinstance(other, SphereWithHandles):
            if other.get_nonorientable_genus() != 0:
                raise NotImplementedError()
            return self._cross_ribbons == other.get_genus() and self.get_boundary_circles() == other.get_holes()
        elif isinstance(other, Hieroglyph):
            return self._cross_ribbons == other.get_cross_ribbons() and self.get_boundary_circles() == other.get_boundary_circles()
        raise TypeError(f"Cannot check homeomorphism between Hieroglyph and {type(other).__name__}")

    def get_boundary_circles(self) -> int:
        """Get boundary circles, count of components of edge"""
        return self._ribbons - 2 * self._cross_ribbons + 1

    def euler_characteristic(self) -> int:
        """Get euler characteristic of this manifold"""
        return 2 - 2 * self._cross_ribbons - self.get_boundary_circles()

    def get_ribbons(self) -> int:
        """Get count of ribbons of this manifold"""
        return self._ribbons

    def get_cross_ribbons(self) -> int:
        """Get count of pairs of ribbons which crosses each other"""
        return self._cross_ribbons