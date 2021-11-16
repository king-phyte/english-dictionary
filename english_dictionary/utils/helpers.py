from typing import Iterable, Sequence, Union


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


def convert_to_list(iterable: Iterable[str], start=1):
    """
    Returns numbered strings starting from :start
    Example:
        iterable: ("hello", "world", "!")
        start: 1

        Returns:
            1. hello
            2. world
            3. !
    """

    return "\n".join(
        map(
            lambda x: f"\t{x[0]}. {x[1]}",
            enumerate(iterable, start=start),
        )
    )
