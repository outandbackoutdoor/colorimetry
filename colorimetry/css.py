import collections

import colorimetry.constant


CSS3_NAMES_TO_RGB_PHRASES = {
    'aliceblue': '#f0f8ff',
    'antiquewhite': '#faebd7',
    'aqua': '#00ffff',
    'aquamarine': '#7fffd4',
    'azure': '#f0ffff',
    'beige': '#f5f5dc',
    'bisque': '#ffe4c4',
    'black': '#000000',
    'blanchedalmond': '#ffebcd',
    'blue': '#0000ff',

    'blueviolet': '#8a2be2',
    'brown': '#a52a2a',
    'burlywood': '#deb887',
    'cadetblue': '#5f9ea0',
    'chartreuse': '#7fff00',
    'chocolate': '#d2691e',
    'coral': '#ff7f50',
    'cornflowerblue': '#6495ed',
    'cornsilk': '#fff8dc',
    'crimson': '#dc143c',

    'darkblue': '#00008b',
    'darkcyan': '#008b8b',
    'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9',
    'darkgreen': '#006400',
    'darkkhaki': '#bdb76b',
    'darkmagenta': '#8b008b',
    'darkolivegreen': '#556b2f',

    'darkorange': '#ff8c00',
    'darkorchid': '#9932cc',
    'darkred': '#8b0000',
    'darksalmon': '#e9967a',
    'darkseagreen': '#8fbc8f',
    'darkslateblue': '#483d8b',
    'darkslategray': '#2f4f4f',
    'darkturquoise': '#00ced1',
    'darkviolet': '#9400d3',

    'deeppink': '#ff1493',
    'deepskyblue': '#00bfff',
    'dimgray': '#696969',
    'dodgerblue': '#1e90ff',
    'firebrick': '#b22222',
    'floralwhite': '#fffaf0',
    'forestgreen': '#228b22',
    'fuchsia': '#ff00ff',
    'gainsboro': '#dcdcdc',

    'ghostwhite': '#f8f8ff',
    'gold': '#ffd700',
    'goldenrod': '#daa520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#adff2f',
    'honeydew': '#f0fff0',
    'hotpink': '#ff69b4',
    'indianred': '#cd5c5c',

    'indigo': '#4b0082',
    'ivory': '#fffff0',
    'khaki': '#f0e68c',
    'lavender': '#e6e6fa',
    'lavenderblush': '#fff0f5',
    'lawngreen': '#7cfc00',
    'lemonchiffon': '#fffacd',
    'lightblue': '#add8e6',
    'lightcoral': '#f08080',
    'lightcyan': '#e0ffff',

    'lightgoldenrodyellow': '#fafad2',
    'lightgray': '#d3d3d3',
    'lightgreen': '#90ee90',
    'lightpink': '#ffb6c1',
    'lightsalmon': '#ffa07a',
    'lightseagreen': '#20b2aa',
    'lightskyblue': '#87cefa',
    'lightslategray': '#778899',

    'lightsteelblue': '#b0c4de',
    'lightyellow': '#ffffe0',
    'lime': '#00ff00',
    'limegreen': '#32cd32',
    'linen': '#faf0e6',
    'maroon': '#800000',
    'mediumaquamarine': '#66cdaa',
    'mediumblue': '#0000cd',
    'mediumorchid': '#ba55d3',

    'mediumpurple': '#9370db',
    'mediumseagreen': '#3cb371',
    'mediumslateblue': '#7b68ee',
    'mediumspringgreen': '#00fa9a',
    'mediumturquoise': '#48d1cc',
    'mediumvioletred': '#c71585',
    'midnightblue': '#191970',
    'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1',
    'moccasin': '#ffe4b5',

    'navajowhite': '#ffdead',
    'navy': '#000080',
    'oldlace': '#fdf5e6',
    'olive': '#808000',
    'olivedrab': '#6b8e23',
    'orange': '#ffa500',
    'orangered': '#ff4500',
    'orchid': '#da70d6',
    'palegoldenrod': '#eee8aa',
    'palegreen': '#98fb98',

    'paleturquoise': '#afeeee',
    'palevioletred': '#db7093',
    'papayawhip': '#ffefd5',
    'peachpuff': '#ffdab9',
    'peru': '#cd853f',
    'pink': '#ffc0cb',
    'plum': '#dda0dd',
    'powderblue': '#b0e0e6',
    'purple': '#800080',
    'red': '#ff0000',

    'rosybrown': '#bc8f8f',
    'royalblue': '#4169e1',
    'saddlebrown': '#8b4513',
    'salmon': '#fa8072',
    'sandybrown': '#f4a460',
    'seagreen': '#2e8b57',
    'seashell': '#fff5ee',
    'sienna': '#a0522d',
    'silver': '#c0c0c0',
    'skyblue': '#87ceeb',

    'slateblue': '#6a5acd',
    'slategray': '#708090',
    'snow': '#fffafa',
    'springgreen': '#00ff7f',
    'steelblue': '#4682b4',
    'tan': '#d2b48c',
    'teal': '#008080',
    'thistle': '#d8bfd8',
    'tomato': '#ff6347',

    'turquoise': '#40e0d0',
    'violet': '#ee82ee',
    'wheat': '#f5deb3',
    'white': '#ffffff',
    'whitesmoke': '#f5f5f5',
    'yellow': '#ffff00',
    'yellowgreen': '#9acd32',


    # We favor the "gray" spelling. Eliminated these so as to not introduce
    # nondeterminism in the colors we pick (since these have the same RGB).

    # 'darkgrey': '#a9a9a9',
    # 'darkslategrey': '#2f4f4f',
    # 'dimgrey': '#696969',
    # 'grey': '#808080',
    # 'lightgrey': '#d3d3d3',
    # 'lightslategrey': '#778899',
    # 'slategrey': '#708090',


    # Not grays, but they still duplicate the RGBs:

    # 'cyan': '#00ffff',
    # 'magenta': '#ff00ff',
}


