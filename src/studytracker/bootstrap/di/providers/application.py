from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents, provide, provide_all

from studytracker.application.commands.create_goal import CreateGoalHandler, CreateGoalRequest
from studytracker.application.commands.delete_goal import DeleteGoalHandler, DeleteGoalRequest
from studytracker.application.queries.get_goal import GetGoalHandler, GetGoalRequest


class ApplicationProvider(Provider):
    handlers = provide_all(CreateGoalHandler, GetGoalHandler, DeleteGoalHandler, scope=Scope.REQUEST)

    resolver = provide(WithParents[DishkaResolver], scope=Scope.REQUEST)
    dispatcher = provide(WithParents[Dispatcher], scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(CreateGoalRequest, CreateGoalHandler)
        registry.add_request_handler(GetGoalRequest, GetGoalHandler)
        registry.add_request_handler(DeleteGoalRequest, DeleteGoalHandler)

        return registry
