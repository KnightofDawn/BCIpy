import numpy as np

KEYBOARD = np.array([['A', 'B', 'C', 'D', 'E', 'F'],
                     ['G', 'H', 'I', 'J', 'K', 'L'],
                     ['M', 'N', 'O', 'P', 'Q', 'R'],
                     ['S', 'T', 'U', 'V', 'W', 'X'],
                     ['Y', 'Z', '0', '1', '2', '3'],
                     ['4', '5', '6', '7', '8', '9']])


def is_target(char, sti_order):
    # here if sti_order < 6 row else col sti_order: 0-11
    row, col = np.nonzero(KEYBOARD == char)
    return sti_order == row if sti_order < 6 else sti_order == col
