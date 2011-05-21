if __name__ == '__main__':
    import sys
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')

from hamcrest.library.text.patternmatcher import matches_pattern, PatternMatchException
from hamcrest.library.text.patternmatcher.patterns import *

from hamcrest_unit_test.matcher_test import MatcherTest
import unittest

__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"


class PatternMatcherTests(MatcherTest):

    def testMatchesPlainText(self):
        matcher = matches_pattern(text("text"))

        self.assert_matches('', matcher, "text")
        self.assert_does_not_match('', matcher, "xxxtextxxx")
        self.assert_does_not_match('', matcher, "tex")
        self.assert_does_not_match('', matcher, "blah")


    def testMatchesPlainTextContainingSpecialRegexCharacters(self):
        self.assert_matches('', matches_pattern(text("*star*")), "*star*")

        self.assert_matches('', matches_pattern(text("-")), "-")


    def testMatchesSequenceOfText(self):
        matcher = matches_pattern(sequence("hello", " ", "world"))

        self.assert_matches('', matcher, "hello world")


    def testMatchesAlternatives(self):
        matcher = matches_pattern(either(text("hello"), text("world")))

        self.assert_matches('', matcher, "hello")
        self.assert_matches('', matcher, "world")
        self.assert_does_not_match('', matcher, "hello world")


    def testMatchesOptionalPattern(self):
        matcher = matches_pattern(sequence(text("hello"), optional(text(" world"))))

        self.assert_matches('', matcher, "hello")
        self.assert_matches('', matcher, "hello world")
        self.assert_does_not_match('', matcher, " world")


    def testMatchesRepetitionZeroOrMoreTimes(self):
        matcher = matches_pattern(zeroOrMore(text("x")))

        self.assert_matches('', matcher, "")
        self.assert_matches('', matcher, "x")
        self.assert_matches('', matcher, "xxx")
        self.assert_does_not_match('', matcher, " xx")
        self.assert_does_not_match('', matcher, "x x")
        self.assert_does_not_match('', matcher, "xx ")


    def testMatchesRepetitionOneOrMoreTimes(self):
        matcher = matches_pattern(oneOrMore(text("x")))

        self.assert_does_not_match('', matcher, "")
        self.assert_matches('', matcher, "x")
        self.assert_matches('', matcher, "xxx")
        self.assert_does_not_match('', matcher, " xx")
        self.assert_does_not_match('', matcher, "x x")
        self.assert_does_not_match('', matcher, "xx ")


    def testTestCanMatchAnyCharacter(self):
        matcher = matches_pattern(sequence(text("x"), anyCharacter(), text("y")))

        self.assert_matches('', matcher, "x.y")
        self.assert_matches('', matcher, "xzy")
        self.assert_does_not_match('', matcher, "xy")


    def testTestCapturesMatchedGroups(void):
        matcher = matches_pattern(sequence(capture("xs", oneOrMore(text("x"))), capture("ys", oneOrMore(text("y")))))

        parse = matcher.parse("xxxyyy")
        assertEquals("xxx", parse.get("xs"))
        assertEquals("yyy", parse.get("ys"))

        parse = matcher.parse("xxyyyyyy")
        assertEquals("xx", parse.get("xs"))
        assertEquals("yyyyyy", parse.get("ys"))


    def testTestFailsIfDoesNotMatchParseInput(self):
        matcher = matches_pattern(text("expected input"))

        with self.assertRaises(PatternMatchException):
            matcher.parse("input that doesn't match")


    def testTestCanReferToContentOfMatchedGroups(self):
        matcher = matches_pattern(sequence(capture("first", oneOrMore(text("x"))), text("-"), valueOf("first")))

        self.assert_matches('', matcher, "x-x")
        self.assert_matches('', matcher, "xx-xx")

        self.assert_does_not_match('', matcher, "x-xx")
        self.assert_does_not_match('', matcher, "xx-x")


    scopedMatcher = matches_pattern(sequence(capture("xs", oneOrMore(text("x"))), capture("inside", sequence(capture("xs", oneOrMore(text("X"))), valueOf("xs"))), valueOf("xs")))

    def testTestReferencesToGroupsAreLexicallyScoped(self):
        self.assert_matches('', self.scopedMatcher, "xxXXXXxx")
        self.assert_matches('', self.scopedMatcher, "xXXx")
        self.assert_does_not_match('', self.scopedMatcher, "xXxx")
        self.assert_does_not_match('', self.scopedMatcher, "xXXX")


    def testTestNamesInInnerScopesCanBeQueriedUsingDottedPathNotation(self):
        parse = self.scopedMatcher.parse("xxXXXXXXxx")
        assertEquals("xx", parse.get("xs"))
        assertEquals("XXX", parse.get("inside.xs"))


    def testTestCanReferToValuesOfGroupsInInnerScopesUsingDottedPathNotation(self):
        matcher = matches_pattern(sequence(capture("xs", oneOrMore(text("x"))), capture("inside", sequence(capture("xs", oneOrMore(text("X"))), valueOf("xs"))), valueOf("xs"), valueOf("inside.xs")))

        self.assert_matches('', matcher, "xXXXXxXX")
        self.assert_matches('', matcher, "xxXXxxX")


    def testTestCanDefinePatternsInTermsOfExistingPatterns(self):
        emailAddressMatcher = matches_pattern(sequence(capture("user", oneOrMore(anyCharacter())), "@", capture("host", oneOrMore(anyCharacter()))))

        mailToURLMatcher = matches_pattern(sequence(capture("scheme", text("mailto")), ":", capture("email", emailAddressMatcher)))

        self.assert_matches('', matches_pattern(mailToURLMatcher), "mailto:npryce@users.sf.net")


    def testMatchesCharacterInList(self):
        matcher = matches_pattern(anyCharacterIn("0123456789"))

        for i in range(9):
            self.assert_matches('', matcher, str(i))

        self.assert_does_not_match('', matcher, "X")


    def testMatchesCharacterRange(self):
        matcher = matches_pattern(anyCharacterIn("0-9"))

        for i in range(9):
            self.assert_matches('', matcher, str(i))

        self.assert_does_not_match('', matcher, "X")


    def testMatchesCharacterNotInRange(self):
        matcher = matches_pattern(anyCharacterNotIn("0-9"))

        for i in range(9):
            self.assert_does_not_match('', matcher, str(i))

        self.assert_matches('', matcher, "X")


    def testMatchesExactlyTheSpecifiedNumberOfRepetitions(self):
        matcher = matches_pattern(exactly(3, "x"))

        self.assert_does_not_match('', matcher, "xx")
        self.assert_matches('', matcher, "xxx")
        self.assert_does_not_match('', matcher, "xxxx")


    def testMatchesARangeOfAllowableRepetitions(self):
        matcher = matches_pattern(between(3, 5, "x"))

        self.assert_does_not_match('', matcher, "xx")
        self.assert_matches('', matcher, "xxx")
        self.assert_matches('', matcher, "xxxx")
        self.assert_matches('', matcher, "xxxxx")
        self.assert_does_not_match('', matcher, "xxxxxx")


    def testMatchesAListOfMatchedThings(self):
        matcher = matches_pattern(listOf("x"))

        self.assert_matches('', matcher, "")
        self.assert_matches('', matcher, "x")
        self.assert_matches('', matcher, "x,x")
        self.assert_matches('', matcher, "x,x,x,x,x")

        self.assert_does_not_match('', matcher, ",")
        self.assert_does_not_match('', matcher, "x,x,x,")


    def testMatchesAListWithSpecificSeparator(self):
        matcher = matches_pattern(listOf("x").separated_by(":"))

        self.assert_matches('', matcher, "")
        self.assert_matches('', matcher, "x")
        self.assert_matches('', matcher, "x:x")
        self.assert_matches('', matcher, "x:x:x:x:x")

        self.assert_does_not_match('', matcher, "x,x,x")


    def testMatchesWhitespace(self):
        matcher = matches_pattern(sequence("a", whitespace(), "z"))

        self.assert_matches('', matcher, "az")
        self.assert_matches('', matcher, "a z")
        self.assert_matches('', matcher, "a \t z")


    def testMatchesSequenceSeparatedByPattern(self):
        matcher = matches_pattern(
                separatedBy(",", "a", "b", "c"))

        self.assert_matches('', matcher, "a,b,c")
