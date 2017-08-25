from drivelink import Dict
import pytest
import os
#from Process import freeze_support


def test_dict():
    dct = Dict("testDict")
    for i in range(10):
        dct[i] = i
    for i in range(10):
        assert dct[i] == i


def test_init():
    with pytest.raises(ValueError) as excinfo:
        Dict("testInit", 0)
    excinfo.match(".* per page.*")
    with pytest.raises(ValueError) as excinfo:
        Dict("testInit", 1, 0)
    excinfo.match(".* in RAM.*")
    with Dict("testInit", 1, 1):
        pass
    Dict("testInit", 1, 1)


def test_guarantee_page():
    with Dict("testGuaranteePage", 1, 1) as d:
        d[0] = 1
        d[1] = "c"
        d[2] = 3.4
        assert d[0] == 1
        assert d[1] == "c"
        assert d[2] == 3.4


def test_save():
    d = Dict("testSave", 1, 1) as d:
    d[0] = 1
    d[1] = "c"
    d[2] = 3.4
    del d
    with Dict("testSave", 1, 1) as d:
        assert d[0] == 1
        assert d[1] == "c"
        assert d[2] == 3.4


if __name__ == '__main__':
    freeze_support()
    ut.main()
