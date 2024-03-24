from typing import Callable, Any

from defs import State

AggFunc = Callable[[list[dict[str, Any]]], dict[str, Any]]


def agg_func_sum(element_arr:list[dict[str, Any]])-> dict[str, Any]:
    sum_dict = {}
    for element in element_arr:
        for entry in element:
            if entry in sum_dict.keys():
                sum_dict[entry] += element[entry]
            else:
                sum_dict[entry] = element[entry]
    return sum_dict


def condition(state:State):
    pass


def get_predicted_state(cur_state:State, horizon:float)->State:
    state = State({'time':cur_state['time']+horizon})
    return state

