def binary_search(vals, condition, **kwargs):
    """this template has two options:
    one where mid satisfying the condition means we
    search to the left, and one where mid satisfying
    the condition means we search to the left.
    I have the former commented in and the latter
    commented out
    """
    left, right = 0, len(vals)
    while left < right:
        mid = left + (right - left) // 2
        # mid = left + (right - left) // 2 + 1
        if condition(mid, **kwargs):
            right = mid
            # left = mid
        else:
            left = mid + 1
            # right = mid - 1
    return left


def condition(**kwargs):
    """this is where the bulk of the logic resides
    """
    pass
