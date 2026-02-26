from dishka import Provider, Scope, provide

from studytracker.api.goal_mapper import APIGoalMapper


class APIProvider(Provider):
    api_goal_mapper = provide(APIGoalMapper, scope=Scope.APP)
