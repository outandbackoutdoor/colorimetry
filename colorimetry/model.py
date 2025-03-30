import logging
import functools

import colormath.color_conversions
import colormath.color_objects

import pyciede2000

import colour

import colorimetry.binding
import colorimetry.utility

_LOGGER = logging.getLogger(__name__)


def _get_comparable_color_with_rgb_ints(
        output_model, output_tuple_fn, input_condition_fn, input_model,
        rgb_tuple):
    """Get CIE-LAB color given an tuple of ints representing an RGB.

    REF: https://python-colormath.readthedocs.io/en/latest/conversions.html
    """

    if input_condition_fn is not None:
        rgb_tuple = input_condition_fn(rgb_tuple)

    r, g, b = rgb_tuple

    input_color = \
        input_model(
            r,
            g,
            b)

    color_other = \
        colormath.color_conversions.convert_color(
            input_color,
            output_model)

    color_output_tuple = output_tuple_fn(color_other)
    return color_output_tuple


_labcie_tuple_fn = \
    lambda color_lab: \
        (
            color_lab.lab_l, \
            color_lab.lab_a, \
            color_lab.lab_b
        )

_convert_rgb_to_labcie = \
    functools.partial(
        _get_comparable_color_with_rgb_ints,
        colormath.color_objects.LabColor,
        _labcie_tuple_fn,
        colorimetry.utility.get_rgb_tuple_decimals_with_ints,
        colorimetry.binding.DEFAULT_INPUT_COLOR_MODEL)


def _labcie_distance__ciede2000(c1, c2):
    """Use CIEDE2000 to calculate the distance."""

    result = pyciede2000.ciede2000(c1, c2)

    return result['delta_E_00']


def _labcie_distance__hyab(c1, c2):
    """Use HyAB to calculate the distance. HyAB is more resistant against
    distortion due to large differences, theoretically, though our own
    experience has yet to verify that.
    """

    distance = colour.difference.delta_E(c1, c2, method="HyAB")
    return distance


MATCHCOLORMODEL_CONVERT_FN = _convert_rgb_to_labcie

# TODO(dustin): HyAB is supposed be at least as good as CIEDE2000 in the normal
#               situation and better with large differences, but there's few
#               references and implementations online that we can't be confident
#               in its operation or validate its results against anything.
# MATCHCOLORMODEL_DISTANCE_FN = _labcie_distance__hyab
MATCHCOLORMODEL_DISTANCE_FN = _labcie_distance__ciede2000
