import random

from components.selection import BaseSelector


class GeneticAlgorithmTSP:
    def __init__(self, population_size: int, n_iterations: int,
                 selector: BaseSelector) -> None:

        self.population_size = population_size
        self.n_iterations = n_iterations
        self.selector = selector

    def create_base_population(self, city_size: int) -> dict:
        base_population = {}

        for i in range(self.population_size):
            random_individual = list(range(city_size))
            random.shuffle(random_individual)

            base_population[i] = random_individual

        return base_population

    def evaluate(self, population: dict, cost_data: list) -> dict:
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
                    score = sum([cost_data[coordinates[0]][coordinates[1]]
                                if coordinates[0] > coordinates[1]
                                else cost_data[coordinates[1]][coordinates[0]]
                                for coordinates in coordinates_list])

                    population_score[index] = score

        return population_score

        def learn(self):
            pass
