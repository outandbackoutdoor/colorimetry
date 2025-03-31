# Overview

This library provides tools to approximate a multitude of colors (as identified
by RGBs) to both standard colors and specific color groups (as defined by this
project).


# Algorithm

1. Determine if the color is black, white, or grey. If so, return that name and
   the configured CSS color for it.

2. Convert the color to the HSLuv color model, and identify all standard colors
   within neighboring hues

3. Convert the principal color and all candidate colors to the LAB color model

4. Use CIEDE2000 to calculate the distance between the color and all
   candidates

5. Take the color with the smallest distance as the nearest match

6. Retrieve the group of the matched color, and return both the match and the
   group


# Useful Functions

## colorimetry.color

`find_nearest_preset_colors_with_rgb_tuple_int()`

This does the primary task of this project, to find the nearest matching color
and group of a given color.

`get_nearby_colors_with_rgb_tuple_int()`

Returns colors considered to be similar to the queries color. The 'best' match
will come from this group (if it's not just black, white, or grey).

`classify_outliers_with_rgb_tuple_int()`

Classifies the given color as black, white, or grey. If none of these apply,
then returns None. Depends on thresholds config in `colorimetry.config.color`.

`find_nearby_color_distances_and_names()`

Returns all 'nearby' colors (see above), along with distances.


## colorimetry.utility

`get_ansi_color_block_with_rgb_tuple_int()`

Get a printable ANSI block for the given RGB.

## colorimetry.preset

A "preset" color refers to the hardcoded CSS colors, RGBs, and groups.

`get_deltas_between_rgb_phrase_and_preset_color_name()`

Get the deltas of the HSL components between the given RGB and the preset color.

`get_preset_swatch_and_description()`

Get a printable ANSI block for the given preset color.

## colorimetry.css

`CSS3_NAMES_TO_RGB_PHRASES`

A dictionary of CSS names to RGBs (expressed in CSS notation)

`CSS3_GROUPS_BY_CSS_COLOR`

A dictionary of CSS names to groups


# Configuration

## colorimetry.config.color

`MAX_HUE_DELTA`

The max hue difference to consider for neighbors of the searched colors.

`THRESHOLDS`

The various thresholds used to identify black, white, and grey colors.

## colorimetry.binding

`DEFAULT_INPUT_COLOR_MODEL`

Defines which model to use for RGB colors (sRGB by default).

`DEFAULT_COLOR_NAMES_TO_RGB_PHRASES`

Defines which set of CSS colors to use (currently, only one set is available).

`DEFAULT_GROUPS_BY_CSS_COLOR`

Defines a dictionary of dictionaries where the outer dictionary is keyed by
group names and RGBs, and the inner dictionary is a list of names. All CSS names
must be representated.

## colorimetry.model

`MATCHCOLORMODEL_CONVERT_FN`

Defines color model conversion function for the distance function (LAB).

`MATCHCOLORMODEL_DISTANCE_FN`

Defines the function to use for calculating distances (currently CIEDE2000).


# Tools

`color_match`

Does a match for a single color. Prints verbosity useful for drilling into
matches, including the HSLuv of the query, a printed swatch of the query, any
identified outlier attributes, and all neighbors (and their swatches) sorted by
distance.

`color_hsluv_grids`

Step through hues at even intervals and display one ANSI grid with all S and
all L for that hue. This supports investigating matches and nearby colors.


# Screenshots

A real-world comparison between brand-specific colors/RGBs and the color groups
they were matched to:

![Trial Matches](assets/documentation/trial1.png)

The match tool:

![Match Tool](assets/documentation/match1.png)

The grid-printing tool:

![Grid-Printing Tool](assets/documentation/grids1.png)
