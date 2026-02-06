from dataclasses import dataclass
from itertools import product

import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from pychoco import Model
from pychoco.variables.intvar import IntVar

colorMap: ListedColormap = ListedColormap(["black","blue","red","green","yellow","grey","pink", "orange","cyan","brown"], "arc_color")
HEURISTICS_REGISTRY = {}
def register_heuristic(name=None):
    def decorator(func):
        key = name or func.__name__
        if key in HEURISTICS_REGISTRY:
            raise ValueError(f"Heuristic '{key}' already registered")
        HEURISTICS_REGISTRY[key] = func
        return func
    return decorator

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


def base_model(name: str="BaseModel", size: tuple[int]=(30,30)) -> ArcModel:
    model: Model = Model(name)

    x_in: list[list[IntVar]] = model.intvars(size, 0, 9, name="xin")
    x_out: list[list[IntVar]] = model.intvars(size, 0, 9, name="xout")
    l_in: IntVar = model.intvar(1,30, "l_in")
    l_out: IntVar = model.intvar(1, 30, "l_out")
    L_in: IntVar = model.intvar(1, 30, "L_in")
    L_out: IntVar = model.intvar(1, 30, "L_out")

    return ArcModel(model, x_in, l_in, L_in, x_out, l_out, L_out)

def count_colors(arc_model: ArcModel, with_zero=False):
    m = 1
    if with_zero:
        m = 0
    C = arc_model.model.intvars(9+m, 0, 30*30,"C")
    X = [el for l in arc_model.x_in for el in l]
    for c in range(9+m):
        arc_model.model.count(c+m, X , C[c])
    Cmin_val = arc_model.model.intvar(0, 30*30, "Cmin_val")
    Cmin = arc_model.model.intvar(0, 9, "Cmin")
    arc_model.model.min(Cmin_val, C)
    arc_model.model.element(Cmin_val, C, Cmin)
    Cmax_val = arc_model.model.intvar(0, 30 * 30, "Cmax_val")
    Cmax = arc_model.model.intvar(0, 9, "Cmax")
    arc_model.model.max(Cmax_val, C)
    arc_model.model.element(Cmax_val, C, Cmax)

def data_0a938d79():
    pass

@register_heuristic("23b5c85d")
def data_23b5c85d():
    arc_model: ArcModel = base_model("23b5c85d")

    C = arc_model.model.intvars(9, 0, 30*30,"C")
    C2 = arc_model.model.intvars(9, 0, 30*30,"C")
    var = sum(arc_model.x_in, [])
    for i in range(1, 10):
        bools = []
        for v in var:
            b = arc_model.model.boolvar()
            arc_model.model.arithm(v, "=", i).reify_with(b)
            bools.append(b)

        arc_model.model.sum(bools, "=", C[i-1]).post()
        arc_model.model.if_then_else(
            arc_model.model.arithm(C[i-1], "=", 0),
            arc_model.model.arithm(C2[i-1], "=", 30*30),
            arc_model.model.arithm(C2[i-1], "=", C[i-1])
        )
    arc_model.countVar = arc_model.model.intvar(0, 30*30)
    arc_model.model.min(arc_model.countVar, C2).post()

    Cm = arc_model.model.intvar(0,9,"Cm")
    arc_model.model.element(arc_model.countVar, C, Cm).post()


    arc_model.Z = arc_model.model.intvars(4,0, 29, "Z")
    for i, j in product(range(30), range(30)):
        arc_model.model.if_then_else(
            arc_model.model.arithm(arc_model.x_in[j][i], "=", Cm, "+", 1),
            arc_model.model.and_(
                [
                    arc_model.model.arithm(arc_model.Z[0], "<=", i),
                    arc_model.model.arithm(arc_model.Z[1], ">=", i),
                    arc_model.model.arithm(arc_model.Z[2], "<=", j),
                    arc_model.model.arithm(arc_model.Z[3], ">=", j),
                ]
            ),
            arc_model.model.or_(
                [arc_model.model.arithm(arc_model.Z[0], ">", i),
                arc_model.model.arithm(arc_model.Z[1], "<", i),
                arc_model.model.arithm(arc_model.Z[2], ">", j),
                arc_model.model.arithm(arc_model.Z[3], "<", j),]
            )

        )

        arc_model.model.if_then_else(
            arc_model.model.and_(
                [
                    arc_model.model.arithm(arc_model.l_out, ">", i),
                    arc_model.model.arithm(arc_model.L_out, ">", j),
                ]
            ),
            arc_model.model.arithm(arc_model.x_out[j][i], "=", Cm, "+", 1),
            arc_model.model.arithm(arc_model.x_out[j][i], "=", 0),
        )

    l = arc_model.model.intvar(0,30)
    L = arc_model.model.intvar(0,30)
    arc_model.model.arithm(l,"=", arc_model.Z[1], "-", arc_model.Z[0]).post()
    arc_model.model.arithm(L,"=", arc_model.Z[3], "-", arc_model.Z[2]).post()
    arc_model.model.arithm(arc_model.l_out,"=", l, "+", 1).post()
    arc_model.model.arithm(arc_model.L_out,"=", L, "+", 1).post()


    return arc_model

