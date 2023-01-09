from base_task import BaseTask
from math_helper.graph import flow_network


class Task8(BaseTask):
    def _solve(self) -> None:
        g = flow_network('A', 'N')


def solve() -> None:
    Task8(8).solve()


if __name__ == '__main__':
    solve()
