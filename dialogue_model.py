import logging
import rasa_core

from rasa_core.agent import Agent
from rasa_core.domain import Domain
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    dialog_training_data_file = './config/stories.md'
    path_to_model = './models/dialogue'
    # domain = Domain()
    featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(),
                                             max_history=5)
    agent = Agent('config/chat_domain.yml',
                  policies=[MemoizationPolicy(max_history=5),
                            KerasPolicy(featurizer)])
    # agent = Agent('data/chat_domain.yml', policies = [MemoizationPolicy(), KerasPolicy()])

    agent.train(
        dialog_training_data_file,
        augmentation_factor=50,
        epochs=500,
        batch_size=10,
        validation_split=0.2)
    agent.persist(path_to_model)
