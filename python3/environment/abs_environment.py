import abc


class Environment(abc.ABC):
    """Abstract environment class."""

    @abc.abstractmethod
    def s_space(self) -> int:
        """Returns the possible range of states."""
        pass

    @abc.abstractmethod
    def a_space(self) -> int:
        """Returns the possible range of actions."""
        pass

    @abc.abstractmethod
    def s(self) -> int:
        """Returns a state index."""
        pass

    @abc.abstractmethod
    def info(self) -> str:
        """Returns string which describes an internal state."""
        pass

    @abc.abstractmethod
    def r(self) -> float:
        """Returns a reward."""
        pass

    @abc.abstractmethod
    def reset(self):
        """Reset an internal state of the environment."""
        pass

    @abc.abstractmethod
    def run_step(self, a):
        """Update an internal state with an action."""
        pass

    @abc.abstractmethod
    def is_done(self) -> bool:
        """Returns whether the task is done."""
        pass

    @abc.abstractmethod
    def is_success(self) -> bool:
        """Returns whether the task was successful."""
        pass
