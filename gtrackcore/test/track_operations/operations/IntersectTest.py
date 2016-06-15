
import unittest
import numpy as np
from collections import OrderedDict

from gtrackcore.track_operations.operations.Intersect import Intersect
from gtrackcore.metadata import GenomeInfo
from gtrackcore.track.core.GenomeRegion import GenomeRegion
from gtrackcore.track_operations.TrackContents import TrackContents
from gtrackcore.test.track_operations.TestUtils import createTrackView
from gtrackcore.test.track_operations.TestUtils import \
    createSimpleTestTrackContent

class IntersectTest(unittest.TestCase):
    """
    Template class for creating track_operations tests.
    """

    def setUp(self):
        self.chr1 = (GenomeRegion('hg19', 'chr1', 0, GenomeInfo.GENOMES['hg19']['size']['chr1']))
        self.chromosomes = (GenomeRegion('hg19', c, 0, l)
                            for c, l in GenomeInfo.GENOMES['hg19']['size'].iteritems())

    def _runIntersectTest(self, startsA, endsA, startsB, endsB, expStarts,
                          expEnds, allowOverlap=False,
                          resultAllowOverlap=False):

        trackA = createSimpleTestTrackContent(startList=startsA, endList=endsA)
        trackB = createSimpleTestTrackContent(startList=startsB, endList=endsB)

        u = Intersect(trackA, trackB, allowOverlap=allowOverlap)
        tc = u()

        for (k, v) in tc.getTrackViews().items():

            if cmp(k, self.chr1) == 0:
                # All test tracks are in chr1
                self.assertTrue(np.array_equal(v.startsAsNumpyArray(), expStarts))
                self.assertTrue(np.array_equal(v.endsAsNumpyArray(), expEnds))
            else:
                # Tests if all tracks no in chr1 have a size of 0.
                self.assertEqual(v.startsAsNumpyArray().size, 0)
                self.assertEqual(v.endsAsNumpyArray().size, 0)

    def _createTrackContent(self, starts, ends):
        """
        Create a track view a start, end list pair.
        Help method used in testing. This method will create a hg19 tracks with
        data in chromosome 1 only.
        :param starts: List of track start positions
        :param ends: List of track end positions
        :return: A TrackContent object
        """
        starts = np.array(starts)
        ends = np.array(ends)
        tv = createTrackView(region=self.chr1, startList=starts, endList=ends,
                             allow_overlap=False)
        d = OrderedDict()
        d[self.chr1] = tv
        return TrackContents('hg19', d)

    def testNoIntersect(self):
        """
        No intersect between A and B
        Test for case 1
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[4], startsB=[5], endsB=[8], expStarts=[],
                           expEnds=[])

    def testTotalIntersect(self):
        """
        A == b
        :return: None
        """
        self._runIntersectTest(startsA=[2, 6], endsA=[4, 8], startsB=[2, 6], endsB=[4, 8], expStarts=[2, 6],
                              expEnds=[4, 8])

    def testABeforeBIntersect(self):
        """
        A intersects B at the end of A
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[6], startsB=[4], endsB=[8], expStarts=[4],
                              expEnds=[6])

    def testBBeforeAIntersect(self):
        """
        B intersects A at the end of B
        :return: None
        """
        self._runIntersectTest(startsA=[4], endsA=[8], startsB=[2], endsB=[6], expStarts=[4],
                              expEnds=[6])

    def testAInsideBIntersect(self):
        """
        A is totally inside B
        :return: None
        """
        self._runIntersectTest(startsA=[4], endsA=[6], startsB=[2], endsB=[8], expStarts=[4],
                              expEnds=[6])

    def testBInsideAIntersect(self):
        """
        B is totally inside A
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[8], startsB=[4], endsB=[6], expStarts=[4],
                              expEnds=[6])

    def testAInsideBStartIntersect(self):
        """
        A is totally inside B, Start of A equals start of B
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[4], startsB=[2], endsB=[8], expStarts=[2],
                              expEnds=[4])

    def testBInsideAStartIntersect(self):
        """
        B is totally inside A, Start of A equals start of B
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[8], startsB=[2], endsB=[4], expStarts=[2],
                              expEnds=[4])

    def testAInsideBEndIntersect(self):
        """
        A is totally inside B, End of A equals start of B
        :return: None
        """
        self._runIntersectTest(startsA=[6], endsA=[8], startsB=[2], endsB=[8], expStarts=[6],
                              expEnds=[8])

    def testBInsideAEndIntersect(self):
        """
        B is totally inside A, End of A equals start of B
        :return: None
        """
        self._runIntersectTest(startsA=[2], endsA=[8], startsB=[6], endsB=[8], expStarts=[6],
                              expEnds=[8])

    def testMultipleIntersect(self):
        """
        B overlaps multiple segments in A
        :return: None
        """
        self._runIntersectTest(startsA=[2,6], endsA=[4, 10], startsB=[3], endsB=[8], expStarts=[3, 6],
                              expEnds=[4,8])


if __name__ == "__main__":
    unittest.main()

