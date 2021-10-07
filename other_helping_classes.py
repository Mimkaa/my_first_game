import weakref

class OneList(list):
    def __getitem__(self, index):
        if type(index) == int and index > 0:
            index -= 1
        if type(index) == slice:
            start, stop = index.start, index.stop
            if start and start > 0:
                start -= 1
            if stop and stop > 0:
                stop -= 1
            index = slice(start, stop, index.step)
        return super().__getitem__(index)

    def __setitem__(self, index, val):
        super().__setitem__(index - 1, val)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class Numberton(type):
    _number_of_them =[]
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if getattr(cls, "number")>0:
            if cls not in cls._instances:
                for i in range(getattr(cls, "number")):
                    cls._instances[cls] = super(Numberton,cls).__call__(*args, **kwargs)
                    cls._number_of_them.append(cls._instances[cls])

            return cls._number_of_them
    def clear(cls):
        try:

            for num, inst in enumerate(cls._number_of_them):
                del cls._number_of_them[num]
            del cls._instances[cls]






        except KeyError :
            pass
    def new_num(cls,num):
        setattr(cls,"number",num)





        # cls._number_of_them = [x for x in cls._number_of_them if x() is not None]  # filter out dead objects
        # if (len(cls._number_of_them) < getattr(cls,"number")):
        #     newproduct = super(Numberton,cls).__call__(*args, **kwargs)
        #     cls._number_of_them.append(weakref.ref(newproduct))
        #     return newproduct
        # else:
        #     return super(Numberton,cls).__call__(*args, **kwargs)


