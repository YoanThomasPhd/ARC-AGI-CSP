import json
from pprint import pprint

from pychoco import Model
from triton.runtime import Heuristics

from csp.models import HEURISTICS_REGISTRY


def check1(name_file: str, show=False) -> bool:
    if name_file not in HEURISTICS_REGISTRY:
        print("Heuristics not registered")
        return False
    model_gen = lambda : HEURISTICS_REGISTRY[name_file]()

    with open(f"../data/training/{name_file}.json") as json_file:
        data = json.load(json_file)

    good = True
    for train in data["train"]:
        model = model_gen()
        model.init_problem(train["input"])
        model.solve()
        good &= model.check_solution(train["output"])
        if show:
            model.show()

    for test in data["test"]:
        model = model_gen()
        model.init_problem(test["input"])
        model.solve()
        good &= model.check_solution(test["output"])
        if show:
            model.show()

    return good

def main():
    # print("23b5c85d", check1("23b5c85d", show=False))
    # print("e9afcf9a", check1("e9afcf9a", show=False))
    # print("a85d4709", check1("a85d4709", show=False))
    # print("810b9b61", check1("810b9b61", show=True))
    print("2dc579da", check1("2dc579da", show=True))



if __name__ == '__main__':
    main()
