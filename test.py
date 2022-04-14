


class X:
    _data: int = 1

    def set_data(self, other):
        print(other)
    
    def get_data(self):
        return self._data

    data= property(get_data, set_data)



b = X()


b.data += 1
