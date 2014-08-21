"""
.. moduleauthor:: Chris Dusold <PySpeedup@chrisdusold.com>

A module containing algorithm parallelization classes and methods.

The motivation for this module was to simplify the often overly convoluted
structure of the Python :mod:`multiprocessing` for common and simple uses
of parallelization.

"""
from _buffer import buffer,Buffer
from _cache import Cache
