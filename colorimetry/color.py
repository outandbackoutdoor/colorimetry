import logging
import collections

import hsluv

import colorimetry.constant
import colorimetry.config.color
import colorimetry.binding
import colorimetry.model
import colorimetry.css
import colorimetry.utility

_LOGGER = logging.getLogger(__name__)


_OUTLIER_FLAGS = \
    collections.namedtuple(
        'OUTLIER_FLAGS', [

            # Specified in the order in which they should be checked
            'is_black',
            'is_grey',
            'is_white',
        ])


def get_hsluv_tuple_with_rgb_tuple_int(color_rgb_tuple_int):
    """Get HSLuv tuple given the RGB tuple."""

    color_rgb_tuple_float = \
        colorimetry.utility.get_rgb_tuple_decimals_with_ints(
            color_rgb_tuple_int)

    color_hsluv_tuple = \
        hsluv.rgb_to_hsluv(
            color_rgb_tuple_float)

    return color_hsluv_tuple


_NAMES_TO_RGB_TUPLE_INTS = {
    name: colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(rgb_phrase)
    for name, rgb_phrase
    in colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES.items()
}

_NAMES_AND_RGB_TUPLE_INTS_AND_HSLUV_TUPLE_FLOATS = [
    (
        name,
        rgb_tuple_int,
        get_hsluv_tuple_with_rgb_tuple_int(rgb_tuple_int),
    )

    for name, rgb_tuple_int
    in _NAMES_TO_RGB_TUPLE_INTS.items()
]


def get_hsluv_tuple_with_rgb_phrase(rgb_phrase):
    """Get HSLuv tuple given the RGB phrase."""

    rgb_tuple_int = \
        colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
            rgb_phrase)

    hsluv_tuple = \
        get_hsluv_tuple_with_rgb_tuple_int(
            rgb_tuple_int)

    return hsluv_tuple


def get_hsluv_deltas(c1, c2):
    """Compare two colors."""

    hue_delta = abs(c1[0] - c2[0])
    sat_delta = abs(c1[1] - c2[1])
    lum_delta = abs(c1[2] - c2[2])

    return hue_delta, sat_delta, lum_delta


def _is_color_nearby__hsluv(c1, c2):
    """Only allow colors to be matched to nearby hues."""

    hue_delta, sat_delta, lum_delta = get_hsluv_deltas(c1, c2)

    if hue_delta > colorimetry.config.color.MAX_HUE_DELTA:
        return False

    return True


def get_nearby_colors_with_rgb_tuple_int(query_rgb_tuple_int):
    """Determine which presets are in the neighborhood of the color being
    queries based on HSLuv hue band proximity).
    """

    query_hsluv_tuple = get_hsluv_tuple_with_rgb_tuple_int(query_rgb_tuple_int)

    filtered = [
        (
            name,
            rgb_tuple_int,
        )

        for name, rgb_tuple_int, hsluv_tuple
        in _NAMES_AND_RGB_TUPLE_INTS_AND_HSLUV_TUPLE_FLOATS
        if _is_color_nearby__hsluv(hsluv_tuple, query_hsluv_tuple)
    ]

    assert \
        filtered, \
        "Found no neighbors for HSLuv {}. You might need to add more preset " \
            "colors: RGB {} -> {}".format(
            query_hsluv_tuple, query_rgb_tuple_int,
            colorimetry.utility.get_rgb_phrase_with_rgb_tuple_int(query_rgb_tuple_int))


    return filtered


def classify_outliers_with_rgb_tuple_int(color_rgb_tuple_int):
    """Identify any peculiarities with the given color that might need special
    handling.
    """

    color_hsluv_tuple = get_hsluv_tuple_with_rgb_tuple_int(color_rgb_tuple_int)

    h, s, l = color_hsluv_tuple

    outliers = \
        _OUTLIER_FLAGS(
            is_black=l <= colorimetry.config.color.THRESHOLDS.black_lum_max,
            is_white=s <= colorimetry.config.color.THRESHOLDS.white_sat_max and l >= colorimetry.config.color.THRESHOLDS.white_lum_min,
            is_grey=s <= colorimetry.config.color.THRESHOLDS.grey_sat_max)

    if outliers.is_black is False and \
       outliers.is_white is False and \
       outliers.is_grey is False:
        return None

    return outliers


def find_nearby_color_distances_and_names(match_rgb_tuple_int):
    """Get list of nearby colors and distances."""

    query_matchcolormodel_tuple_int = \
        colorimetry.model.MATCHCOLORMODEL_CONVERT_FN(
            match_rgb_tuple_int)


    # Determine which preset colors are in a nearby hue

    neighbor_names_and_rgb_tuple_ints = \
        get_nearby_colors_with_rgb_tuple_int(
            match_rgb_tuple_int)

    neighbor_names_and_matchcolormodel_tuple_ints = \
        map(
            lambda pair: (
                pair[0],
                colorimetry.model.MATCHCOLORMODEL_CONVERT_FN(pair[1])
            ),

            neighbor_names_and_rgb_tuple_ints)


    # Calculate distances

    distances_and_names = \
        map(
            lambda pair: (
                colorimetry.model.MATCHCOLORMODEL_DISTANCE_FN(
                    query_matchcolormodel_tuple_int,
                    pair[1]),

                pair[0],
            ),

            neighbor_names_and_matchcolormodel_tuple_ints)


    distances_and_names = list(distances_and_names)


    assert \
        distances_and_names, \
        "No nearby colors for RGB {}.".format(match_rgb_tuple_int)

    return distances_and_names


def find_nearest_preset_colors_with_rgb_tuple_int(match_rgb_tuple_int):
    """Return the preset colors that are nearby the given RGB."""

    outliers = classify_outliers_with_rgb_tuple_int(match_rgb_tuple_int)

    if outliers is not None:

        # The order of these is important. Grays are white and black, but white
        # and black are not gray.

        if outliers.is_black is True:
            return \
                None, \
                colorimetry.constant.COLOR_NAME_BLACK, \
                colorimetry.constant.COLOR_CSS_BLACK

        elif outliers.is_white is True:
            return \
                None, \
                colorimetry.constant.COLOR_NAME_WHITE, \
                colorimetry.constant.COLOR_CSS_WHITE

        elif outliers.is_grey is True:
            return \
                None, \
                colorimetry.constant.COLOR_NAME_GREY, \
                colorimetry.constant.COLOR_CSS_GREY


    distances_and_names = \
        find_nearby_color_distances_and_names(
            match_rgb_tuple_int)

    # ordered = max(distances_and_names, key=lambda x: x[0])
    ordered = min(distances_and_names, key=lambda x: x[0])

    nearest_name = ordered[1]

    group = colorimetry.binding.DEFAULT_GROUPS_BY_CSS_COLOR[nearest_name]

    return \
        nearest_name, \
        group.name, \
        group.css