# Confirm no duplication in colors, which would make our choices
# nondeterministic.

_VISITED_RGB_PHRASES = {}
for name, css in CSS3_NAMES_TO_RGB_PHRASES.items():
    css = css.lower()

    try:
        previous_name = _VISITED_RGB_PHRASES[css]

    except KeyError:
        pass

    else:
        raise \
            Exception(
                "RGB [{}] is associated with both CSS names [{}] and "
                "[{}].".format(css, previous_name, name))


    _VISITED_RGB_PHRASES[css] = name


# Granular CSS colors grouped by major colors
_CSS3_COLOR_GROUPS = {
    ('red', '#ff0000'): [
        'brown',
        'crimson',
        'darkred',
        'deeppink',
        'firebrick',
        'hotpink',
        'indianred',
        'lavenderblush',
        'lightcoral',
        'lightpink',
        'maroon',
        'mistyrose',
        'palevioletred',
        'pink',
        'red',
    ],

    ('orange', '#ffa500'): [
        'bisque',
        'coral',
        'darkorange',
        'darksalmon',
        'lightsalmon',
        'orange',
        'orangered',
        'papayawhip',
        'peachpuff',
        'salmon',
        'tomato',
    ],

    ('yellow', '#ffff00'): [
        'beige',
        'cornsilk',
        'darkgoldenrod',
        'darkkhaki',
        'gold',
        'goldenrod',
        'khaki',
        'lemonchiffon',
        'lightgoldenrodyellow',
        'lightyellow',
        'palegoldenrod',
        'yellow',
    ],

    ('green', '#008000'): [
        'aquamarine',
        'chartreuse',
        'darkgreen',
        'darkolivegreen',
        'darkseagreen',
        'darkslategray',
# Commented above
        # 'darkslategrey',
        'forestgreen',
        'green',
        'greenyellow',
        'honeydew',
        'lawngreen',
        'lightgreen',
        'lightseagreen',
        'lime',
        'limegreen',
        'mediumaquamarine',
        'mediumseagreen',
        'mediumspringgreen',
        'olive',
        'olivedrab',
        'palegreen',
        'seagreen',
        'springgreen',
        'teal',
        'yellowgreen',
    ],

    ('blue', '#0000ff'): [
        'aliceblue',
        'aqua',
        'azure',
        'blue',
        'cadetblue',
        'cornflowerblue',

# Commented above
        # 'cyan',

        'darkblue',
        'darkcyan',
        'darkturquoise',
        'deepskyblue',
        'dodgerblue',
        'lightblue',
        'lightcyan',
        'lightskyblue',
        'lightsteelblue',
        'mediumblue',
        'mediumturquoise',
        'midnightblue',
        'navy',
        'paleturquoise',
        'powderblue',
        'royalblue',
        'skyblue',
        'steelblue',
        'turquoise',
    ],

    ('purple', '#800080'): [
        'blueviolet',
        'darkmagenta',
        'darkorchid',
        'darkslateblue',
        'darkviolet',
        'fuchsia',
        'indigo',
        'lavender',

# Commented above
        # 'magenta',

        'mediumorchid',
        'mediumpurple',
        'mediumslateblue',
        'mediumvioletred',
        'orchid',
        'plum',
        'purple',
        'slateblue',
        'thistle',
        'violet',
    ],

    ('brown', '#8b4513'): [
        'antiquewhite',
        'blanchedalmond',
        'burlywood',
        'chocolate',
        'linen',
        'moccasin',
        'navajowhite',
        'oldlace',
        'peru',
        'rosybrown',
        'saddlebrown',
        'sandybrown',
        'sienna',
        'tan',
        'wheat',
    ],

    (colorimetry.constant.COLOR_NAME_GRAY, colorimetry.constant.COLOR_CSS_GRAY): [
        'darkgray',
        'dimgray',
        'floralwhite',
        'gainsboro',
        'ghostwhite',
        'gray',
        'ivory',
        'lightgray',
        'lightslategray',
        'mintcream',
        'seashell',
        'silver',
        'slategray',
        'snow',
        'whitesmoke',

# # Commented above
#         'darkgrey',
#         'dimgrey',
#         'grey',
#         'lightgrey',
#         'lightslategrey',
#         'slategrey',
    ],

    (colorimetry.constant.COLOR_NAME_WHITE, colorimetry.constant.COLOR_CSS_WHITE): [
        'white',
    ],

    (colorimetry.constant.COLOR_NAME_BLACK, colorimetry.constant.COLOR_CSS_BLACK): [
        'black',
    ],
}


# Reindex the groups by child color name

MATCHED_COLOR_GROUP = \
    collections.namedtuple(
        'MATCHED_COLOR_GROUP', [
            'name',
            'css',
        ])

CSS3_GROUPS_BY_CSS_COLOR = {}
for (group_color_name, group_color_css), child_color_names \
        in _CSS3_COLOR_GROUPS.items():

    group = \
        MATCHED_COLOR_GROUP(
            name=group_color_name,
            css=group_color_css)

    for child_color_name in child_color_names:
        CSS3_GROUPS_BY_CSS_COLOR[child_color_name] = group
