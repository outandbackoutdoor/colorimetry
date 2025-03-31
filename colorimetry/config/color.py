import collections


SWATCH_WIDTH = 5

MAX_HUE_DELTA = 20

# Our ranges are determined in terms of counts of the blocks in the grids
# printed by ss_color_hsluv_grids
HSL_GRID_SQUARE_SIZE = 10.0


_THRESHOLDS_CLS = \
    collections.namedtuple(
        '_THRESHOLDS', [
            'black_lum_max',
            'white_sat_max',
            'white_lum_min',
            'gray_sat_max',
        ])

THRESHOLDS = \
    _THRESHOLDS_CLS(
        # These values determined by trial and error using the 'ss_color_match'
        # and 'ss_color_hsluv_grids' scripts.
        #
        # The hue is out of 360, but S and L are out of 100.

        # It has proven difficult to add enough colors to cover the *nearly*
        # black luminocities, even though they're still visually discernable as
        # non-black.
        black_lum_max=2.0 / HSL_GRID_SQUARE_SIZE * 100.0,
        white_sat_max=2.0 / HSL_GRID_SQUARE_SIZE * 100.0,
        white_lum_min=9.0 / HSL_GRID_SQUARE_SIZE * 100.0,
        gray_sat_max=1.0 / HSL_GRID_SQUARE_SIZE * 100.0,
    )
