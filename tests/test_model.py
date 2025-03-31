import functools

import colormath.color_objects

import colorimetry.constant
import colorimetry.binding
import colorimetry.testing_support
import colorimetry.model
import colorimetry.utility


# Establish 'lightblue'

_RGB_PHRASE__LIGHTBLUE = '#add8e6'

_RGB_TUPLE_INT__LIGHTBLUE = \
    colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
        _RGB_PHRASE__LIGHTBLUE)

_LAB_TUPLE_FLOAT__LIGHTBLUE = \
    colorimetry.model._convert_rgb_to_labcie(
        _RGB_TUPLE_INT__LIGHTBLUE)

# Establish 'powderblue'

_RGB_PHRASE__POWDERBLUE = '#b0e0e6'

_RGB_TUPLE_INT__POWDERBLUE = \
    colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
        _RGB_PHRASE__POWDERBLUE)

_LAB_TUPLE_FLOAT__POWDERBLUE = \
    colorimetry.model._convert_rgb_to_labcie(
        _RGB_TUPLE_INT__POWDERBLUE)

# Establish 'blue'

_RGB_PHRASE__BLUE = '#0000ff'

_RGB_TUPLE_INT__BLUE = \
    colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
        _RGB_PHRASE__BLUE)

_LAB_TUPLE_FLOAT__BLUE = \
    colorimetry.model._convert_rgb_to_labcie(
        _RGB_TUPLE_INT__BLUE)

# Establish 'deepskublue'

_RGB_PHRASE__DEEPSKYBLUE = '#00bfff'

_RGB_TUPLE_INT__DEEPSKYBLUE = \
    colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
        _RGB_PHRASE__DEEPSKYBLUE)

_LAB_TUPLE_FLOAT__DEEPSKYBLUE = \
    colorimetry.model._convert_rgb_to_labcie(
        _RGB_TUPLE_INT__DEEPSKYBLUE)


_RGB_TUPLE_INT__GRAY = colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(colorimetry.constant.COLOR_CSS_GRAY)


class Test(colorimetry.testing_support.TestBase):
    def _get_float_tuple_as_integers100(self, tuple_floats):
        # These are more reliable for validating

        tuple_ints = map(lambda x: int(x * 100.0), tuple_floats)
        tuple_ints = tuple(tuple_ints)

        return tuple_ints

    def test_get_comparable_color_with_rgb_ints(self):

        labcie_tuple_fn = \
            lambda color_lab: \
                (
                    color_lab.lab_l, \
                    color_lab.lab_a, \
                    color_lab.lab_b
                )

        convert_rgb_to_labcie = \
            functools.partial(
                colorimetry.model._get_comparable_color_with_rgb_ints,
                colormath.color_objects.LabColor,
                labcie_tuple_fn,
                colorimetry.utility.get_rgb_tuple_decimals_with_ints,
                colorimetry.binding.DEFAULT_INPUT_COLOR_MODEL)

        labcie_float_tuple = \
            convert_rgb_to_labcie(
                _RGB_TUPLE_INT__GRAY)

        labcie_int_tuple = \
            self._get_float_tuple_as_integers100(
                labcie_float_tuple)

        expected = (5358, 0, 0)
        self.assertEquals(labcie_int_tuple, expected)

    def test_labcie_distance__ciede2000(self):

        # Calculate short delta

        distance = \
            colorimetry.model._labcie_distance__ciede2000(
                _LAB_TUPLE_FLOAT__LIGHTBLUE,
                _LAB_TUPLE_FLOAT__POWDERBLUE)

        distance = int(distance * 100)
        self.assertEquals(distance, 427)

        # Calculate larger delta

        distance = \
            colorimetry.model._labcie_distance__ciede2000(
                _LAB_TUPLE_FLOAT__LIGHTBLUE,
                _LAB_TUPLE_FLOAT__DEEPSKYBLUE)

        distance = int(distance * 100)
        self.assertEquals(distance, 1557)

    def test_labcie_distance__hyab(self):

        # Calculate short delta

        delta = \
            colorimetry.model._labcie_distance__hyab(
                _LAB_TUPLE_FLOAT__LIGHTBLUE,
                _LAB_TUPLE_FLOAT__POWDERBLUE)

        delta = int(delta * 100)
        self.assertEquals(delta, 703)

        # Calculate larger delta

        delta = \
            colorimetry.model._labcie_distance__hyab(
                _LAB_TUPLE_FLOAT__LIGHTBLUE,
                _LAB_TUPLE_FLOAT__DEEPSKYBLUE)

        delta = int(delta * 100)
        self.assertEquals(delta, 4305)
