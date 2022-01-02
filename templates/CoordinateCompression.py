# see this article on what coordinate compression is and why it's useful:
# https://medium.com/algorithms-digest/coordinate-compression-2fff95326fb


def coordinate_compression_1d(nums):
    distinct = set(nums)
    mapping = {x: i for i, x in enumerate(sorted(distinct))}
    out = [mapping[n] for n in nums]
    return mapping, out


def coordinate_compression_2d(pairs):
    xs, ys = zip(*pairs)
    mapping_x, mapped_x = coordinate_compression_1d(xs)
    mapping_y, mapped_y = coordinate_compression_1d(ys)
    mapped_pairs = zip(mapped_x, mapped_y)
    return mapping_x, mapping_y, mapped_pairs
