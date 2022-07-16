from abc import ABC, abstractmethod


class BaseTspAlgorithm(ABC):

    @abstractmethod
    def learn(self):
        pass

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
