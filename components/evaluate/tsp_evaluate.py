def evaluate(population: dict, cost_matrix: list) -> dict:
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
                            else cost_matrix[
                                coordinates[1]][coordinates[0]]
                            for coordinates in coordinates_list])

                population_score[index] = score

    return population_score
