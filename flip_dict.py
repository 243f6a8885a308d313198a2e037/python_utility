from collections import defaultdict


def flip_dict(d):
    out = defaultdict(list)
    for k, v in d.items():
        out[v].append(k)
    return out


class MutableKeyDict:
    def __init__(self):
        self.keys = []
        self.values = []
        pass

    def __str__(self):
        return "{" + ", ".join(["{}: {}".format(key, value) for key, value in zip(self.keys, self.values)]) + "}"

    def __contains__(self, key):
        return key in self.keys

    def __getitem__(self, key):
        index = self.keys.index(key)
        return self.values[index]

    def __setitem__(self, key, value):
        if key in self.keys:
            self.values[self.keys.index(key)] = value
        else:
            self.keys.append(key)
            self.values.append(value)

    def __iter__(self):
        self.cache_index = -1
        return self

    def __next__(self):
        self.cache_index += 1
        if len(self.keys) == self.cache_index:
            raise StopIteration
        return self.keys[self.cache_index - 1]


def flip_dict_with_mutable_value(d):
    md = MutableKeyDict()
    for v, k in d.items():
        if k in md:
            md[k].append(v)
        else:
            md[k] = [v]
    return md
