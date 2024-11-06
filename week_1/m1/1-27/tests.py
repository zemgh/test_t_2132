""" Задача - Синглтон """

from classes import CatMetaTest


if __name__ == '__main__':
    from classes import singleton_cat
    id_1 = id(singleton_cat)

    from classes import singleton_cat
    id_2 = id(singleton_cat)
    assert id_1 == id_2


    meta_cat_1 = CatMetaTest()
    meta_cat_2 = CatMetaTest()
    assert id(meta_cat_1) == id(meta_cat_2)
