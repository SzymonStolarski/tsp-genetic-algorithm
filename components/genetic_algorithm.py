import random

from components.selection import BaseSelector
from components.crossover import BaseCrossover
from components.mutation import BaseMutator


class GeneticAlgorithmTSP:
    def __init__(self, population_size: int, n_iterations: int,
                 selector: BaseSelector, crossover: BaseCrossover,
                 mutator: BaseMutator, maximize: bool = False) -> None:

        self.population_size = population_size
        self.n_iterations = n_iterations
        self.selector = selector
        self.crossover = crossover
        self.mutator = mutator
        self.maximize = maximize

    @property
    def results(self):
        return self.__results

    @property
    def paths(self):
        return self.__paths

    @property
    def best_result(self):
        return self.__best_result

    @property
    def best_path(self):
        return self.__best_path

    def learn(self, cost_matrix: list):
        self.__results = {}
        self.__paths = {}
        self.__best_result = 0
        self.__best_path = []

        iteration = 0
        population = self._create_base_population(len(cost_matrix))
        evaluated_population = self._evaluate(population, cost_matrix)

        if not self.maximize:
            self.__results[iteration] = min(list(evaluated_population.values()))
            self.__paths[iteration] = population[min(evaluated_population,
                                                     key=evaluated_population.get)
                                                 ]
        else:
            self.__results[iteration] = max(list(evaluated_population.values()))
            self.__paths[iteration] = population[max(evaluated_population,
                                                     key=evaluated_population.get)
                                                 ]
        print(f'Iteration: {iteration}. Best result: {self.__results[iteration]}')

        while not iteration == self.n_iterations:
            # Increment iteration here because iteration 0 was base population
            iteration += 1

            # Selection
            selected_population = self.selector.selection(population,
                                                          evaluated_population,
                                                          self.maximize)
            # Mutation
            population = self.mutator.mutate(selected_population)
            # Crossover
            population = self.crossover.crossover(population)
            # Evaluation
            evaluated_population = self._evaluate(population, cost_matrix)

            if not self.maximize:
                self.__results[iteration] = min(list(evaluated_population.values()))
                self.__paths[iteration] = population[min(evaluated_population,
                                                        key=evaluated_population.get)
                                                     ]
            else:
                self.__results[iteration] = max(list(evaluated_population.values()))
                self.__paths[iteration] = population[max(evaluated_population,
                                                        key=evaluated_population.get)
                                                     ]

            print(f'Iteration: {iteration}. Best result: {self.__results[iteration]}')

        if not self.maximize:
            self.__best_result = min(list(self.__results.values()))
            self.__best_path = self.__paths[min(self.__results,
                                                key=self.__results.get)]
        else:
            self.__best_result = min(list(self.__results.values()))
            self.__best_path = self.__paths[min(self.__results,
                                                key=self.__results.get)]

        return self

    def _create_base_population(self, city_size: int) -> dict:
        base_population = {}

        for i in range(self.population_size):
            random_individual = list(range(city_size))
            random.shuffle(random_individual)

            base_population[i] = random_individual

        return base_population

    def _evaluate(self, population: dict, cost_matrix: list) -> dict:
        population_score = {}

        for index, values in population.items():

            # For each individual in population we need to create a
            # list of route coordinates from city 10 to 15: [10, 15]
            coordinates_list = []

            for idx, value in enumerate(values):
                if idx == 0:
                    first_city_value = value
                    continue

                coordinates = [values[idx-1], values[idx]]
                coordinates_list.append(coordinates)

                if idx+1 == len(values):
                    last_city_value = value
                    # On our last route we need to come back to the
                    # starting point
                    last_route_coordinates = [last_city_value,
                                              first_city_value]
                    coordinates_list.append(last_route_coordinates)

                    # Calculate the full cost for given individual
                    # Takes the cost of each route from the cost matrix
                    # Not the prettiest syntax, however quite fast solution
                    score = sum([cost_matrix[coordinates[0]][coordinates[1]]
                                if coordinates[0] > coordinates[1]
                                else cost_matrix[coordinates[1]][coordinates[0]]
                                for coordinates in coordinates_list])

                    population_score[index] = score

        return population_score
