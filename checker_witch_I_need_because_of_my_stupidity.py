class Singleton(type):
    _instances = {}

    # Each of the following functions use cls instead of self
    # to emphasize that although they are instance methods of
    # Singleton, they are also *class* methods of a class defined
    # with Singleton
    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]

    def clear(cls):
        try:
            del Singleton._instances[cls]
        except KeyError:
            print(1)


class MySing(metaclass=Singleton):
    pass


s1 = MySing()  # First call: actually creates a new instance
s2 = MySing()  # Second call: returns the cached instance
assert s1 is s2  # Yup, they are the same
MySing.clear()  # Throw away the cached instance
s3 = MySing()  # Third call: no cached instance, so create one
assert s1 is not s3  # Yup, s3 is a distinct new instance