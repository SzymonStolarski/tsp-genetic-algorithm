from abc import ABC, abstractmethod
import random


class BaseSelector(ABC):

    @abstractmethod
    def selection(self, evaluated_population) -> list:
        return


class ElitismSelector(BaseSelector):

    def __init__(self, percent: float, maximize: bool = False) -> None:
        self.percent = percent
        self.maximize = maximize

    def selection(self, evaluated_population: dict) -> list:
        no_of_elite_individuals = (int(len(
                                   evaluated_population)*self.percent))
        sorted_evaluation = {k: v for k, v in sorted(
                             evaluated_population.items(),
                             key=lambda item: item[1], reverse=self.maximize)}
        best_individuals = [k for k in
                            list(
                                 sorted_evaluation.keys()
                                 )[:no_of_elite_individuals]
                            ]

        missing_multiplier = int(
                            len(evaluated_population)/no_of_elite_individuals
                                )
        selected_individuals = missing_multiplier*best_individuals
        if len(selected_individuals) < len(evaluated_population):
            difference = (len(evaluated_population)-len(selected_individuals))
            selected_individuals.extend(selected_individuals[:difference])

        return selected_individuals


class TournamentSelector(BaseSelector):

    def __init__(self, k_percent: float, maximize: bool = False) -> None:
        self.k_percent = k_percent
        self.maximize = maximize

    def selection(self, evaluated_population: dict) -> list:
        population_size = len(evaluated_population)
        no_of_ind_in_tournament = int(self.k_percent*population_size)

        selected_individuals = []
        iterator = 0
        while not iterator == len(evaluated_population):
            selected_keys = random.sample(
                            range(population_size), no_of_ind_in_tournament
                            )
            tournament = {k: evaluated_population[k] for k in selected_keys}
            if not self.maximize:
                winner = min(tournament, key=tournament.get)
            else:
                winner = max(tournament, key=tournament.get)

            selected_individuals.append(winner)
            iterator += 1

        return selected_individuals


class RouletteSelector(BaseSelector):

    def __init__(self, maximize: bool = False) -> None:
        self.maximize = maximize

    def selection(self, evaluated_population: dict) -> list:
        sum_of_scores = sum([v for v in evaluated_population.values()])
        if not self.maximize:
            dict_of_share_initial = {k: v/sum_of_scores for k, v
                                     in evaluated_population.items()}
            dict_of_share_sorted = {k: v for k, v in sorted(
                                    dict_of_share_initial.items(),
                                    key=lambda item: item[1], reverse=False)}
            reversed_keys = list(dict_of_share_sorted.keys())
            reversed_keys.reverse()
            dict_of_share = {k: v for k, v in zip(reversed_keys,
                             dict_of_share_sorted.values())}
        else:
            dict_of_share = {k: v/sum_of_scores for k, v
                             in evaluated_population.items()}
            dict_of_share = {k: v for k, v in sorted(dict_of_share.items(),
                             key=lambda item: item[1], reverse=False)}

        ranges = []
        for idx, value in enumerate(dict_of_share.values()):
            if idx == 0:
                current_range = [0, value]
                previous_value = value
                ranges.append(current_range)
                continue

            current_range = [previous_value, previous_value+value]
            previous_value = previous_value+value
            ranges.append(current_range)
        dict_with_ranges = {k: v for k, v in zip(dict_of_share.keys(), ranges)}

        selected_individuals = []
        iterator = 0
        while not iterator == len(evaluated_population):
            random_number = random.random()
            selected_individual = [k for k, v in dict_with_ranges.items()
                                   if random_number > v[0]
                                   and random_number <= v[1]
                                   ][0]
            selected_individuals.append(selected_individual)
            iterator += 1

        return selected_individuals
