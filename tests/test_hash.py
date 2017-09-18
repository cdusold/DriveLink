from drivelink.hash import hash
from drivelink.hash import frozen_hash
from pytest import raises
from sys import version_info

test_items = {0:0,
              12:12,
              int(1e16):1e16,
              "a":91634880152443617534842621287039938041581081254914058002978601050179556493499,
              "123":75263518707598184987916378021939673586055614731957507592904438851787542395619,
              (0,1,2):33822245971830441941584207765618803954591506626161146963614155313748171978276,
              frozenset([0,1,2]):72252079842091549505691736167086842307551715296043210784274131111424579773361}
#Turns out, due to long.__repr__, it is impossible to simply use the same hash between 2 and 3.
if version_info[0] == 3:
    test_items_hash = 100629669830209025598188697529866622321230535989662311885517553315311996762890
else:
    test_items_hash = 101320894591067286039721536210337767081651837586820788720628983031603277260963

def test_hash():
    for item, soln in test_items.items():
        print(hash(item))
        assert hash(item) == soln
    with raises(TypeError):
        assert hash(test_items) == test_items_hash

def test_frozen_hash():
    for item in test_items.keys():
        assert frozen_hash(item) == hash(item)
    print(frozen_hash(test_items))
    assert frozen_hash(test_items) == test_items_hash
