from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return ""
        self._data.move_to_end(key)
        return self._data[key]

    def set(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value

        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def rem(self, key):
        self._data.pop(key, None)
