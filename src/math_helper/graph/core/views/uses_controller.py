class UsesController:

    _gc: 'GraphController' = None

    def use_controller(self, controller: 'GraphController') -> None:
        self._gc = controller
