import random
from typing import List, Tuple, Set

Position = Tuple[int, int]


class Environment:
    """Simple grid environment where some cells are dirty."""
    def __init__(self, width: int, height: int, dirt: Set[Position], agent_pos: Position):
        self.width = width
        self.height = height
        self.dirt = set(dirt)
        self.agent_pos = agent_pos
        self.steps = 0

    def is_dirty(self, pos: Position) -> bool:
        return pos in self.dirt

    def clean(self, pos: Position):
        self.dirt.discard(pos)

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def move_agent(self, pos: Position):
        if self.in_bounds(pos):
            self.agent_pos = pos
        self.steps += 1

    def get_neighbors(self, pos: Position) -> List[Position]:
        x, y = pos
        candidates = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [p for p in candidates if self.in_bounds(p)]

    def manhattan_distance(self, a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def nearest_dirt_distance(self, pos: Position) -> int:
        if not self.dirt:
            return None
        return min(self.manhattan_distance(pos, d) for d in self.dirt)

    def display(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                p = (x, y)
                if p == self.agent_pos:
                    row.append("A")
                elif p in self.dirt:
                    row.append("*")
                else:
                    row.append(".")
            grid.append(" ".join(row))
        print("\n".join(grid))
        print(f"Steps: {self.steps}  Dirt remaining: {len(self.dirt)}\n")


class UtilityAgent:
    """
    Utility-based agent:
      - reward_clean: reward for cleaning a dirty tile
      - move_cost: cost per move (positive number)
      - time_penalty: small penalty per timestep (positive number)
      - clean_cost: cost for performing the clean action
    The agent computes a simple optimistic utility for each action and picks the best.
    """
    def __init__(self, reward_clean=10.0, move_cost=1.0, time_penalty=0.1, clean_cost=0.2):
        self.reward_clean = reward_clean
        self.move_cost = move_cost
        self.time_penalty = time_penalty
        self.clean_cost = clean_cost

    def decide_action(self, env: Environment):
        x, y = env.agent_pos

        # If current tile is dirty, cleaning usually best
        if env.is_dirty(env.agent_pos):
            return ("suck", env.agent_pos)

        # Consider moves (including 'stay') and estimate utility if we take that action
        moves = env.get_neighbors(env.agent_pos)
        best_move = None
        best_utility = -float('inf')

        for new_pos in moves:
            # immediate cost for taking action to move to 'new_pos'
            # If staying in place, still pay a small time penalty (no movement cost)
            if new_pos == env.agent_pos:
                immediate_cost = self.time_penalty
            else:
                immediate_cost = self.move_cost + self.time_penalty

            # optimistic estimate of future: the agent will go to the nearest dirt from new_pos
            nearest_dist = env.nearest_dirt_distance(new_pos)
            if nearest_dist is None:
                # no dirt left => utility is negative (we pay cost/waste time)
                optimistic_future = 0.0
            else:
                # cost to reach the nearest dirt from new_pos:
                travel_cost = nearest_dist * (self.move_cost + self.time_penalty)
                optimistic_future = self.reward_clean - travel_cost

            utility = optimistic_future - immediate_cost

            # tie-breaker: prefer moves that actually change position (toward exploration)
            if utility > best_utility or (utility == best_utility and new_pos != env.agent_pos):
                best_utility = utility
                best_move = new_pos

        # If best utility is negative and there's no value in moving, choose to stay (no-op)
        if best_move is None:
            return ("stay", env.agent_pos)
        else:
            if best_move == env.agent_pos:
                return ("stay", best_move)
            else:
                # Return direction as move
                return ("move", best_move)


def run_simulation(env: Environment, agent: UtilityAgent, max_steps=200, verbose=True):
    history = []
    for step in range(max_steps):
        if verbose:
            print(f"=== Step {step} ===")
            env.display()

        if not env.dirt:
            if verbose:
                print("All clean! Done.")
            break

        action, target = agent.decide_action(env)

        if action == "suck":
            if env.is_dirty(env.agent_pos):
                env.clean(env.agent_pos)
                env.steps += 1
                history.append(("suck", env.agent_pos))
                if verbose:
                    print(f"Agent cleans at {env.agent_pos}")
            else:
                # nothing to clean, waste time
                env.steps += 1
                history.append(("nothing", env.agent_pos))
                if verbose:
                    print("Agent tried to clean but tile was already clean.")
        elif action == "move":
            env.move_agent(target)
            history.append(("move", target))
            if verbose:
                print(f"Agent moves to {target}")
        elif action == "stay":
            env.steps += 1
            history.append(("stay", env.agent_pos))
            if verbose:
                print("Agent stays.")
        else:
            env.steps += 1
            history.append(("unknown", env.agent_pos))

    return history


if __name__ == "__main__":
    # Example setup: 5x4 grid, agent starts at (0,0), some dirt scattered.
    width, height = 5, 4
    dirt_positions = {(4, 0), (2, 1), (1, 3), (3, 2)}
    agent_start = (0, 0)
    env = Environment(width, height, dirt_positions, agent_start)
    agent = UtilityAgent(reward_clean=10.0, move_cost=1.0, time_penalty=0.1, clean_cost=0.2)

    history = run_simulation(env, agent, max_steps=100, verbose=True)

    print("\nHistory (first 20 steps):")
    for h in history[:20]:
        print(h)