import itertools

from components.tsp_algorithms.genetic_algorithm import GeneticAlgorithmTSP
from components.crossover import BaseCrossover
from components.mutation import BaseMutator
from components.selection import BaseSelector


class GridSearchGA:

    def __init__(self, params: dict, maximize: bool = False,
                 verbose: bool = True) -> None:
        self.params = params
        self.maximize = maximize
        self.verbose = verbose

    def learn(self, cost_data: list):
        self.__grid_search_results = {}
        self.__grid_search_paths = {}
        self.__grid_search_params = {}

        self.__best_grid_search_result = 0
        self.__best_grid_search_path = []
        self.__best_grid_search_params = {}

        params_generator = (dict(zip(self.params, x))
                            for x in itertools.product(*self.params.values()))
        no_of_combinations = sum(1 for x in params_generator)-1
        params_generator = (dict(zip(self.params, x))
                            for x in itertools.product(*self.params.values()))

        iterator = 0

        for params in params_generator:
            if self.verbose:
                print(f'Iteration {iterator}/{no_of_combinations}')
            algorithm = GeneticAlgorithmTSP(**params)
            algorithm.learn(cost_data)

            self.__grid_search_results[iterator] = algorithm.best_result
            self.__grid_search_paths[iterator] = algorithm.best_path
            self.__grid_search_params[iterator] = {k: ({v.__class__.__name__:
                                                        v.__dict__}
                                                       if isinstance(v, (BaseCrossover, BaseSelector, BaseMutator))
                                                       else v) for k, v in params.items()}
            if self.verbose:
                print(f'Iteration: {iterator}. Result: {algorithm.best_result}')
            iterator += 1

        if not self.maximize:
            self.__best_grid_search_result = min(list(self.__grid_search_results.values()))
            self.__best_grid_search_path = self.__grid_search_paths[min(self.__grid_search_results,
                                                key=self.__grid_search_results.get)]
            self.__best_grid_search_params = self.__grid_search_params[min(self.__grid_search_results,
                                                key=self.__grid_search_results.get)]
        else:
            self.__best_grid_search_result = max(list(self.__grid_search_results.values()))
            self.__best_grid_search_path = self.__grid_search_paths[max(self.__grid_search_results,
                                                key=self.__grid_search_results.get)]
            self.__best_grid_search_params = self.__grid_search_params[max(self.__grid_search_results,
                                                key=self.__grid_search_results.get)]

        return self

    @property
    def grid_search_results(self):
        return self.__grid_search_results

    @property
    def grid_search_paths(self):
        return self.__grid_search_paths

    @property
    def grid_search_params(self):
        return self.__grid_search_paths

    @property
    def best_grid_search_result(self):
        return self.__best_grid_search_result

    @property
    def best_grid_search_path(self):
        return self.__best_grid_search_path

    @property
    def best_grid_search_params(self):
        return self.__best_grid_search_params
