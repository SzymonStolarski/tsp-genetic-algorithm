import math
import random

from components.evaluate.tsp_evaluate import evaluate
from components.tsp_algorithms.base_algorithm import BaseTspAlgorithm


class SimulatedAnnealing(BaseTspAlgorithm):

    def __init__(self, temp_start: float, temp_end: float,
                 cooling_factor: float):

        self.temp_start = temp_start
        self.temp_end = temp_end
        self.cooling_factor = cooling_factor

    def learn(self, cost_matrix: list):

        route = self.__create_route(len(cost_matrix))
        cost_prev = evaluate(route, cost_matrix)

        temp = self.temp_start
        while temp >= self.temp_end:
            route = self.__create_route(len(cost_matrix))
            cost_new = evaluate(route, cost_matrix)
            difference = cost_new - cost_prev

            if difference < 0 or math.exp(-difference/temp) > random():
                cost_prev = cost_new

            temp = temp * self.cooling_factor

        return self

    def __create_route(self, city_size: int) -> list:

        random_route = list(range(city_size))
        random.shuffle(random_route)

        # Currently this way in order to be compatible
        # with the evaluate function from GA algorithm
        # that uses dictionary as whole population
        random_route = {1: random_route}

        return random_route
