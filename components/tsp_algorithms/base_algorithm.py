from abc import ABC, abstractmethod
import random


class BaseTspAlgorithm(ABC):

    @abstractmethod
    def learn(self):
        pass

    def _create_base_population(self, city_size: int) -> dict:
        base_population = {}

        for i in range(self.population_size):
            random_individual = list(range(city_size))
            random.shuffle(random_individual)

            base_population[i] = random_individual

        return base_population

    @property
    def results(self):
        return self._results

    @property
    def paths(self):
        return self._paths

    @property
    def best_result(self):
        return self._best_result

    @property
    def best_path(self):
        return self._best_path
