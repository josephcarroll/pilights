import math
import time
from Snake import Direction, State


class AIPlayer:
    def __init__(self):
        self.known_food_location = None
        self.optimal_path = []

    def take_turn(self, game):
        """
        :type game: Snake.Snake
        """

        # We always restart the game if dead!
        if game.state == State.game_over:
            game.start()
            return

        if self.known_food_location is None or self.known_food_location != game.food:
            self.known_food_location = game.food
            time1 = time.time()
            self.optimal_path = self.search_for_move(game)[1:]  # We exclude the first entry as that's our location!
            time2 = time.time()
            print "Path creation took {}ms".format((time2-time1)*1000.0)

        current_head = game.snake[-1]

        if len(self.optimal_path) > 0:
            path_head = self.optimal_path[0]
            self.optimal_path = self.optimal_path[1:]

            cx = current_head.x
            cy = current_head.y
            tx = path_head.x
            ty = path_head.y

            if tx < cx and ty == cy:
                game.change_direction(Direction.left)
            elif tx > cx and ty == cy:
                game.change_direction(Direction.right)
            elif ty < cy and tx == cx:
                game.change_direction(Direction.up)
            elif ty > cy and tx == cx:
                game.change_direction(Direction.down)
        else:
            print 'No path found! Gonna die!'

    def search_for_move(self, game):
        start = game.snake[-1]
        goal = game.food

        closed_set = set()
        open_set = set()
        open_set.add(start)
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = self.heuristic_cost_estimate(start, goal)

        while len(open_set) > 0:
            current = self.lowest_cost_from(open_set, f_score)
            if current == goal:
                return self.path_from(came_from, goal)
            open_set.remove(current)
            closed_set.add(current)
            for neighbour in self.neighbours_of(current, game.snake):
                if neighbour in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1  # All neighbours are 1 unit away!
                if neighbour not in open_set or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = g_score[neighbour] + self.heuristic_cost_estimate(neighbour, goal)
                if neighbour not in open_set:
                    open_set.add(neighbour)
        return []

    def neighbours_of(self, current, snake):
        possible_neighbours = [
            current._replace(x=current.x - 1),
            current._replace(x=current.x + 1),
            current._replace(y=current.y - 1),
            current._replace(y=current.y + 1),
        ]
        return [n for n in possible_neighbours if n not in snake]

    def path_from(self, came_from, goal):
        current_node = goal
        path = [current_node]

        previous = came_from.get(current_node)
        while previous is not None:
            path.append(previous)
            previous = came_from.get(previous)

        path.reverse()
        return path

    # Optimise using a sorted heap!
    def lowest_cost_from(self, open_set, f_score):
        min_node = None
        for node in open_set:
            node_score = f_score[node]
            if min_node is None or node_score < min_node[1]:
                min_node = (node, node_score)
        return min_node[0]

    def heuristic_cost_estimate(self, start, goal):
        """
        :type start: Snake.Position
        :type goal: Snake.Position
        """
        return math.sqrt(math.pow(start.x - goal.x, 2) + math.pow(start.y - goal.y, 2))