import unittest
from unittest.mock import MagicMock
from python_topology import Hieroglyph, SphereWithHandles, Thickening


class TestSphereWithHandles(unittest.TestCase):
    def setUp(self):
        self.sphere = SphereWithHandles(0, 0)
        self.torus = SphereWithHandles(1, 0)
        self.torus_with_holes = SphereWithHandles(1, 2)
        self.projective_plane = SphereWithHandles(0, 0, 1)

    def test_euler_characteristic(self):
        """Euler formula tests: 2 - 2g - h"""
        self.assertEqual(self.sphere.euler_characteristic(), 2)
        self.assertEqual(self.torus.euler_characteristic(), 0)
        self.assertEqual(self.torus_with_holes.euler_characteristic(), -2)

    def test_holes_manipulation(self):
        """Holes tests"""
        s = SphereWithHandles(1, 1)
        s.puncture(2)
        self.assertEqual(s.get_holes(), 3)
        s.glue_disk(1)
        self.assertEqual(s.get_holes(), 2)
        s.glue_disk(5)
        self.assertEqual(s.get_holes(), 0)

    def test_addition_orientable(self):
        """Sum tests"""
        double_torus = self.torus + self.torus
        self.assertEqual(double_torus.get_genus(), 2)
        self.assertEqual(double_torus.get_nonorientable_genus(), 0)

    def test_addition_dicks_theorem(self):
        """Dicks theorem tests"""
        klein_bottle_plus_crosscap = self.torus + self.projective_plane
        self.assertEqual(klein_bottle_plus_crosscap.get_genus(), 0)
        self.assertEqual(klein_bottle_plus_crosscap.get_nonorientable_genus(), 3)

    def test_homeomorphism_spheres(self):
        """Homeomorphism tests"""
        other_torus = SphereWithHandles(1, 0)
        self.assertTrue(self.torus.is_homeomorphic_to(other_torus))
        self.assertFalse(self.torus.is_homeomorphic_to(self.sphere))


class TestHieroglyph(unittest.TestCase):
    def test_valid_orientable_words(self):
        """Orientable hieroglyph tests"""
        h = Hieroglyph("abAB")
        self.assertEqual(h.get_ribbons(), 2)
        self.assertEqual(h.get_cross_ribbons(), 1)
        self.assertEqual(h.get_twisted_ribbons(), 0)
        self.assertEqual(h.euler_characteristic(), -1)
        self.assertEqual(h.get_boundary_circles(), 1)

    def test_valid_nonorientable_words(self):
        """Non-orientable hieroglyph tests"""
        h = Hieroglyph("aabb")
        self.assertEqual(h.get_ribbons(), 2)
        self.assertEqual(h.get_twisted_ribbons(), 2)
        self.assertEqual(h.euler_characteristic(), -1)
        self.assertEqual(h.get_boundary_circles(), 1)

    def test_homeomorphism_hieroglyph_to_sphere(self):
        """Homeomorphism tests"""
        torus_h = Hieroglyph("abAB")
        torus_s = SphereWithHandles(1, 1)
        self.assertTrue(torus_h.is_homeomorphic_to(torus_s))

    def test_invalid_words(self):
        """Incorrect words tests"""
        with self.assertRaises(ValueError):
            Hieroglyph("abc")
        with self.assertRaises(ValueError):
            Hieroglyph("aaa")


class TestIsRealizable(unittest.TestCase):
    def test_is_realizable_with_thickening_mock(self):
        """is_realizable tests"""
        torus = SphereWithHandles(1, 0)

        mock_thickening = MagicMock(spec=Thickening)
        mock_thickening.handles.return_value = 1

        self.assertTrue(torus.is_realizable(mock_thickening))

        sphere = SphereWithHandles(0, 0)
        self.assertFalse(sphere.is_realizable(mock_thickening))


if __name__ == '__main__':
    unittest.main()