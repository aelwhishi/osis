from base.tests.factories.learning_container import LearningContainerFactory


class LearningContainerMixin:

    @staticmethod
    def init():
        return LearningContainerFactory()
