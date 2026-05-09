from python_topology import Graph, Thickening
import unittest


class TestGraph(unittest.TestCase):
    def SetUp(self):
        pass

    def tearDown(self):
        pass

     def test_handles(self):
        K3 = Graph(3,[[1,2],[0,2],[0,1]])
        K4 = Graph(4,[[1,2,3],[0,2,3],[0,1,3],[0,1,2]])
        K5 = Graph(5,[[1,2,3,4],[0,2,3,4],[0,1,3,4],[0,1,2,4],[0,1,2,3]])
        self.assertEqual(K3.handles(),0)
        self.assertEqual(K4.handles(),0)
        self.assertEqual(K5.handles(),1)

    def test_connected(self):
        K3 = Graph(3, [[1, 2], [0, 2], [0, 1]])
        K4 = Graph(4, [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]])
        K5 = Graph(5, [[1, 2, 3, 4], [0, 2, 3, 4], [
                   0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]])
        two_cliques = Graph(
            6, [[1, 2], [0, 2], [0, 1], [4, 5], [3, 5], [3, 4]])
        self.assertTrue(K3.connected())
        self.assertTrue(K3.connected())
        self.assertTrue(K3.connected())
        self.assertFalse(two_cliques.connected())

    def test_deg(self):
        K3 = Graph(3, [[1, 2], [0, 2], [0, 1]])
        K4 = Graph(4, [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]])
        K5 = Graph(5, [[1, 2, 3, 4], [0, 2, 3, 4], [
                   0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]])
        bamboo_4 = Graph(4, [[1], [0, 2], [1, 3], [2]])
        self.assertEqual(K3.deg(0), 2)
        self.assertEqual(K3.deg(1), 2)
        self.assertEqual(K3.deg(2), 2)
        self.assertEqual(K4.deg(0), 3)
        self.assertEqual(K4.deg(1), 3)
        self.assertEqual(K4.deg(2), 3)
        self.assertEqual(K4.deg(3), 3)
        self.assertEqual(K5.deg(0), 4)
        self.assertEqual(K5.deg(1), 4)
        self.assertEqual(K5.deg(2), 4)
        self.assertEqual(K5.deg(3), 4)
        self.assertEqual(K5.deg(4), 4)
        self.assertEqual(bamboo_4.deg(0), 1)
        self.assertEqual(bamboo_4.deg(1), 2)
        self.assertEqual(bamboo_4.deg(2), 2)
        self.assertEqual(bamboo_4.deg(3), 1)


class TestThickening(unittest.TestCase):
    def SetUp(self):
        pass

    def tearDown(self):
        pass

    def test_handles(self):
        K5 = Graph(5, [[1, 2, 3, 4], [0, 2, 3, 4], [
                   0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]])
        self.assertEqual(Thickening(K5, 0).handles(), 2)
        self.assertEqual(Thickening(K5, 1).handles(), 3)
        self.assertEqual(Thickening(K5, 65535).handles(), 2)
        self.assertEqual(Thickening(K5, 45510).handles(), 2)
        self.assertEqual(Thickening(K5, 1156).handles(), 1)


if __name__ == '__main__':
    unittest.main()
