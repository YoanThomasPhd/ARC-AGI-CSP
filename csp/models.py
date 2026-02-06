from itertools import product

from csp.base_model import ArcModel
from csp.model_utils import base_model, count_colors
from csp.utils import register_heuristic

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