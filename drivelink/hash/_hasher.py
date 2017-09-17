"""
I pulled out `this solution from Stack Overflow <https://stackoverflow.com/a/21614155>`_
a way to guarantee hashability.

In order to make it backwards compatible, I made it so the hash of an Integral is itself.
"""

from hashlib import sha256
from base64 import b64encode
from collections import Hashable, Set, Mapping, Iterable
from numbers import Integral

class Deterministic_Hashable():
    def __fixed_hash__(self):
        return NotImplemented

def hash(o):
    if isinstance(o, Integral):
        return int(o)
    if isinstance(o, Deterministic_Hashable):
        return o.__fixed_hash__()
    if not isinstance(o, Hashable):
        raise TypeError("unhashable type: '"+ type({}).__name__+"'")
    try:
        return int(sha256(o).hexdigest(), base=16)
    except TypeError:
        pass
    if isinstance(o, Set):
        return int(sha256(repr((type(o).__name__,) + tuple(sorted(frozen_hash(e) for e in o)))).hexdigest(), base=16)
    if isinstance(o, Mapping):
        return int(sha256(repr((type(o).__name__,) + tuple(sorted((frozen_hash(k),frozen_hash(v)) for k,v in o.items())))).hexdigest(), base=16)
    if isinstance(o, Iterable):
        return int(sha256(repr((type(o).__name__,) + tuple(frozen_hash(e) for e in o))).hexdigest(), base=16)
    # This likely won't work.
    return int(sha256(repr(tuple((type(o).__name__, str(o))))).hexdigest(), base=16)

def frozen_hash(o):
    """
    This can hash the unhashable!
    """
    if isinstance(o, Integral):
        return int(o)
    if isinstance(o, Deterministic_Hashable):
        return o.__fixed_hash__()
    try:
        return int(sha256(o).hexdigest(), base=16)
    except TypeError:
        pass
    if isinstance(o, Set):
        return int(sha256(repr((type(o).__name__,) + tuple(sorted(frozen_hash(e) for e in o)))).hexdigest(), base=16)
    if isinstance(o, Mapping):
        return int(sha256(repr((type(o).__name__,) + tuple(sorted((frozen_hash(k),frozen_hash(v)) for k,v in o.items())))).hexdigest(), base=16)
    if isinstance(o, Iterable):
        return int(sha256(repr((type(o).__name__,) + tuple(frozen_hash(e) for e in o))).hexdigest(), base=16)
    # This likely won't work.
    return int(sha256(repr(tuple((type(o).__name__, str(o))))).hexdigest(), base=16)
