
import colorimetry.testing_support
import colorimetry.preset


class Test(colorimetry.testing_support.TestBase):
    def _get_hsluv_as_integers100(self, hsluv_tuple):
        # These are more reliable for validating

        hsluv_tuple__ints = map(lambda x: int(x * 100.0), hsluv_tuple)
        hsluv_tuple__ints = tuple(hsluv_tuple__ints)

        return hsluv_tuple__ints

    def test_get_deltas_between_rgb_phrase_and_preset_color_name(self):

        # Compare "salmon" to "red"

        rgb_phrase = '#fa8072'
        preset_name = 'red'

        deltas = \
            colorimetry.preset.get_deltas_between_rgb_phrase_and_preset_color_name(
                rgb_phrase,
                preset_name)

        deltas = self._get_hsluv_as_integers100(deltas)

        expected = (465, 745, 1402)
        self.assertEquals(deltas, expected)


        # Compare "lightsalmon" to "red". It's further from the principal than
        # the previous.

        rgb_phrase = '#ffa07a'
        preset_name = 'red'

        deltas = \
            colorimetry.preset.get_deltas_between_rgb_phrase_and_preset_color_name(
                rgb_phrase,
                preset_name)

        deltas = self._get_hsluv_as_integers100(deltas)

        expected = (1605, 0, 2146)
        self.assertEquals(deltas, expected)


        # Compare "pink" to "red". It's further from the principal than the
        # previous.

        rgb_phrase = '#ffc0cb'
        preset_name = 'red'

        deltas = \
            colorimetry.preset.get_deltas_between_rgb_phrase_and_preset_color_name(
                rgb_phrase,
                preset_name)

        deltas = self._get_hsluv_as_integers100(deltas)

        expected = (1152, 0, 3034)
        self.assertEquals(deltas, expected)

    def test_get_preset_swatch_and_description(self):

        s = colorimetry.preset.get_preset_swatch_and_description('red')

        expected = """\
[48:2::255:0:0m [49m[48:2::255:0:0m [49m[48:2::255:0:0m [49m[48:2::255:0:0m [49m[48:2::255:0:0m [49m red                  RGB=(255, 0, 0)->#ff0000       HSLuv=(12.177050630061776, 100.000, 53.237)"""

        self.assertEquals(s, expected)
