""" Задача - Декоратор управления доступом """


class User:
    def __init__(self, name: str, roles: list):
        self.name = name
        self.roles = roles


def get_user():
    global USER
    return USER


def check_access(user: User, roles: list) -> set:
    return set(roles) & set(user.roles)


def access_control(roles=None):
    if not roles:
        roles = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_user()

            if user:
                if not roles or check_access(user, roles):
                    return func(*args, **kwargs)

            raise PermissionError('Access denied')

        return wrapper
    return decorator


@access_control(['role_1', 'role_2'])
def hello_world_1():
    return 'allowed'


@access_control(['role_3', 'role_4'])
def hello_world_2():
    return 'allowed'


if __name__ == '__main__':

    USER = User('username', ['role_1'])
    assert hello_world_1() == 'allowed'
    try:
        hello_world_2()
        assert False
    except PermissionError as e:
        assert str(e) == 'Access denied'
    except Exception:
        assert False



    USER = None
    try:
        hello_world_1()
        assert False
    except PermissionError as e:
        assert str(e) == 'Access denied'
    except Exception:
        assert False


