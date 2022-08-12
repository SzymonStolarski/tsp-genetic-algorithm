import random

from components.evaluate.tsp_evaluate import evaluate
from components.tsp_algorithms.base_algorithm import BaseTspAlgorithm


class TabuSearch(BaseTspAlgorithm):

    def __init__(self, n_iterations: int, n_candidates: int,
                 tabu_iterations: int = 3):

        self.n_iterations = n_iterations
        self.n_candidates = n_candidates
        self.tabu_iterations = tabu_iterations

    def learn(self, cost_matrix: list):
        self._results = {}
        self._best_result = 0

        iteration = 0
        # create initial solution
        route = self.__initial_route(city_size=len(cost_matrix))
        evaluated_route = evaluate(route, cost_matrix)[1]

        self._results[iteration] = evaluated_route
        self._best_result = min(list(self._results.values()))
        self._paths[iteration] = route
        self._best_path = route

        tabu_list = {}
        while not iteration == self.n_iterations:
            iteration += 1
            tabu_list = self.__tabu_list_cleaning(tabu_list)

            # create a candidate list of moves
            candidate_list = {}
            tabu_pretenders = {}
            for candidate in range(0, self.n_candidates):
                candidate_list[candidate], tabu_pretenders[candidate]\
                    = self.__create_candidate(route[1])

            # evaluate the list of candidates
            evaluated_candidates = evaluate(candidate_list, cost_matrix)

            # sort it
            evaluated_candidates_sorted = {k: v for k, v in sorted(
                evaluated_candidates.items(), key=lambda item: item[1])}
            # same order of keys in `tabu_pretenders`
            keyorder = list(evaluated_candidates_sorted.keys())
            tabu_pretenders = {k: tabu_pretenders[k] for k in keyorder
                               if k in tabu_pretenders}

            for idx, distance in evaluated_candidates_sorted.items():
                # does it have better evaluation than any other move?
                if distance < list(self._results.values())[-1]:
                    # is it on tabu?
                    if tabu_pretenders[idx] in tabu_list.keys():
                        # Check if the move is admissable (best thus far)
                        if distance < self._best_result:
                            self._results[iteration] = distance
                            self._best_result = min(
                                list(self._results.values()))
                            self._best_path = self._paths[
                                min(self._results, key=self._results.get)]
                            tabu_list[tabu_pretenders[
                                idx]] = self.tabu_iterations
                            break
                        else:
                            # Check next neighbourhood candidate
                            continue
                    else:
                        self._results[iteration] = distance
                        self._best_result = min(
                            list(self._results.values()))
                        self._best_path = self._paths[
                            min(self._results, key=self._results.get)]
                        tabu_list[tabu_pretenders[idx]] = self.tabu_iterations
                        break

            if iteration % 10000 == 0:
                print(self._best_result)

        return self

    def __initial_route(self, city_size: int) -> dict:
        random_route = list(range(city_size))
        random.shuffle(random_route)

        # Currently this way in order to be compatible
        # with the evaluate function from GA algorithm
        # that uses dictionary as whole population
        random_route = {1: random_route}

        return random_route

    def __create_candidate(self, current_route: list):
        neighbour_candidate = current_route.copy()

        idx_1 = 0
        idx_2 = 0
        while idx_1 == idx_2:
            idx_1 = random.randint(0, len(current_route)-1)
            idx_2 = random.randint(0, len(current_route)-1)

        neighbour_candidate[idx_1] = current_route[idx_2]
        neighbour_candidate[idx_2] = current_route[idx_1]

        # we need somewhere to track the indexes that could
        # be stored in the tabu list as forbidden moves
        tabu_pretender = tuple({idx_1, idx_2})

        return neighbour_candidate, tabu_pretender

    def __tabu_list_cleaning(self, tabu_list: dict) -> dict:
        decremented_tabu = {k: v-1 for k, v in tabu_list.items()}
        cleaned_tabu = {k: v for k, v in decremented_tabu.items()
                        if not v == 0}

        return cleaned_tabu
