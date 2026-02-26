import studytracker.api.dto.responses.goal as response
from studytracker.application.dto.goal import CreatedGoal, GoalReadModel, GoalWithSubgoalsReadModel


class APIGoalMapper:
    def created_response(self, goal: CreatedGoal) -> response.CreatedGoal:
        return response.CreatedGoal(goal_id=goal.goal_id)

    def goal_response(self, goal: GoalReadModel) -> response.Goal:
        return response.Goal(
            goal_id=goal.goal_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )

    def with_subgoals_response(self, goal: GoalWithSubgoalsReadModel) -> response.GoalWithSubgoals:
        subgoals = []
        if goal.subgoals:
            subgoals = [self.with_subgoals_response(subgoal) for subgoal in goal.subgoals]

        return response.GoalWithSubgoals(
            goal_id=goal.goal_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            subgoals=subgoals,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )
