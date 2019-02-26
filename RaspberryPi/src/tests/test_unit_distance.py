import unittest
import sys
sys.path.append('vision/')
import preprocessor


class TestUnitDistance(unittest.TestCase):

    def test_distance_valid(self):
        centroid1 = [0,0]
        centroid2 = [2,2]

        preprocess = preprocessor.Preprocessor()

        distance = preprocessor.distance(centroid1, centroid2)

        self.assertTrue(distance == 2.828, "Distance calculator in preprocessor incorrectly calculates the distance between centroids")


if __name__ == '__main__':
    unittest.main()