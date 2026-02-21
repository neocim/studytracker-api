from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents, provide

from studytracker.application.commands.create_goal import CreateGoalHandler, CreateGoalRequest


class ApplicationProvider(Provider):
    resolver = provide(WithParents[DishkaResolver])
    dispatcher = provide(WithParents[Dispatcher])

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(CreateGoalRequest, CreateGoalHandler)

        return registry
