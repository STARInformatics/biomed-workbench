# Good test file: R-HSA-8936459.sbgn

import os
import click
from libsbgnpy import utils

INPUT_DIR = 'backend/data/sbgn/'

def isContainedIn(a, b) -> bool:
    """
    Returns: a is contained in b
    """
    c1 = a.x > b.x
    c2 = a.y > b.y
    c3 = (a.x + a.w) < (b.x + b.w)
    c4 = (a.y + a.h) < (b.y + b.h)
    return c1 and c2 and c3 and c4

if __name__ == '__main__':
    records = set()
    files = os.listdir(INPUT_DIR)
    print('Processing {} many files'.format(len(files)))
    with click.progressbar(files, label='building label list') as bar:
        for filename in bar:
            path = INPUT_DIR + filename
            sbgn = utils.read_from_file(path)

            m = sbgn.get_map()
            glyphs = m.get_glyph()

            glyphs = sorted(glyphs, key=lambda g: g.bbox.w * g.bbox.h)

            for a in glyphs:
                for b in glyphs:
                    if isContainedIn(a.bbox, b.bbox):
                        a.compartmentRef = b.id
                        break

            sbgn.write_file(INPUT_DIR + filename)
