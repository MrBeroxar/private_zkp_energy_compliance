import numpy as np
from scipy.stats import norm


class GaussianMockDataGenerator:
    def __init__(self, array_size, variance=5):
        if array_size % 8 != 0:
            raise ValueError("array_size must be a multiple of 8.")
        self.array_size = array_size
        self.variance = variance

    def compute_net_result(self, consumption, production):
        # Prime number of Bls12_377
        p = 8444461749428370424248824938781546531375899335154063827935233455917409239041
        net_result = sum(consumption) - sum(production)
        if sum(production) > sum(consumption):
            net_result += p
        return int(net_result)

    def get_gaussian_mock_data(self, consumption_mean, production_mean):

        produce_distribution = norm(production_mean, self.variance)
        consume_distribution = norm(consumption_mean, self.variance)
        produce_data = []
        consume_data = []

        for _ in range(self.array_size):

            produce_sample = np.round(produce_distribution.rvs(1)[0], 2)
            consume_sample = np.round(consume_distribution.rvs(1)[0], 2)

            produce = max(produce_sample, 0)
            consume = max(consume_sample, 0)

            produce_data.append(int(produce * 100))
            consume_data.append(int(consume * 100))

        netResult = self.compute_net_result(consume_data, produce_data)
        return consume_data, produce_data, netResult
