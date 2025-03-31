import unittest

import colorimetry.constant
import colorimetry.testing_support
import colorimetry.color
import colorimetry.binding
import colorimetry.utility

_RGB_PHRASE_RED = '#ff0000'
_RGB_PHRASE_GREEN = '#00ff00'
_RGB_PHRASE_BLUE = '#0000ff'

_RGB_TUPLE_INT__BLACK = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(colorimetry.constant.COLOR_CSS_BLACK)
_RGB_TUPLE_INT__WHITE = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(colorimetry.constant.COLOR_CSS_WHITE)
_RGB_TUPLE_INT__GRAY = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(colorimetry.constant.COLOR_CSS_GRAY)


class Test(colorimetry.testing_support.TestBase):
    def _get_hsluv_as_integers100(self, hsluv_tuple):
        # These are more reliable for validating

        hsluv_tuple__ints = map(lambda x: int(x * 100.0), hsluv_tuple)
        hsluv_tuple__ints = tuple(hsluv_tuple__ints)

        return hsluv_tuple__ints

    def test_get_hsluv_tuple_with_rgb_tuple_int(self):

        rgb_tuple_int = (255, 0, 0)

        hsluv_tuple = \
            colorimetry.color.get_hsluv_tuple_with_rgb_tuple_int(
                rgb_tuple_int)

        hsluv_tuple__ints = self._get_hsluv_as_integers100(hsluv_tuple)

        # (12.177050630061776, 100.00000000000222, 53.23711559542933)
        expected = (1217, 10000, 5323)
        self.assertEquals(hsluv_tuple__ints, expected)

    def test_get_hsluv_deltas(self):

        # Less and more

        c1 = (33, 44, 55)
        c2 = (99, 88, 77)

        deltas = colorimetry.color.get_hsluv_deltas(c1, c2)

        expected = (66, 44, 22)
        self.assertEquals(deltas, expected)


        # More and less. We've used slightly different arguments than the theme
        # of the previous in order to assure a slightly different result (and
        # that we don't have a bug that results in always returning the same
        # result).

        c1 = (89, 78, 67)
        c2 = (22, 33, 44)

        deltas = colorimetry.color.get_hsluv_deltas(c1, c2)

        expected = (67, 45, 23)
        self.assertEquals(deltas, expected)

    def test_get_hsluv_tuple_with_rgb_phrase(self):

        # Common red

        hsluv_tuple = colorimetry.color.get_hsluv_tuple_with_rgb_phrase(_RGB_PHRASE_RED)
        hsluv_tuple__ints = self._get_hsluv_as_integers100(hsluv_tuple)

        expected = (1217, 10000, 5323)
        self.assertEquals(hsluv_tuple__ints, expected)


        # Common blue

        hsluv_tuple = colorimetry.color.get_hsluv_tuple_with_rgb_phrase(_RGB_PHRASE_BLUE)
        hsluv_tuple__ints = self._get_hsluv_as_integers100(hsluv_tuple)

        expected = (26587, 10000, 3230)
        self.assertEquals(hsluv_tuple__ints, expected)


        # Purple (a color in the middle)

        hsluv_tuple = colorimetry.color.get_hsluv_tuple_with_rgb_phrase('#6c2c6c')
        hsluv_tuple__ints = self._get_hsluv_as_integers100(hsluv_tuple)

        expected = (30771, 6671, 2959)
        self.assertEquals(hsluv_tuple__ints, expected)

    def test_is_color_nearby__hsluv(self):

        hsluv_tuple__red = colorimetry.color.get_hsluv_tuple_with_rgb_phrase(_RGB_PHRASE_RED)
        hsluv_tuple__orangered = colorimetry.color.get_hsluv_tuple_with_rgb_phrase('#ff4500')
        hsluv_tuple__orange = colorimetry.color.get_hsluv_tuple_with_rgb_phrase('#ffa500')

        self.assertTrue(colorimetry.color._is_color_nearby__hsluv(hsluv_tuple__red, hsluv_tuple__orangered))
        self.assertFalse(colorimetry.color._is_color_nearby__hsluv(hsluv_tuple__red, hsluv_tuple__orange))

    def test_get_nearby_colors_with_rgb_tuple_int(self):

        rgb_tuple_int__red = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(_RGB_PHRASE_RED)
        rgb_tuple_int__orangered = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase('#ff4500')
        rgb_tuple_int__orange = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase('#ffa500')

        nearby = colorimetry.color.get_nearby_colors_with_rgb_tuple_int(rgb_tuple_int__red)

        key = ('orangered', rgb_tuple_int__orangered)
        self.assertIn(key, nearby)

        key = ('orange', rgb_tuple_int__orange)
        self.assertNotIn(key, nearby)

    def test_classify_outliers_with_rgb_tuple_int(self):

        outliers = colorimetry.color.classify_outliers_with_rgb_tuple_int(_RGB_TUPLE_INT__BLACK)
        self.assertEquals(outliers, colorimetry.color._OUTLIER_FLAGS(is_black=True, is_gray=True, is_white=False))


        outliers = colorimetry.color.classify_outliers_with_rgb_tuple_int(_RGB_TUPLE_INT__WHITE)
        self.assertEquals(outliers, colorimetry.color._OUTLIER_FLAGS(is_black=False, is_gray=True, is_white=True))


        gray_rgb_phrase = colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES[colorimetry.constant.COLOR_NAME_GRAY]
        rgb_tuple_int__gray = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(gray_rgb_phrase)

        outliers = colorimetry.color.classify_outliers_with_rgb_tuple_int(rgb_tuple_int__gray)
        self.assertEquals(outliers, colorimetry.color._OUTLIER_FLAGS(is_black=False, is_gray=True, is_white=False))


        rgb_tuple_int__red = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(_RGB_PHRASE_RED)

        outliers = colorimetry.color.classify_outliers_with_rgb_tuple_int(rgb_tuple_int__red)
        self.assertIsNone(outliers)

    def test_find_nearby_color_distances_and_names(self):

        orangered_rgb_phrase = colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES['orangered']
        rgb_tuple_int__red = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(orangered_rgb_phrase)

        distances_and_names = \
            colorimetry.color.find_nearby_color_distances_and_names(
                rgb_tuple_int__red)

        distances_and_names = \
            map(
                lambda pair: (int(pair[0] * 100.0), pair[1]),
                distances_and_names)

        distances_and_names = sorted(distances_and_names)
        distances_and_names = distances_and_names[:5]

        expected = [
            (0, 'orangered'),
            (639, 'red'),
            (812, 'tomato'),
            (1063, 'coral'),
            (1092, 'chocolate'),
        ]

        self.assertEquals(distances_and_names, expected)

    def test_find_nearest_preset_colors_with_rgb_tuple_int(self):

        # Black

        nearest_name, \
        group_name, \
        group_css = \
            colorimetry.color.find_nearest_preset_colors_with_rgb_tuple_int(
                _RGB_TUPLE_INT__BLACK)

        # Outlier colors don't return a nearest name
        self.assertIsNone(nearest_name)

        self.assertEquals(group_name, colorimetry.constant.COLOR_NAME_BLACK)
        self.assertEquals(group_css, colorimetry.constant.COLOR_CSS_BLACK)

        # White

        nearest_name, \
        group_name, \
        group_css = \
            colorimetry.color.find_nearest_preset_colors_with_rgb_tuple_int(
                _RGB_TUPLE_INT__WHITE)

        # Outlier colors don't return a nearest name
        self.assertIsNone(nearest_name)

        self.assertEquals(group_name, colorimetry.constant.COLOR_NAME_WHITE)
        self.assertEquals(group_css, colorimetry.constant.COLOR_CSS_WHITE)

        # Gray

        nearest_name, \
        group_name, \
        group_css = \
            colorimetry.color.find_nearest_preset_colors_with_rgb_tuple_int(
                _RGB_TUPLE_INT__GRAY)

        # Outlier colors don't return a nearest name
        self.assertIsNone(nearest_name)

        self.assertEquals(group_name, colorimetry.constant.COLOR_NAME_GRAY)
        self.assertEquals(group_css, colorimetry.constant.COLOR_CSS_GRAY)

        # A color with some actual color. A grayish blue.

        _rgb_tuple_int__lightblue = \
            colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
                '#728582')

        nearest_name, \
        group_name, \
        group_css = \
            colorimetry.color.find_nearest_preset_colors_with_rgb_tuple_int(
                _rgb_tuple_int__lightblue)

        self.assertEquals(nearest_name, 'cadetblue')
        self.assertEquals(group_name, 'blue')
        self.assertEquals(group_css, _RGB_PHRASE_BLUE)
