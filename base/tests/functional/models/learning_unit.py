from base.tests.factories.learning_unit import LearningUnitFactory


class LearningUnitMixin:

    @staticmethod
    def init(learning_container=None):

        if learning_container:
            learning_unit = LearningUnitFactory(learning_container=learning_container)
        else:
            learning_unit = LearningUnitFactory()

        return learning_unit
