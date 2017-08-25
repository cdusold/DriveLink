from drivelink import List
import pytest
import os
#from Process import freeze_support


def test_list():
    lst = List("testList")
    for i in range(10):
        lst.append(i)
    for i in range(10):
        assert lst[i] == i


def test_init():
    with pytest.raises(ValueError) as excinfo:
        List("testListInit", 0)
    excinfo.match(".* per page.*")
    with pytest.raises(ValueError) as excinfo:
        List("testListInit", 1, 0)
    excinfo.match(".* in RAM.*")
    with List("testListInit", 1, 1):
        pass
    List("testListInit", 1, 1)


def test_guarantee_page():
    with List("testGuaranteePage", 1, 1) as l:
        l.append(1)
        l.append("c")
        l.append(3.4)
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4


def test_save():
    l = List("testGuaranteePage", 1, 1)
    l.append(1)
    l.append("c")
    l.append(3.4)
    del l
    with List("testGuaranteePage", 1, 1) as l:
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4


if __name__ == '__main__':
    freeze_support()
    ut.main()
