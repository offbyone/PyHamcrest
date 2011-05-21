from __future__ import absolute_import
import itertools

from . import util

class AnyCharacter(util.BasePatternMatcher):

    def _build_regexp(self, builder, groups):
        builder.append('.')


class CaptureGroup(util.BasePatternMatcher):

    def __init__(self, name, pattern):
        self.name, self.pattern = name, pattern

    def _build_regexp(self, builder, groups):
        subgroups = groups.create(self.name)
        builder.append("(")
        self.pattern._build_regexp(builder, subgroups)
        builder.append(")")


class CharacterInRange(util.BasePatternMatcher):

    def __init__(self, range):
        self.range = range

    def _build_regexp(self, builder, groups):
        builder.extend(["[", self.range, "]"])


class CharacterInUnicodeCategory(util.BasePatternMatcher):

    def __init__(self, categoryname):
        self.categoryname = categoryname

    def _build_regexp(self, builder, groups):
        builder.extend([r'\p{Is', self.categoryname, '}'])


class CharacterNotInRange(util.BasePatternMatcher):

    def __init__(self, range):
        self.range = range

    def _build_regexp(self, builder, groups):
        builder.extend(['[^', self.range, ']'])


class CharacterNotInUnicodeCategory(util.BasePatternMatcher):

    def __init__(self, categoryname):
        self.categoryname = categoryname

    def _build_regexp(self, builder, groups):
        builder.extend([r'\P{Is', self.categoryname, '}'])


class Choice(util.BasePatternMatcher):

    def __init__(self, alternatives):
        self.alternatives = alternatives

    def _build_regexp(self, builder, groups):
        builder.append('(?:')
        started = False
        for alt in self.alternatives:
            if started:
                builder.append('|')
            else:
                started = True

            alt._build_regexp(builder, groups)
        builder.append(')')


class Exactly(util.BasePatternMatcher):

    def __init__(self, number, pattern):
        self.number, self.pattern = number, pattern

    def _build_regexp(self, builder, groups):
        self.pattern._build_regexp(builder, groups)
        builder.extend(['{', self.number, '}'])


class Flags(util.BasePatternMatcher):

    def __init__(self, flags, pattern):
        self.flags, self.pattern = flags, pattern

    def _build_regexp(self, builder, groups):
        builder.extend(['(?', self.flags, ':'])
        self.pattern._build_regexp(builder, groups)
        builder.append(')')


class FromTo(util.BasePatternMatcher):

    def __init__(self, min, max, repeated_pattern):
        self.min, self.max, self.repeated_pattern = min, max, repeated_pattern

    def _build_regexp(self, builder, groups):
        self.repeated_pattern._build_regexp(builder, groups)
        builder.extend(['{', self.min, ',', self.max, '}'])


class GroupReference(util.BasePatternMatcher):

    def __init__(self, name):
        self.name = name

    def _build_regexp(self, builder, groups):
        builder.extend(['\\', groups.resolve(self.name)])


class ListOf(util.BasePatternMatcher):

    def __init__(self, element, separator):
        self.element, self.separator = element, separator

    def _build_regexp(self, builder, groups):
        return Optional(Sequence([
            self.element,
            ZeroOrMore(Sequence([
                self.separator,
                self.element])),
            ]))._build_regexp(builder, groups)

    def separated_by(self, separator):
        return ListOf(self.element, util.to_pattern(separator))


class Literal(util.BasePatternMatcher):

    def __init__(self, literal):
        self.literal = literal

    def _build_regexp(self, builder, groups):
        builder.append(util.quote(self.literal))


class Unquoted(util.BasePatternMatcher):

    def __init__(self, string):
        self.string = string

    def _build_regexp(self, builder, groups):
        builder.append(self.string)


class NullPatternComponent(util.BasePatternMatcher):

    def _build_regexp(self, builder, groups):
        pass


class PatternModifier(util.BasePatternMatcher):

    def __init__(self, pattern):
        self.pattern = pattern

    def _build_regexp(self, builder, groups):
        builder.append('(?:')
        self.pattern._build_regexp(builder, groups)
        builder.append(')')
        self.append_modifier(builder)


class OneOrMore(PatternModifier):

    def append_modifier(self, builder):
        builder.append('+')


class Optional(PatternModifier):

    def append_modifier(self, builder):
        builder.append('?')


class Sequence(util.BasePatternMatcher):

    def __init__(self, alternatives):
        self.alternatives = alternatives[:]

    def _build_regexp(self, builder, groups):
        for a in self.alternatives:
            a._build_regexp(builder, groups)


class ZeroOrMore(PatternModifier):

    def append_modifier(self, builder):
        builder.append('*')


class Path(list):

    @property
    def head(self):
        return self[0]

    @property
    def tail(self):
        return self[1:]


class GroupNamespace(object):

    def __init__(self, parent=None, next_index=itertools.count(0)):
        self.parent, self.next_index = parent, next_index
        self.index = next(next_index)
        self.bindings = {}

    def create(self, name):
        if name in self.bindings:
            raise ValueError('Duplicate name: ' + name)

        child = GroupNamespace(self, self.next_index)
        self.bindings[name] = child
        return child

    def resolve(self, path):
        if isinstance(path, basestring):
            return self.resolve(path_parse(path))
        else:
            return self.environment_containing(path.head).resolve_internally(path.tail)

    def resolve_internally(self, path):
        if (path.size == 0):
            return self.index

        if path.head in self.bindings:
            return self.bindings[path.head].resolve_internally(path.tail)

        raise ValueError('name "' + path.head + '" not bound')

    def environment_containing(self, name):
        if name in self.bindings:
            return self.bindings[name]

        if parent is not None:
            return parent.environment_containing(name)

        raise ValueError('name "' + name + '" not bound')
