from typing import Callable, Any
AggFunc = Callable[[list[dict[str, Any]]], dict[str, Any]]


def AggFuncSum(element_arr:list[dict[str, Any]])-> dict[str, Any]:
    sum_dict = {}
    for element in element_arr:
        for entry in element:
            if entry in sum_dict.keys():
                sum_dict[entry] += element[entry]
            else:
                sum_dict[entry] = element[entry]
    return sum_dict
