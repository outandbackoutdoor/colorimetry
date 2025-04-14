import unittest

import colorimetry.helper.lookup


class Test(unittest.TestCase):
    def test_smooth_rgb_with_phrase__cached(self):

        # Check with purple-like color

        specific_rgb_phrase = '#680B76'

        narrowed_color_name, \
        narrowed_rgb_phrase, \
        general_color_name, \
        general_rgb_phrase = \
            colorimetry.helper.lookup.smooth_rgb_with_phrase__cached(
                specific_rgb_phrase)

        self.assertEqual(narrowed_color_name, 'purple')
        self.assertEqual(narrowed_rgb_phrase, '#800080')
        self.assertEqual(general_color_name, 'purple')
        self.assertEqual(general_rgb_phrase, '#800080')


        # Check with aqua-like color

        specific_rgb_phrase = '#0B7664'

        narrowed_color_name, \
        narrowed_rgb_phrase, \
        general_color_name, \
        general_rgb_phrase = \
            colorimetry.helper.lookup.smooth_rgb_with_phrase__cached(
                specific_rgb_phrase)

        self.assertEqual(narrowed_color_name, 'lightseagreen')
        self.assertEqual(narrowed_rgb_phrase, '#20b2aa')
        self.assertEqual(general_color_name, 'green')
        self.assertEqual(general_rgb_phrase, '#008000')


        # Check with orange-like color

        specific_rgb_phrase = '#76560B'

        narrowed_color_name, \
        narrowed_rgb_phrase, \
        general_color_name, \
        general_rgb_phrase = \
            colorimetry.helper.lookup.smooth_rgb_with_phrase__cached(
                specific_rgb_phrase)

        self.assertEqual(narrowed_color_name, 'darkgoldenrod')
        self.assertEqual(narrowed_rgb_phrase, '#b8860b')
        self.assertEqual(general_color_name, 'yellow')
        self.assertEqual(general_rgb_phrase, '#ffff00')
