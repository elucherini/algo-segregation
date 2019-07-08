import argparse
import numpy as np
import constants as const
import matplotlib.pyplot as plt

from popularity import PopularityRecommender
from content import ContentFiltering

if __name__ == '__main__':
    # Supported recommender systems
    rec_dict = {'popularity':PopularityRecommender, 'content':ContentFiltering}
    # Supported additional arguments for each recommender system
    rec_args = {'popularity': None}
    # A: number of attributes; items_representation: non-random representation of items based on attributes
    rec_args['content'] = {'A':100}
    rec_args['content']['items_representation'] = np.zeros((const.NUM_ITEMS, rec_args['content']['A']))
    
    for i, row in enumerate(rec_args['content']['items_representation']):
        A = rec_args['content']['A']
        n_indices = np.random.randint(1, A)
        indices = np.random.randint(A, size=(n_indices))
        row[indices] = 1
        rec_args['content']['items_representation'][i,:] = row
    rec_args['content']['items_representation'] = rec_args['content']['items_representation'].T
    
    choices = set(rec_dict.keys())

    parser = argparse.ArgumentParser()
    parser.add_argument('recommender', metavar='r', type=str, nargs=1, help='Type of recommender system',
        choices=choices)
    parser.add_argument('--debug', '-d', help='Debug info', action='store_true')

    args = parser.parse_args()
    rec_type = args.recommender[0]

    if rec_args[rec_type] is None:
        rec = rec_dict[rec_type](const.NUM_USERS, const.NUM_ITEMS, num_startup_iter=const.NUM_STARTUP_ITER,
            num_items_per_iter=const.NUM_ITEMS_PER_ITER, randomize_recommended=True, user_preference=False)
    else:
        rec = rec_dict[rec_type](const.NUM_USERS, const.NUM_ITEMS, num_startup_iter=const.NUM_STARTUP_ITER,
            num_items_per_iter=const.NUM_ITEMS_PER_ITER, randomize_recommended=True, user_preference=False, 
            **rec_args[rec_type])

    print('Num items:', const.NUM_ITEMS, '\nUsers:', const.NUM_USERS, '\nItems per iter:', const.NUM_ITEMS_PER_ITER)
    print('Recommender system:', rec_type)

    # Startup
    rec.startup_and_train(const.NUM_STARTUP_ITER, debug=args.debug)

    # Runtime
    rec.run(const.TIMESTEPS - const.NUM_STARTUP_ITER, debug=args.debug, train=True)

    delta_t = rec.get_heterogeneity()
    plt.style.use('seaborn-whitegrid')
    plt.plot(np.arange(len(delta_t)), delta_t)
    plt.show()
    