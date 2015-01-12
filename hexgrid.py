"""A class to display a static hexgrid
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

class HexGrid(object):
    CENTER_ROW = 12
    CENTER_COL = 35
    STATIC_GRID = '''\
 __    __    __    __    __    __    __    __    __    __    __    __ 
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \\
\__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/
    '''

    def __init__(self, reduced=False):
        import textwrap
        self.grid = textwrap.wrap(self.STATIC_GRID, 70)
        self._show_reduced = reduced
        self.bounds = {
            'left': 0,
            'top': 0,
            'right': 0,
            'bottom': 0
        }
        
    def __str__(self):
        if self._show_reduced:
            return self.reduced
        else:
            return '\n'.join(i for i in self.grid)

    def annotate(self, coords, note):
        self.bounds['left'] = min([coords[0], self.bounds['left']])
        self.bounds['right'] = max([coords[0], self.bounds['right']])
        
        self.bounds['top'] = min([coords[1], self.bounds['top']])
        self.bounds['bottom'] = max([coords[1], self.bounds['bottom']])
        
        list_row = self.CENTER_ROW + (coords[1] * 2) + (coords[0])
        col_row = self.CENTER_COL + (coords[0] * 3)
        self.grid[list_row] = self.grid[list_row][0:col_row-1] \
                                     + note \
                                     + self.grid[list_row][col_row + 1:]
        
if __name__ == '__main__':
    example = HexGrid()
    example.annotate( (-4,0), 'wB' )
    example.annotate( (-3,0), 'wB' )
    example.annotate( (-2,0), 'wS' )
    example.annotate( (-1,0), 'wS' )
    example.annotate( (0,0), 'wQ' )
    example.annotate( (1,0), 'wA' )
    example.annotate( (2,0), 'wA' )
    
    example.annotate( (-2,1), 'bB' )
    example.annotate( (-1,1), 'bB' )
    example.annotate( (0,1), 'bS' )
    example.annotate( (1,1), 'bS' )
    example.annotate( (2,1), 'bQ' )
    example.annotate( (3,1), 'bA' )
    example.annotate( (4,1), 'bA' )
    
    print(example)