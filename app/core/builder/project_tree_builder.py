def generate_project_tree_from_paths(paths):
    tree = {}
    for path in paths:
        parts = path.split("/")
        current = tree
        for part in parts:
            current = current.setdefault(part, {})
    return tree