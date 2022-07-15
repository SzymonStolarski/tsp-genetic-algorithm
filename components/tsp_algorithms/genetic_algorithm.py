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
                 verbose: bool = True, atomic_bomb: int = None) -> None:

        self.population_size = population_size
        self.n_iterations = n_iterations
        self.selector = selector
        self.crossover = crossover
        self.mutator = mutator
        self.maximize = maximize
        self.verbose = verbose
        self.atomic_bomb = atomic_bomb

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
        evaluated_population = evaluate(population, cost_matrix)

        if not self.maximize:
            self.__results[iteration] = min(
                list(evaluated_population.values()))
            self.__paths[iteration] = population[
                min(evaluated_population, key=evaluated_population.get)]
        else:
            self.__results[iteration] = max(
                list(evaluated_population.values()))
            self.__paths[iteration] = population[
                max(evaluated_population, key=evaluated_population.get)]
        if self.verbose:
            print('Starting algorithm...')
            print(f'Iteration: {iteration}. \
                  Best result: {self.__results[iteration]}')

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

            if not self.maximize:
                self.__results[iteration] = min(
                    list(evaluated_population.values()))
                self.__paths[iteration] = population[
                    min(evaluated_population, key=evaluated_population.get)]
            else:
                self.__results[iteration] = max(
                    list(evaluated_population.values()))
                self.__paths[iteration] = population[
                    max(evaluated_population, key=evaluated_population.get)]
            if self.verbose and iteration % 100 == 0:
                print(f'Iteration: {iteration}. \
                      Best result: {self.__results[iteration]}')

            # Atomic bomb component - kill population after stagnation
            if (self.atomic_bomb is not None
                and iteration > self.atomic_bomb
                    and (self.__results[iteration] == self.__results[
                        iteration - self.atomic_bomb])):

                population = self._create_base_population(len(cost_matrix))

        if not self.maximize:
            self.__best_result = min(list(self.__results.values()))
            self.__best_path = self.__paths[min(self.__results,
                                                key=self.__results.get)]
        else:
            self.__best_result = min(list(self.__results.values()))
            self.__best_path = self.__paths[min(self.__results,
                                                key=self.__results.get)]
        if self.verbose:
            print('Algorithm finished.')

        return self

    def _create_base_population(self, city_size: int) -> dict:
        base_population = {}

        for i in range(self.population_size):
            random_individual = list(range(city_size))
            random.shuffle(random_individual)

            base_population[i] = random_individual

        return base_population