@register_heuristic("e9afcf9a")
def data_e9afcf9a():
    arc_model: ArcModel = base_model("e9afcf9a")

    model = arc_model.model
    model.arithm(arc_model.L_out,"=",arc_model.L_in).post()
    model.arithm(arc_model.l_out,"=",arc_model.l_in).post()
    for i in range(30):
        model.if_then_else(
            model.arithm(arc_model.l_out, "<=", i),
            model.arithm(arc_model.x_out[0][i], "=", 0),
            model.arithm(arc_model.x_out[0][i], "=", arc_model.x_in[i%2][i]),
        )
        model.if_then_else(
            model.arithm(arc_model.l_out, "<=", i),
            model.arithm(arc_model.x_out[1][i], "=", 0),
            model.arithm(arc_model.x_out[1][i], "=", arc_model.x_in[(i+1) % 2][i]),
        )
    return arc_model

@register_heuristic("a85d4709")
def data_a85d4709():
    arc_model: ArcModel = base_model("a85d4709")

    model = arc_model.model
    model.arithm(arc_model.L_out,"=",arc_model.L_in).post()
    model.arithm(arc_model.l_out,"=",arc_model.l_in).post()
    for i in range(3):
        model.if_then(
            model.arithm(arc_model.x_in[i][0], "=", 5),
            model.and_(
                [model.arithm(arc_model.x_out[i][j], "=", 2) for j in range(3)]
            )
        )
        model.if_then(
            model.arithm(arc_model.x_in[i][1], "=", 5),
            model.and_(
                [model.arithm(arc_model.x_out[i][j], "=", 4) for j in range(3)]
            )
        )
        model.if_then(
            model.arithm(arc_model.x_in[i][2], "=", 5),
            model.and_(
                [model.arithm(arc_model.x_out[i][j], "=", 3) for j in range(3)]
            )
        )

    # for i,j in product(range(3,30),range(3,30)):
    #     model.arithm(arc_model.x_out[i][j],"=",0).post()
    return arc_model

@register_heuristic("810b9b61")
def data_810b9b61():
    arc_model: ArcModel = base_model("810b9b61")
    model = arc_model.model

    model.arithm(arc_model.L_out,"=",arc_model.L_in).post()
    model.arithm(arc_model.l_out,"=",arc_model.l_in).post()
    Z = model.intvars((30,30),0,3,"Z")

    delta = [(0,1),(1,0),(-1,0),(0,-1)]
    C = model.intvars((30,30),0,9 ,"C")
    for i,j in product(range(30),range(30)):
        model.if_then(
            model.or_(
                [
                    model.arithm(arc_model.L_out, "<=", i),
                    model.arithm(arc_model.l_out, "<=", j),
                ]
            ),
            model.arithm(arc_model.x_out[j][i],"=", 0)
        )

        # model.count(1, [arc_model.x_in[j+dj][i+di] for di,dj in delta if 0<=i+di<30 and 0<=j+dj<30], Z[j][i]).post()

        model.if_then_else(
            model.arithm(arc_model.x_in[j][i], "=", 1),
            model.arithm(C[j][i], ">", 0),
            model.arithm(C[j][i], "=", 0),
        )

        # model.if_then_else(
        #     model.arithm(arc_model.x_in[j][i], "=", 0),
        #     model.arithm(arc_model.x_out[j][i], "=", 0),
        #     model.arithm(arc_model.x_out[j][i], ">", 0),
        # )

        model.arithm(arc_model.x_out[j][i], "=", C[j][i]).post()

        for ip, jp in product(range(30), range(30)):
            if abs(i-ip) + abs(j-jp) == 1:
                model.if_then(
                    model.and_([
                        model.arithm(arc_model.x_in[j][i], "=", 1),
                        model.arithm(arc_model.x_in[jp][ip], "=", 1),
                    ]),
                    model.arithm(C[jp][ip], "=", C[j][i])
                )
            elif i!=ip and j!=ip:
                model.if_then(
                    model.and_([
                        model.arithm(arc_model.x_in[j][i], "=", 1),
                        model.arithm(arc_model.x_in[jp][ip], "=", 1),
                    ]),
                    model.arithm(C[jp][ip], "!=", C[j][i])
                )
    return arc_model

@register_heuristic("2dc579da")
def data_2dc579da():
    arc_model: ArcModel = base_model("2dc579da")
    model = arc_model.model

    model.arithm(arc_model.L_out, "=", arc_model.L_in, "*", 2).post()
    model.arithm(arc_model.l_out, "=", arc_model.l_in, "*", 2).post()
    count_colors(arc_model)

    Y = model.intvars((30,30, 2),0,30,"Y")
    for i,j in product(range(30),range(30)):
        model.if_then(
            model.arithm(arc_model.l_in, ">", i),
            model.arithm(Y[i][j][0], "=", i)
        )
        model.if_then(
            model.and_(
                [
                    model.arithm(arc_model.l_in, ">", i),
                    model.arithm(arc_model.l_out, "<", i, "+", 1),
                ]
            ),
            model.arithm(Y[i][j][0], "+", arc_model.l_in,"=", i)
        )
        arc_model.model.if_then(
            model.and_([
                model.arithm(arc_model.l_in, ">", i),
                model.arithm(arc_model.L_in, ">", j),
            ]),
        )
    return  arc_model