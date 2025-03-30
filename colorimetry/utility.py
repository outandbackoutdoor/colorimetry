import colorimetry.log


def register_common_parameters(parser):
    parser.add_argument(
        '-l', '--log-filepath',
        help="Redirect logging to a file")

    parser.add_argument(
        '--buffered-logs',
        dest='use_buffered_logs',
        action='store_true',
        help="Buffer logs in order to mitigate effects of volume logging")

    parser.add_argument(
        '-v', '--verbose',
        dest='is_verbose',
        action='store_true',
        help="Show debug logging")

def handle_common_arguments(args):
    colorimetry.log.configure_logging_with_commandline(args)


def get_rgb_tuple_decimals_with_ints(rgb_tuple_decimals):
    """Get fractional RGB values from integers."""

    rgb_tuple_decimals = map(lambda d: float(d) / 255.0, rgb_tuple_decimals)
    return tuple(rgb_tuple_decimals)


def get_rgb_tuple_int_with_rgb_phrase(rgb_phrase):
    """Get RGB integer tuple for the hex expression."""

    assert \
        len(rgb_phrase) == 7, \
        "RGB phrase is not the right length: [{}]".format(rgb_phrase)

    assert \
        rgb_phrase[0] == '#', \
        "RGB phrase does not have the hash prefix: [{}]".format(rgb_phrase)

    r_hex, g_hex, b_hex = rgb_phrase[1:3], rgb_phrase[3:5], rgb_phrase[5:7]

    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def get_ansi_color_block_with_rgb_tuple_int(rgb_tuple_int):
    """Generate colored block for CLI display.

    REF: https://alexwlchan.net/2021/coloured-squares/
    """

    return "\033[48:2::{}:{}:{}m \033[49m".format(*rgb_tuple_int)


def get_rgb_phrase_with_rgb_tuple_int(query_rgb_tuple_int):
    """Get hex expression for RGB color."""

    return '#{:02x}{:02x}{:02x}'.format(*query_rgb_tuple_int)
