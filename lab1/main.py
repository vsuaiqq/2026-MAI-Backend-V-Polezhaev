from cache import LRUCache


def main():
    cache = LRUCache(100)
    cache.set("Jesse", "Pinkman")
    cache.set("Walter", "White")
    cache.set("Jesse", "James")
    assert cache.get("Jesse") == "James"
    cache.rem("Walter")
    assert cache.get("Walter") == ""
    print('ok')


if __name__ == "__main__":
    main()
