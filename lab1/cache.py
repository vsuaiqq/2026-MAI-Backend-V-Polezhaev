class LRUCache:
    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data: dict[str, str] = {}

    def get(self, key: str):
        value = self._data.pop(key, None)
        if value is None:
            return ""
        self._data[key] = value
        return value

    def set(self, key: str, value: str):
        if key in self._data:
            self._data.pop(key, None)
        self._data[key] = value

        if len(self._data) > self.capacity:
            lru_key = next(iter(self._data))
            self._data.pop(lru_key, None)

    def rem(self, key: str):
        self._data.pop(key, None)
