from typing import Any, Callable


class Mediator:
    def __init__(self):
        self._handlers: dict = {}
        self._behaviours: list = []

    def register_handler(self, command_type: type, handler: Any) -> None:
        self._handlers[command_type] = handler

    def register_behaviour(self, behaviour: Any) -> None:
        self._behaviours.append(behaviour)

    def send(self, command: Any) -> Any:
        handler = self._handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler registered for {type(command).__name__}")

        def execute() -> Any:
            return handler.handle(command)

        pipeline: Callable = execute
        for behaviour in reversed(self._behaviours):
            def make_next(current_pipeline, current_behaviour):
                def next_fn():
                    return current_behaviour.handle(command, current_pipeline)
                return next_fn
            pipeline = make_next(pipeline, behaviour)

        return pipeline()
