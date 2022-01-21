class Tools:

    @staticmethod
    def get_one_hot_encoded_feature_list(feature_list: list, class_feature_dict: dict):

        """Gets the one-hot encoding of a given feature list according to a given dict.

        Returns:
            list[float]: The one-hot encoded feature list.
        """

        one_hot_encoded_feature_list = []

        for i in range(len(feature_list)):

            if i in class_feature_dict.keys():
                one_hot_encoded_feature_list.append(Tools.get_one_hot_encoding(len(class_feature_dict[i]), class_feature_dict[i].index(feature_list[i])))
            else:
                one_hot_encoded_feature_list.append(feature_list[i])

        return Tools.flatten_list(one_hot_encoded_feature_list)

    @staticmethod
    def get_one_hot_encoding(n_classes: int, class_number: int):

        """Helper function that the one hot encoding for one specific element by specifying the number of classes and the class of the current element.

        Raises:
            ValueError: If a class number is requested that is higher than the maximum number of classes.

        Returns:
            list[int]: The one hot encoding of one element.
        """

        if class_number >= n_classes:
            raise ValueError('Cannot get one hot encoding for a class number higher than the number of classes.')

        # return empty list if there is only one type
        if n_classes == 1:
            return []

        return [1 if x == class_number else 0 for x in list(range(n_classes))]

    @staticmethod
    def get_class_feature_indices(feature_list):

        """Takes a feature list a determines at which positions non-numerical class features are used.

        Returns:
            list[int]: A list with indices denoting at which positions non-numerical class features are used.
        """

        class_feature_indices = []

        # get indices of features that are not numeric and need to be one-hot encoded
        for i in range(len(feature_list)):
            if not type(feature_list[i]) == int and not type(feature_list[i]) == float:
                class_feature_indices.append(i)

        return class_feature_indices

    @staticmethod
    def flatten_list(input_list):

        """Flattens a irregular list. Embeds any sublist as individual values in main list.

        Returns:
            list[]: The flattend list.
        """

        flattend_list = []
        for element in input_list:
            if isinstance(element, list):
                flattend_list.extend(Tools.flatten_list(element))
            else:
                flattend_list.append(element)

        return flattend_list

    @staticmethod
    def calculate_euclidean_distance(x: list[float], y: list[float]) -> float:

        """Calculates the euclidean distance between to points given as lists.

        Returns:
            float: The euclidean distance between the points
        """

        # make sure both lists have the same length
        assert len(x) == len(y)

        # get dimension wise squared distances
        squares = [(a - b) ** 2 for a, b in zip(x, y)]

        # return sum of square root
        return sum(squares) ** 0.5

    @staticmethod
    def calculate_distance_matrix(points: list[list[float]]) -> list[list[float]]:

        """Calculates the distance matrix of a list of points.

        Returns:
            list[list[float]]: The distance matrix.
        """

        # setup matrix
        distance_matrix = [[0 for x in range(len(points))] for y in range(len(points))]

        # iterate over the upper triangle
        for i in range(len(distance_matrix) - 1):
            for j in range(i + 1, len(distance_matrix), 1):
                distance = Tools.calculate_euclidean_distance(points[i], points[j])
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
