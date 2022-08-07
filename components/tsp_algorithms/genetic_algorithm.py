import random

from components.evaluate.tsp_evaluate import evaluate
from components.ga_components.selection import BaseSelector
from components.ga_components.crossover import BaseCrossover
from components.ga_components.mutation import BaseMutator
from components.tsp_algorithms.base_algorithm import BaseTspAlgorithm


class GeneticAlgorithmTsp(BaseTspAlgorithm):
    def __init__(self, population_size: int, n_iterations: int,
                 selector: BaseSelector, crossover: BaseCrossover,
                 mutator: BaseMutator, maximize: bool = False,
                 verbose: bool = True, atomic_bomb: int = None):

        self.population_size = population_size
        self.n_iterations = n_iterations
        self.selector = selector
        self.crossover = crossover
        self.mutator = mutator
        self.maximize = maximize
        self.verbose = verbose
        self.atomic_bomb = atomic_bomb

    def learn(self, cost_matrix: list):
        self._results = {}
        self._paths = {}
        self._best_result = 0
        self._best_path = []

        iteration = 0
        population = self.__create_base_population(len(cost_matrix))
        evaluated_population = evaluate(population, cost_matrix)

        self._results[iteration] = min(
            list(evaluated_population.values()))
        self._paths[iteration] = population[
            min(evaluated_population, key=evaluated_population.get)]

        if self.verbose:
            print('Starting algorithm...')
            print(f'Iteration: {iteration}. \
                  Best result: {self._results[iteration]}')

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
            evaluated_population = evaluate(population, cost_matrix)

            self._results[iteration] = min(
                list(evaluated_population.values()))
            self._paths[iteration] = population[
                min(evaluated_population, key=evaluated_population.get)]

            if self.verbose and iteration % 100 == 0:
                print(f'Iteration: {iteration}. \
                      Best result: {self._results[iteration]}')

            # Atomic bomb component - kill population after stagnation
            if (self.atomic_bomb is not None
                and iteration > self.atomic_bomb
                    and (self._results[iteration] == self._results[
                        iteration - self.atomic_bomb])):

                population = self.__create_base_population(len(cost_matrix))

            self._best_result = min(list(self._results.values()))
            self._best_path = self._paths[min(self._results,
                                              key=self._results.get)]

        if self.verbose:
            print('Algorithm finished.')

        return self

    def __create_base_population(self, city_size: int) -> dict:
        base_population = {}

        for i in range(self.population_size):
            random_individual = list(range(city_size))
            random.shuffle(random_individual)

            base_population[i] = random_individual

        return base_population
