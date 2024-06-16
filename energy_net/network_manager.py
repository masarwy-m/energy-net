import numpy as np
import scipy.optimize as opt

from .market_entity import MarketEntity
from .model.state import State
from .defs import Bid
from .utils.utils import condition, get_predicted_state
from .market_entity import MarketProducer, MarketConsumer


def optimal_dispatch(consumption_demand, bids):
    costs = np.array([bids[bidder][1] for bidder in sorted(bids)])
    capacities = np.array([bids[bidder][0] for bidder in sorted(bids)])
    cons = [{'type': 'eq', 'fun': lambda x: sum(x) - consumption_demand},
            {'type': 'ineq', 'fun': lambda x: capacities - x}]  # Ensure production does not exceed capacities

    res = opt.minimize(lambda x: sum(x * costs), capacities, constraints=cons)
    if res.success:
        return dict(zip(sorted(bids), res.x)), costs[np.argmin(res.x)]  # Assuming last price as MCP
    else:
        raise ValueError("Optimization failed")


class NetworkManager:
    def __init__(self, market_entities: list[MarketEntity]):
        self.market_entities = market_entities
        self.history = []  # Track past market outcomes

    def update_bidding_strategies(self):
        # Placeholder for a learning algorithm that updates entities' strategies
        # based on historical outcomes
        pass

    def do_market_clearing(self, state: State):
        demand = self.collect_demand(state)
        bids = self.collect_production_bids(state, demand)
        workloads, price = self.market_clearing_merit_order(demand, bids)
        return [demand, bids, workloads, price]

    def collect_demand(self, state: State) -> float:
        total_demand = 0
        for ma in self.market_entities:
            if isinstance(ma, MarketConsumer):
                total_demand += ma.get_total_demand()
        return total_demand

    def collect_production_bids(self, state: State, demand: float) -> dict[str, Bid]:
        bids = {}
        for ma in self.market_entities:
            if isinstance(ma, MarketProducer):
                bid = ma.get_bid('production', state, demand)
                if bid:
                    bids[ma.name] = (bid.quantity, bid.price)
        return bids

    def dispatch(self, consumption_demand, bids) -> tuple[dict[MarketEntity, float], float]:
        sorted_bidders = sorted(bids.keys(), key=lambda k: bids[k][1])
        workloads = {}
        last_bid = 0
        for bidder in sorted_bidders:
            available_capacity = min(bids[bidder][0], consumption_demand)
            workloads[bidder] = available_capacity
            consumption_demand -= available_capacity
            last_bid = bids[bidder][1]
            if consumption_demand <= 0:
                break

        return workloads, last_bid

    def set_price(self, workloads, last_bid):
        return last_bid

    def market_clearing(self, method: str, consumption_demand, bids):
        if method == 'merit_order':
            return self.market_clearing_merit_order(consumption_demand, bids)
        else:
            raise NotImplementedError

    def market_clearing_merit_order(self, consumption_demand, bids):
        workloads, last_bid = self.dispatch(consumption_demand, bids)
        price = self.set_price(workloads, last_bid)
        return workloads, price

    def run(self, initial_state: State, stop_criteria: condition, horizons: list[float] = [24, 48]):
        cur_state = initial_state
        while not stop_criteria(cur_state):
            for horizon in horizons:
                predicted_state = get_predicted_state(cur_state, horizon)
                [demand, bids, workloads, price] = self.do_market_clearing(predicted_state)
                self.history.append((demand, bids, workloads, price))
                self.update_bidding_strategies()  # Update strategies based on market outcomes
                # send solution
