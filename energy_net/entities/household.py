import random
from typing import Any, Union
import numpy as np

from ..config import INITIAL_TIME, NO_CONSUMPTION, MIN_POWER
from ..defs import Bounds
from ..model.action import EnergyAction, StorageAction, TradeAction
from ..model.state import State
from ..network_entity import NetworkEntity, CompositeNetworkEntity, ElementaryNetworkEntity
from ..entities.device import StorageDevice
from ..entities.local_storage import Battery
from ..entities.params import StorageParams, ProductionParams, ConsumptionParams
from ..entities.local_producer import PrivateProducer


class HouseholdState(State):
    storage:float
    production:float
    consumption:float



class Household(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """
    def __init__(self, name: str, consumption_params_dict:dict[str,ConsumptionParams]=None, storage_params_dict:dict[str,StorageParams]=None, production_params_dict:dict[str,ProductionParams]=None, agg_func=None):
        consumption_dict = {name: HouseholdConsumption(params) for name, params in consumption_params_dict.items()}
        storage_dict = {name: Battery(init_time=INITIAL_TIME, storage_params=params) for name, params in storage_params_dict.items()}
        production_dict = {name: PrivateProducer(params) for name, params in production_params_dict.items()}
        
        self.consumption_name_array = list(consumption_dict.keys())
        self.storage_name_array = list(storage_dict.keys())
        self.production_name_array = list(production_dict.keys())
        sub_entities = {**consumption_dict, **storage_dict, **production_dict}
    
        super().__init__(name=name, sub_entities=sub_entities, agg_func=agg_func)

        self.state = self.reset()

    def step(self, actions: dict[str, EnergyAction]):
        super().step(actions)

    def system_step(self):

        # get current consumption
        cur_comsumption = self.get_current_consumption()


        # get current production
        cur_production = self.get_current_production()


        # get current price
        [cur_price_sell, cur_price_buy] = self.get_current_market_price()

        # get storage/trade policy
        cur_storage = []
        for storage_name in self.storage_name_array:
            charge_range = self.get_action_space()[storage_name]
            charge_value = random.uniform(charge_range['low'],charge_range['high'])
            charge_action = StorageAction(charge=charge_value)
            # execute policy
            new_state=self.sub_entities[storage_name].step(charge_action)
            cur_storage.append(new_state['state_of_charge'])
            # update storage
        self.state['storage'] = sum(cur_storage)

        # buy/sell surplus
        trade_amount = cur_comsumption
        trade_power_action = TradeAction(amount=trade_amount)


    def get_current_market_price(self):
        # todo: remove
        return [8,8]

    def predict(self, actions: Union[np.ndarray, dict[str, Any]]):
        pass


    def get_current_consumption(self):
        return self.state['consumption']
    
    def get_current_production(self):
        return self.state['production']


    def get_current_state(self):
        return self.state

    def update_state(self, state: State):
        for entity in self.sub_entities:
            entity.update_state(state[entity.name])

    def get_observation_space(self):
        return dict(self.apply_func_to_sub_entities(lambda entity: entity.get_observation_space()))

    def get_action_space(self):
        conditions = lambda entity: isinstance(entity, StorageDevice)
        # print(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions), "Action Space")
        return dict(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions))

    def reset(self) -> HouseholdState:
        # return self.apply_func_to_sub_entities(lambda entity: entity.reset())
        return HouseholdState(consumption=100, production=200, storage=0)

    
    def validate_action(self, actions: dict[str, EnergyAction]):
        for entity_name, action in actions.items():
            if len(action) > 1 or 'charge' not in action.keys():
                raise ValueError(f"Invalid action key {action.keys()} for entity {entity_name}")
            else:
                return True
    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])

    def apply_func_to_sub_entities(self, func, condition=lambda x: True):
        results = {}
        for name, entity in self.sub_entities.items():
            if condition(entity):
                results[name] = func(entity)
        return results


class HouseholdConsumption(ElementaryNetworkEntity):
    def __init__(self, consumption_params:ConsumptionParams):
        super().__init__(name=consumption_params["name"],energy_dynamics=consumption_params["energy_dynamics"])

    def reset(self):
        return NO_CONSUMPTION

    def get_observation_space(self):
        low = NO_CONSUMPTION
        high = np.inf
        return Bounds(low=low, high=high, dtype=np.float32)

    def get_action_space(self):
        return Bounds(low=MIN_POWER, high=self.max_electric_power, dtype=np.float32)


class HouseholdIS(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """

    def __init__(self, name: str = None, sub_entities: list[NetworkEntity] = None):
        super().__init__(name, sub_entities)

    def step(self, actions: Union[np.ndarray, dict[str, Any]]):
        pass

    def get_current_state(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.get_current_state())

    def update_state(self, state: State):
        for entity in self.sub_entities:
            entity.update_state(state[entity.name])

    def get_observation_space(self):
        return dict(self.apply_func_to_sub_entities(lambda entity: entity.get_observation_space()))

    def get_action_space(self):
        conditions = lambda entity: isinstance(entity, StorageDevice)
        # print(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions), "Action Space")
        return dict(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions))

    def reset(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.reset())

    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])

    def apply_func_to_sub_entities(self, func, condition=lambda x: True):
        results = {}
        for name, entity in self.sub_entities.items():
            if condition(entity):
                results[name] = func(entity)
        return results



