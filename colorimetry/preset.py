import logging

import colorimetry.config.color
import colorimetry.binding
import colorimetry.color
import colorimetry.utility

_LOGGER = logging.getLogger(__name__)


def get_deltas_between_rgb_phrase_and_preset_color_name(
        query_rgb_phrase, preset_color_name):

    preset_rgb_phrase = \
        colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES[
            preset_color_name]

    query_hsluv_tuple = \
        colorimetry.color.get_hsluv_tuple_with_rgb_phrase(
            query_rgb_phrase)

    preset_hsluv_tuple = \
        colorimetry.color.get_hsluv_tuple_with_rgb_phrase(
            preset_rgb_phrase)

    hue_delta, \
    sat_delta, \
    lum_delta = \
        colorimetry.color.get_hsluv_deltas(
            query_hsluv_tuple,
            preset_hsluv_tuple)

    return hue_delta, sat_delta, lum_delta

def get_preset_rgb_phrase(preset_name):
    """Return the RGB phrase for the preset color name."""

# TODO(dustin): Add test

    preset_rgb_phrase = \
        colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES[
            preset_name]

    return preset_rgb_phrase

def get_preset_swatch_and_description(preset_name):
    """Return an ANSI block with the color of the given name."""

    preset_rgb_phrase = \
        colorimetry.binding.DEFAULT_COLOR_NAMES_TO_RGB_PHRASES[
            preset_name]


    # RGB

    preset_rgb_tuple_int = \
        colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
            preset_rgb_phrase)

    preset_rgb_phrase = \
        colorimetry.utility.get_rgb_phrase_with_rgb_tuple_int(
            preset_rgb_tuple_int)

    rgb_expression = \
        'RGB={}->{}'.format(
        preset_rgb_tuple_int,
        preset_rgb_phrase)

    # HSLuv

    h, s, l = \
        colorimetry.color.get_hsluv_tuple_with_rgb_tuple_int(
            preset_rgb_tuple_int)

    hsluv_expression = \
        'HSLuv=({}, {:.03f}, {:.03f})'.format(
        h, s, l)


    # Return swatch

    preset_color_block = \
        colorimetry.utility.get_ansi_color_block_with_rgb_tuple_int(
            preset_rgb_tuple_int)

    return \
        "{} {:20} {:30} {}".format(
        preset_color_block * colorimetry.config.color.SWATCH_WIDTH, preset_name,
        rgb_expression, hsluv_expression)
