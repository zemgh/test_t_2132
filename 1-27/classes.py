""" Задача - Синглтон """


class CatMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class CatMetaTest(metaclass=CatMeta):
    pass


class SingletonCat:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, name):
        if not self._initialized:
            self.name = name
            self._initialized = True


singleton_cat = SingletonCat('singleton cat')
