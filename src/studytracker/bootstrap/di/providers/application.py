from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents, provide, provide_all

from studytracker.application.commands.create_goal import CreateGoalHandler, CreateGoalRequest
from studytracker.application.commands.create_subgoal import CreateSubgoalHandler, CreateSubgoalRequest
from studytracker.application.commands.delete_goal import DeleteGoalHandler, DeleteGoalRequest
from studytracker.application.commands.update_goal import UpdateGoalHandler, UpdateGoalRequest
from studytracker.application.queries.get_goal import GetGoalHandler, GetGoalRequest


class ApplicationProvider(Provider):
    handlers = provide_all(
        CreateGoalHandler,
        CreateSubgoalHandler,
        GetGoalHandler,
        DeleteGoalHandler,
        UpdateGoalHandler,
        scope=Scope.REQUEST,
    )

    resolver = provide(WithParents[DishkaResolver], scope=Scope.REQUEST)
    dispatcher = provide(WithParents[Dispatcher], scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(CreateGoalRequest, CreateGoalHandler)
        registry.add_request_handler(CreateSubgoalRequest, CreateSubgoalHandler)
        registry.add_request_handler(GetGoalRequest, GetGoalHandler)
        registry.add_request_handler(UpdateGoalRequest, UpdateGoalHandler)
        registry.add_request_handler(DeleteGoalRequest, DeleteGoalHandler)

        return registry
