from typing import Sequence, Union


def binary_search(array: Sequence[Union[str, int]], target: Union[str, int]):
    if len(array) < 1:
        return -1

    lower_bound = 0
    upper_bound = len(array) - 1

    while lower_bound <= upper_bound:
        mid_point = (lower_bound + upper_bound) // 2

        if array[mid_point] == target:
            return mid_point

        elif array[mid_point] > target:
            upper_bound = mid_point - 1

        elif array[mid_point] < target:
            lower_bound = mid_point + 1

    return -1
