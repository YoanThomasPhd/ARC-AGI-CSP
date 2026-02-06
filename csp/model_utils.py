from pychoco import Model
from pychoco.variables.intvar import IntVar

from csp.base_model import ArcModel


def base_model(name: str="BaseModel", size: tuple[int]=(30,30)) -> ArcModel:
    model: Model = Model(name)

    x_in: list[list[IntVar]] = model.intvars(size, 0, 9, name="xin")
    x_out: list[list[IntVar]] = model.intvars(size, 0, 9, name="xout")
    l_in: IntVar = model.intvar(1,30, "l_in")
    l_out: IntVar = model.intvar(1, 30, "l_out")
    L_in: IntVar = model.intvar(1, 30, "L_in")
    L_out: IntVar = model.intvar(1, 30, "L_out")

    return ArcModel(model, x_in, l_in, L_in, x_out, l_out, L_out)

def count_colors(arc_model: ArcModel, with_zero=False) -> None:
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
