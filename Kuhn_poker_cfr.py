import random

Pass, Bet = 0, 1
num_actions = 2

rng = random.Random()
node_map = {} # maps infoset strings to node objects

class Node:
    def __init__(self, info_set):
        self.info_set = info_set
        self.regret_sum = [0] * num_actions
        self.strategy = [0] * num_actions
        self.strategy_sum = [0] * num_actions
    
    def get_strategy(self, realization_weight):
        # 1) regret-matching
        normalizing_sum = 0
        for a in range(num_actions):
            self.strategy[a] = self.regret_sum[a] if self.regret_sum[a] > 0 else 0
            normalizing_sum += self.strategy[a]
        
        if normalizing_sum > 0:
            for a in range(num_actions):
                self.strategy[a] /= normalizing_sum
        else:
            for a in range(num_actions):
                self.strategy[a] = 1 / num_actions # uniform fallback strategy
        
        # 2) accumulate average strategy with reach probability weight pi_i
        for a in range(num_actions):
            self.strategy_sum[a] += realization_weight * self.strategy[a]
        
        return self.strategy
    
    def get_average_strategy(self):
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            res = []
            for strat in self.strategy_sum:
                res.append(strat/normalizing_sum)
            return res
        else:
            return [1/num_actions]*num_actions
        
    def __str__(self):
        avg = self.get_average_strategy()
        avg_txt = "[" + ", ".join(f"{p:.4g}" for p in avg) + "]"
        return f"{self.info_set:>4}: {avg_txt}"

def get_node(info_set):
    node = node_map.get(info_set) # returns the value of the key (info_set) if it exists in the hash map, if it doesn't exist it returns None
    if node is None:
        node = Node(info_set) # store the key inside the node
        node_map[info_set] = node # register it so we reuse this object next time
    return node

def cfr(cards, history, p0, p1):
    """
    cards: list of 3 ints (shuffled once per iteration) - cards[0] = p0, cards[1] = p1
    history: string of 'p'/'b' so far
    p0, p1: reach probabilities of the players actions to arrive at this history (chancenode/deal has
    already been sampled in shuffling and therefore is not included here)
    returns: expected utility from the current player
    """
    plays = len(history)
    player = plays % 2 # 0 if P0 to act and 1 if P1 to act
    opponent = 1 - player

    # return payoff for terminal states
    if plays > 1:
        terminal_pass = history[-1] == 'p' # last action was a pass
        double_bet = history[-2:] == 'bb' # last 2 actions were both bets
        is_player_higher = cards[player] > cards[opponent] 

        if terminal_pass:
            if history == 'pp':
                # both players checked: so the winner gets +1 and loser gets -1
                return 1 if is_player_higher else -1
            else:
                # someone folded to a bet (e.g., "bp" or "pbp"):
                # bettor wins +1 from the current players perspective
                return 1
        elif double_bet:
            # bet + call: showdown with pot = 4 -> winner +2 and loser -2
            return 2 if is_player_higher else -2

    # get infoset node or create it if it doesnt exist
    info_set = f"{cards[player]}{history}"
    node = get_node(info_set)

    # for each action, recursively call cfr with additional history and probability
    realization_weight = p0 if player == 0 else p1
    strategy = node.get_strategy(realization_weight)

    util = [0] * num_actions
    node_util = 0

    for a in (Pass, Bet):
        next_history = history + ('p' if a == Pass else 'b')

        # Update reach probabilities for the acting player
        next_p0, next_p1 = (p0 * strategy[a], p1) if player == 0 else (p0, p1 * strategy[a])

        # child returns next player's value, so you need to negate to get current players value
        util[a] = -cfr(cards, next_history, next_p0, next_p1)
        
        # Expected value at this infoset under current strategy
        node_util += strategy[a] * util[a]
    
    # for each action, compute and accumulate counterfactual regret

    opp_reach = p1 if player == 0 else p0 # opponent reach probabilty at this history

    # accumulate cumulative counterfactual regrets
    for a in (Pass, Bet):
        regret = util[a] - node_util
        node.regret_sum[a] += opp_reach * regret

    return node_util

def train(iterations):
    cards = [1, 2, 3]
    utility = 0
    
    for a in range(iterations):
        rng.shuffle(cards)
        utility += cfr(cards, "", 1, 1)

    print(f"Number of iterations: {iterations}")
    print("Average game value:", utility/iterations)
    for n in node_map.values():
        print(n)

train(1000000)