if __name__ == '__main__':
    import sys
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')

from hamcrest.library.collection.issequence_exactlycontaining import *

from hamcrest.core.core.isequal import equal_to
from hamcrest.library.number.ordering_comparison import less_than
from hamcrest_unit_test.matcher_test import MatcherTest
from quasisequence import QuasiSequence
import unittest

__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

class IsSequenceExactlyContainingTest(MatcherTest):

    def testMatchesSingletonList(self):
        self.assert_matches('singleton_list', contains_exactly(equal_to(1)), [1])

    def testDoesNotMatchEmptyListWhenMatchersProvided(self):
        self.assert_does_not_match('empty list',
                                   contains_exactly(equal_to(1)),
                                   [])

    def testMatchesEmptyListWhenNoMatchersProvided(self):
        self.assert_matches('empty list with no matchers',
                            contains_exactly(),
                            [])

    def testMismatchWhenNonconformingElement(self):
        self.assert_does_not_match('outlier element',
                                   contains_exactly(less_than(3)),
                                   [1,2,3])

    def testMismatchWhenNotEveryMatcherIsSatisfied(self):
        self.assert_does_not_match('has an unmatched matcher',
                                   contains_exactly(equal_to(1), equal_to(2)),
                                   [1])

    def testProvidesConvenientShortcutForMatchingWithEqualTo(self):
        self.assert_matches('Values automatically wrapped with equal_to',
                            contains_exactly(less_than(3), 7),
                            [0, 7, 1, 2])

    def testMatchesAnyConformingSequence(self):
        class ObjectWithLenOnly:
            def __len__(self): return 20
        self.assert_matches('quasi-sequence',
                            contains_exactly(less_than(3)), QuasiSequence())
        self.assert_does_not_match('non-sequence', contains_exactly(1), object())
        self.assert_does_not_match('non-sequence with length',
                                   contains_exactly(1), ObjectWithLenOnly())

    def testHasAReadableDescription(self):
        self.assert_description('a sequence consisting of all items matching (<1> or <2>)',
                                contains_exactly(1,2))

    def testDescribeMismatch(self):
        self.assert_describe_mismatch("was 'bad'", contains_exactly(1,2), 'bad')

    def testDescribeMismatchOfNonSequence(self):
        self.assert_describe_mismatch("was <3>", contains_exactly(1,2), 3)


if __name__ == '__main__':
    unittest.main()
