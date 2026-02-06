from matplotlib.colors import ListedColormap

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