from typing import override

from studytracker.application.dto.goal import CreatedGoal, GoalReadModel, GoalWithSubgoalsReadModel
from studytracker.application.ports.goal_mapper import GoalMapper
from studytracker.domain.entities.goal import Goal


class GoalMapperImpl(GoalMapper):
    @override
    def to_created(self, goal: Goal) -> CreatedGoal:
        return CreatedGoal(goal_id=goal.entity_id)

    @override
    def to_readmodel(self, goal: Goal) -> GoalReadModel:
        return GoalReadModel(
            goal_id=goal.entity_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )

    @override
    def to_readmodel_with_subgoals(self, goal: Goal) -> GoalWithSubgoalsReadModel:
        subgoals = []
        if goal.subgoals:
            subgoals = [self.to_readmodel_with_subgoals(subgoal) for subgoal in goal.subgoals]

        return GoalWithSubgoalsReadModel(
            goal_id=goal.entity_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            subgoals=subgoals,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )
