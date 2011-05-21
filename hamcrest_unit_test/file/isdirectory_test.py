import os
import tempfile
import shutil

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')

from hamcrest.library.file.isdirectory import *

from hamcrest_unit_test.matcher_test import MatcherTest
import unittest

__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

matcher = is_directory()

class PathIsDirectoryTest(MatcherTest):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_file = os.path.join(self.tmp_dir, 'temp_file')
        with open(self.tmp_file, 'w') as f:
            f.write('some data')

    def tearDown(self):
        if self.tmp_dir and os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def testMatchesDirectory(self):
        self.assert_matches("a directory", matcher, self.tmp_dir)

    def testDoesNotMatchFile(self):
        self.assert_does_not_match('a file', matcher, self.tmp_file)

    def testDoesNotMatchNonexistentPaths(self):
        self.assert_does_not_match('garbage', matcher, 'crap')

    def testHasAReadableDescription(self):
        self.assert_description("a path that is a directory", matcher)

    def testSuccessfulMatchDoesNotGenerateMismatchDescription(self):
        self.assert_no_mismatch_description(matcher, self.tmp_dir)

    def testMismatchDescription(self):
        self.assert_mismatch_description("was not a directory", matcher, self.tmp_file)

    def testDescribeMismatch(self):
        self.assert_describe_mismatch("was not a directory", matcher, self.tmp_file)

    def testDescribeMismatch(self):
        self.assert_describe_mismatch("did not exist", matcher, 'crap')


if __name__ == '__main__':
    unittest.main()
