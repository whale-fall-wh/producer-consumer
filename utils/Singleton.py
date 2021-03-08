def singleton(cls):
    """
    单例修饰器
    :param cls:
    :return:
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
