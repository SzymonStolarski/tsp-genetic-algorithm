from math import exp
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
        cost_prev = evaluate(route, cost_matrix)[1]

        temp = self.temp_start
        iteration = 1

        self._results = {}

        self._results[iteration] = cost_prev
        self._best_result = min(list(self._results.values()))

        while temp >= self.temp_end:
            iteration += 1
            route = self.__create_route(len(cost_matrix))
            cost_new = evaluate(route, cost_matrix)[1]
            difference = cost_new - cost_prev

            if difference < 0 or exp(-difference/temp) > random.random():
                cost_prev = cost_new
                self._results[iteration] = cost_prev
            else:
                self._results[iteration] = cost_new

            self._best_result = min(list(self._results.values()))

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
