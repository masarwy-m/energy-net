class NetworkManager:
    def __init__(self, producers, consumers):
        self.producers = producers
        self.consumers = consumers

    def collect_demand(self, state):
        total_consumption = 0
        for consumer in self.consumers:
            total_consumption += consumer.predict({'consume': {}}, state)['consume']

        return total_consumption

    def collect_bids(self, state, consumption_demand):
        bids = {}
        for producer in self.producers:
            bids[producer.name] = producer.production_bid(state, consumption_demand)

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

    def market_clearing(self, consumption_demand, bids):
        workloads, last_bid = self.dispatch(consumption_demand, bids)
        price = self.set_price(workloads, last_bid)
        return workloads, price