from typing import Callable, Any
AggFunc = Callable[[list[dict[str, Any]]], dict[str, Any]]


def AggFuncSum(element_arr:list[dict[str, Any]])-> dict[str, Any]:
    pass