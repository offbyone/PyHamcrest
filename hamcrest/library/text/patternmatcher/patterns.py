__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

from ._ast import *
from . import util

def text(text):
    return Literal(text)

def anyCharacter():
    return AnyCharacter()

def anyCharacterIn(range):
    return CharacterInRange(range)

def anyCharacterNotIn(range):
    return CharacterNotInRange(range)

# def anyCharacterInCategory(category):
#     return CharacterInUnicodeCategory(category)

# def anyCharacterNotInCategory(category):
#     return CharacterNotInUnicodeCategory(category)

def either(*alternatives):
    return Choice(to_patterns(*alternatives))

def sequence(*elements):
    return Sequence(to_patterns(*elements))

def optional(o):
    return Optional(util.to_pattern(o))

def zeroOrMore(o):
    return ZeroOrMore(util.to_pattern(o))

def oneOrMore(o):
    return OneOrMore(util.to_pattern(o))

def capture(name, pattern):
    return CaptureGroup(name, pattern)

def valueOf(name):
    return GroupReference(name)

def exactly(requiredCount, o):
    return Exactly(requiredCount, util.to_pattern(o))

def between(minimumCount, maximumCount, o):
    return FromTo(minimumCount, maximumCount, util.to_pattern(o))

def listOf(element):
    return ListOf(util.to_pattern(element), util.to_pattern(","));

def whitespace():
    return ZeroOrMore(Unquoted(r'\s'))

def separatedBy(separator, *elements):
    separated = [elements[0]] if elements else []
    for e in elements[1:]:
        separated.append(separator)
        separated.append(e)

    return sequence(*separated)

def to_patterns(*args):
    return [util.to_pattern(a) for a in args]
