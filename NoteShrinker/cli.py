#!/usr/bin/env python3
"""Commandline interface for NoteShrink"""

import os
import re
from argparse import ArgumentParser

from . import NoteShrinker

# TODO: dpi
# TODO: logging/debug/print

def main():

    options = get_argument_parser().parse_args()

    unshrunk = get_filenames(options)

    ns = NoteShrinker(unshrunk, options.global_palette, options.sample_fraction,
                    options.num_colors, options.saturate, options.white_bg,
                    options.value_threshold, options.sat_threshold,
                    options.downsample_ratio)

    shrunk = ns.shrink()

    for i, shrunk_image in enumerate(shrunk):
        output_filename = '{}{:04d}.png'.format(options.basename, i)
        shrunk_image.save(output_filename)


def percent(string):
    '''Convert a string (i.e. 85) to a fraction (i.e. .85).'''
    return float(string)/100.0


def get_filenames(options):

    '''Get the filenames from the command line, optionally sorted by
    number, so that IMG_10.png is re-arranged to come after IMG_9.png.
    This is a nice feature because some scanner programs (like Image
    Capture on Mac OS X) automatically number files without leading zeros,
    and this way you can supply files using a wildcard and still have the
    pages ordered correctly.'''

    if not options.sort_numerically:
        return options.filenames

    filenames = []

    for filename in options.filenames:
        basename = os.path.basename(filename)
        root, _ = os.path.splitext(basename)
        matches = re.findall(r'[0-9]+', root)
        if matches:
            num = int(matches[-1])
        else:
            num = -1
        filenames.append((num, filename))

    return [fn for (_, fn) in sorted(filenames)]



def get_argument_parser():

    '''Parse the command-line arguments for this program.'''

    parser = ArgumentParser(description='convert scanned, hand-written notes to PDF')

    show_default = ' (default %(default)s)'

    parser.add_argument('filenames', metavar='IMAGE', nargs='+',
                        help='files to convert')

    parser.add_argument('-b', dest='basename', metavar='BASENAME',
                        default='page',
                        help='output PNG filename base' + show_default)

    parser.add_argument('-v', dest='value_threshold', metavar='PERCENT',
                        type=percent, default='15',
                        help='background value threshold %%'+show_default)

    parser.add_argument('-s', dest='sat_threshold', metavar='PERCENT',
                        type=percent, default='20',
                        help='background saturation '
                        'threshold %%'+show_default)

    parser.add_argument('-n', dest='num_colors', type=int,
                        default='8',
                        help='number of output colors '+show_default)

    parser.add_argument('-p', dest='sample_fraction',
                        metavar='PERCENT',
                        type=percent, default='5',
                        help='%% of pixels to sample' + show_default)

    parser.add_argument('-w', dest='white_bg', action='store_true',
                         default=True, help='make background white')

    parser.add_argument('-g', dest='global_palette',
                        action='store_true', default=False,
                        help='use one global palette for all pages')

    parser.add_argument('-S', dest='saturate', action='store_false',
                        default=True, help='do not saturate colors')

    parser.add_argument('-K', dest='sort_numerically',
                        action='store_false', default=True,
                        help='keep filenames ordered as specified; '
                        'use if you *really* want IMG_10.png to '
                        'precede IMG_2.png')

    parser.add_argument('-d', dest='downsample_ratio',
                        metavar='PERCENT',
                        type=percent, default='50',
                        help='%% to resize the image before applying NoteShrink' + show_default)

    return parser
