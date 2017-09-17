from drivelink.hash import hash
from drivelink.hash import frozen_hash
import pytest

test_items = {0:0,
              12:12,
              int(1e16):1e16,
              "a":91634880152443617534842621287039938041581081254914058002978601050179556493499L,
              "123":75263518707598184987916378021939673586055614731957507592904438851787542395619L,
              (0,1,2):33822245971830441941584207765618803954591506626161146963614155313748171978276L,
              frozenset([1,2,3]):25882003764048987718141392734117082888638242004662515896959010033876831084321L}
test_items_hash = 24201422530674263649081231419844906437853135089414056955828843044645193994003L

def test_hash():
    for item, soln in test_items.items():
        assert hash(item)==soln
    with pytest.raises(TypeError):
        assert hash(test_items)== test_items_hash

def test_frozen_hash():
    for item in test_items.keys():
        assert frozen_hash(item)==hash(item)
    assert frozen_hash(test_items)== test_items_hash
