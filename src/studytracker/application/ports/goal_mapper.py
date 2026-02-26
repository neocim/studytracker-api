from abc import abstractmethod
from typing import Protocol

from studytracker.application.dto.goal import CreatedGoal, GoalReadModel, GoalWithSubgoalsReadModel
from studytracker.domain.entities.goal import Goal


class GoalMapper(Protocol):
    @abstractmethod
    def to_created(self, goal: Goal) -> CreatedGoal:
        raise NotImplementedError

    @abstractmethod
    def to_readmodel(self, goal: Goal) -> GoalReadModel:
        raise NotImplementedError

    @abstractmethod
    def to_readmodel_with_subgoals(self, goal: Goal) -> GoalWithSubgoalsReadModel:
        raise NotImplementedError
