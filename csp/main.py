from csp.check_model import check1
from csp.model_utils import base_model
from csp.utils import HEURISTICS_REGISTRY


def main():
    for model in HEURISTICS_REGISTRY.keys():
        print(f"{model} done : {check1(model)}")


if __name__ == '__main__':
    main()