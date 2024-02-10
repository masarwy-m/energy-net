from energy_net import NetworkEntity
from energy_net.defs import State, Bid


class NetworkManager:
    def __init__(self, grid_agents:list[NetworkEntity]):
        self.grid_agents = grid_agents

    def collect_demand(self, state:State):
        total_consumption = 0
        for ga in self.grid_agents:
            total_consumption += ga.predict({'consume': {}}, state)['consume']

        return total_consumption

    def collect_production_bids(self, state:State, demand:float) -> dict[str, Bid]:
        bids = {}
        for ga in self.grid_agents:
            bid = ga.get_bid('production',state, demand)
            if bid:
                bids[ga.name] = bid

        return bids

    def dispatch(self, consumption_demand, bids):
        sorted_bidders = sorted(bids.keys(), key=lambda k: bids[k][1])

        workloads = {}
        last_bid = 0
        for bidder in sorted_bidders:
            workloads[bidder] = min(bids[bidder][0], consumption_demand)
            consumption_demand -= workloads[bidder]
            last_bid = bids[bidder][1]
            if consumption_demand == 0:
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
