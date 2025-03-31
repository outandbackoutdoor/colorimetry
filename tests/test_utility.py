import unittest

import colorimetry.utility
import colorimetry.testing_support


class Test(colorimetry.testing_support.TestBase):
    def test_get_rgb_tuple_int_with_rgb_phrase(self):

        rgb_phrase = '#ff0000'

        rgb_tuple_int = \
            colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
                rgb_phrase)

        self.assertEquals(rgb_tuple_int, (0xff, 0x0, 0x0))


        recovered = \
            colorimetry.utility.get_rgb_tuple_decimals_with_ints(
                rgb_tuple_int)

        self.assertEquals(recovered, (1.0, 0.0, 0.0))


        block = \
            colorimetry.utility.get_ansi_color_block_with_rgb_tuple_int(
                rgb_tuple_int)

        expected = '[48:2::255:0:0m [49m'
        self.assertEquals(block, expected)


        recovered = colorimetry.utility.get_rgb_phrase_with_rgb_tuple_int(rgb_tuple_int)
        self.assertEquals(recovered, rgb_phrase)


    test_get_rgb_tuple_int_with_rgb_phrase = test_get_rgb_tuple_int_with_rgb_phrase
    test_test_get_ansi_color_block_with_rgb_tuple_int = test_get_rgb_tuple_int_with_rgb_phrase
    test_get_rgb_phrase_with_rgb_tuple_int = test_get_rgb_tuple_int_with_rgb_phrase
