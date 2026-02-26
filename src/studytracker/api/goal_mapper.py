import studytracker.api.dto.responses.goal as goal_response
from studytracker.application.dto.goal import CreatedGoal, GoalReadModel, GoalWithSubgoalsReadModel


class APIGoalMapper:
    def to_created_response(self, goal: CreatedGoal) -> goal_response.CreatedGoal:
        return goal_response.CreatedGoal(goal_id=goal.goal_id)

    def to_goal_response(self, goal: GoalReadModel) -> goal_response.Goal:
        return goal_response.Goal(
            goal_id=goal.goal_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )

    def to_goal_with_subgoals_response(self, goal: GoalWithSubgoalsReadModel) -> goal_response.GoalWithSubgoals:
        subgoals = []
        if goal.subgoals:
            subgoals = [self.to_goal_with_subgoals_response(subgoal) for subgoal in goal.subgoals]

        return goal_response.GoalWithSubgoals(
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
