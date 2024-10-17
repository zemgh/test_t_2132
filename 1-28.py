""" Задача - Атрибуты класса """

from datetime import datetime, timezone


class CatMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now(tz=timezone.utc)
        return super().__new__(cls, name, bases, attrs)


class CatMetaTest(metaclass=CatMeta):
    pass


if __name__ == '__main__':
    cat = CatMetaTest()
    assert hasattr(cat, 'created_at')
