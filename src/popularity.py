import numpy as np
from recommender import Recommender
from measurements import Measurements
import matplotlib.pyplot as plt

class PopularityRecommender(Recommender):
    def __init__(self, num_users, num_items, num_startup_iter=10, num_items_per_iter=10,
        randomize_recommended=True, num_recommended=None, num_new_items=None,
        user_preference=False):
        # TODO: check on invalid parameters
        self.user_profiles = np.ones((num_users, 1), dtype=int)
        self.item_attributes = np.zeros((1, num_items), dtype=int)
        super().__init__(num_users, num_items, num_startup_iter, num_items_per_iter,
        randomize_recommended, num_recommended, num_new_items,
        user_preference, Measurements(num_items, num_users))

    def _store_interaction(self, interactions):
        self.item_attributes = np.add(self.item_attributes, interactions)

    def train(self):
        return super().train()

    def interact(self, plot=False, startup=False):
        if startup:
            num_new_items = self.num_items_per_iter
            num_recommended = 0
        elif self.randomize_recommended:
            num_new_items = np.random.randint(1, self.num_items_per_iter)
            num_recommended = self.num_items_per_iter-num_new_items
        else:
            # TODO: these may be constants or iterators on vectors
            num_new_items = self.num_new_items
            num_recommended = self.num_recommended
        recommended = self.recommend(k=num_recommended) if not startup else None
        if num_recommended > 0:
            assert(num_recommended == recommended.shape[1])
        interactions = super().interact(recommended, num_new_items)
        interaction_matrix = self.measure_equilibrium(interactions, plot=plot)
        self._store_interaction(interaction_matrix)

    # Recommends items proportional to their popularity
    def recommend(self, k=1):
        return super().recommend(k)

    def startup_and_train(self, timesteps=50, debug=False):
        return super().startup_and_train(timesteps, debug)

    def run(self, timesteps=50, train=True, debug=False):
        return super().run(timesteps, train, debug)

    def get_heterogeneity(self):
        return self.measurements.get_delta()

    def measure_equilibrium(self, interactions, plot=False):
        return self.measurements.measure_equilibrium(interactions, plot)