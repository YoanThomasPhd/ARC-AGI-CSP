from dataclasses import dataclass
from itertools import product

import numpy as np
from matplotlib.colors import BoundaryNorm
from pychoco import Model
from pychoco.variables.intvar import IntVar

from csp.utils import colorMap


@dataclass
class ArcModel:
    model: Model
    x_in: list[list[IntVar]]
    l_in: IntVar
    L_in: IntVar

    x_out: list[list[IntVar]]
    l_out: IntVar
    L_out: IntVar

    def init_problem(self, x_val:list[list[int]]) -> None:
        L_val, l_val = len(x_val), len(x_val[0])

        self.model.arithm(self.l_in, "=", l_val).post()
        self.model.arithm(self.L_in, "=", L_val).post()

        for i,j in product(range(30), range(30)):
            if i >= l_val or j >= L_val:
                self.model.arithm(self.x_in[j][i],"=", 0).post()
            else:
                self.model.arithm(self.x_in[j][i],"=", x_val[j][i]).post()

    def solve(self) -> bool:
        return self.model.get_solver().solve()

    def solution_count(self) -> int:
        return len(self.model.get_solver().find_all_solutions())

    def check_solution(self, x_val:list[list[int]]) -> bool:
        if self.model.get_solver().get_solution_count() == 0:
            raise Exception("Aucune solution")

        L_val, l_val = len(x_val), len(x_val[0])

        if self.l_out.get_value() != l_val:
            print(self.l_out.get_value(), l_val)
            return False

        if self.L_out.get_value() != L_val:
            print(self.L_out.get_value() != L_val)
            return False

        for i,j in product(range(30), range(30)):
            if i >= l_val or j >= L_val:
                if self.x_out[j][i].get_value() != 0:
                    print(f"{i=},{j=},{self.x_out[j][i].get_value()}, 0")
                    return False
            else:
                if self.x_out[j][i].get_value() != x_val[j][i]:
                    print(f"{i=},{j=},{self.x_out[j][i].get_value()}, {x_val[j][i]}")
                    return False
        return True

    def show(self):
        if not self.L_in.is_instantiated():
            self.model.get_solver().solve()

        import matplotlib.pyplot as plt
        norm = BoundaryNorm(boundaries=range(11), ncolors=10)
        fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(6, 3))
        data_input = [[self.x_in[j][i].get_value()
                       for i in range(self.l_in.get_value())]
                      for j in range(self.L_in.get_value())]
        ax1.imshow(data_input, cmap=colorMap, norm=norm)
        ax1.tick_params(
            left=False, bottom=False,
            labelleft=False, labelbottom=False
        )
        ax1.set_xticks(np.arange(-0.5, self.l_in.get_value(), 1))
        ax1.set_yticks(np.arange(-0.5, self.L_in.get_value(), 1))
        ax1.grid(True, color="lightgrey", linewidth=0.2)

        data_output = [[self.x_out[j][i].get_value()
                        for i in range(self.l_out.get_value())]
                       for j in range(self.L_out.get_value())]
        ax2.imshow(data_output, cmap=colorMap, norm=norm)
        ax2.tick_params(
            left=False, bottom=False,
            labelleft=False, labelbottom=False
        )
        ax2.set_xticks(np.arange(-0.5, self.l_out.get_value(), 1))
        ax2.set_yticks(np.arange(-0.5, self.L_out.get_value(), 1))
        ax2.grid(True, color="lightgrey", linewidth=0.2)
        plt.show()

