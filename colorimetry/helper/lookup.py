import functools

import colorimetry.color
import colorimetry.preset
import colorimetry.utility


@functools.lru_cache(maxsize=1000)
def smooth_rgb_with_phrase__cached(specific_rgb_phrase):
    """Determine the nearest color match to the given color as well as the group
    of colors it comes from. Cache result.
    """

    color_tuple_int = \
        colorimetry.utility.get_rgb_tuple_int_with_rgb_phrase(
            specific_rgb_phrase)

    narrowed_color_name, \
    general_color_name, \
    general_rgb_phrase = \
        colorimetry.color.find_nearest_preset_colors_with_rgb_tuple_int(
            color_tuple_int)

    if narrowed_color_name is None:
        narrowed_rgb_phrase = None

    else:
        narrowed_rgb_phrase = \
            colorimetry.preset.get_preset_rgb_phrase(
                narrowed_color_name)

    return \
        narrowed_color_name, \
        narrowed_rgb_phrase, \
        general_color_name, \
        general_rgb_phrase
