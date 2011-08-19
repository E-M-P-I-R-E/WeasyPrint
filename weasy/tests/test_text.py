# coding: utf8

#  WeasyPrint converts web documents (HTML, CSS, ...) to PDF.
#  Copyright (C) 2011  Simon Sapin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from attest import Tests, assert_hook
import attest

from .. import text


suite = Tests()

FONTS = u"Nimbus Mono L, Liberation Mono, FreeMono, Monospace"

@suite.test
def test_line_content():
    string = u"This is a text for test"
    width = 120
    line = text.TextLineFragment(string, width)
    line.set_font_size(12)
    line.set_font_family(FONTS)
    assert line.get_remaining_text() == u'text for test'
    line.set_width(60)
    assert line.get_remaining_text() == u'is a text for test'
    assert u"%s%s" % (line.get_text(), line.get_remaining_text())  == string


@suite.test
def test_line_with_any_width():
    """
    we don't specify width in order to get the maximum width of the text
    """
    line = text.TextLineFragment(u"some text")
    line.set_font_family(FONTS)
    width = line.get_size()[0]
    line.set_text("some some some text some some some text")
    new_width = line.get_size()[0]

    assert width < new_width

@suite.test
def test_line_breaking():
    string = u"This is a text for test"
    width = 120
    line = text.TextLineFragment(string, width)
    line.set_font_family(FONTS)

    line.set_font_size(12)
    line.set_font_weight(200)
    assert line.get_remaining_text() == u"text for test"

    line.set_font_weight(800)
    assert line.get_remaining_text() == u"text for test"

    line.set_font_size(14)
    assert line.get_remaining_text() == u"text for test"

@suite.test
def test_text_dimension():
    string = u"This is a text for test. This is a test for text.py"
    width = 200
    fragment = text.TextFragment(string, width)
    fragment.set_font_size(12)

    dimension = list(fragment.get_size())
    fragment.set_font_size(20)
    new_dimension = list(fragment.get_size())
    assert dimension[0]*dimension[1] < new_dimension[0]*new_dimension[1]

    dimension = list(fragment.get_size())
    fragment.set_spacing(20)
    new_dimension = list(fragment.get_size())
    assert dimension[0]*dimension[1] < new_dimension[0]*new_dimension[1]


@suite.test
def test_text_other():
    """ Test other properties """
    fragment = text.TextFragment(u"", 40)
    fragment.set_text(u"some text")

    #The default value of alignement property is ``left`` for western script
    assert fragment.layout.get_alignment() == text.ALIGN_PROPERTIES["left"]
    assert not fragment.layout.get_justify()

    for key, value in text.ALIGN_PROPERTIES.iteritems():
        fragment.set_alignment(key)
        assert fragment.layout.get_alignment() == value

    fragment.set_alignment('justify')
    assert fragment.layout.get_justify()


    fragment.justify = True
    assert fragment.justify != False