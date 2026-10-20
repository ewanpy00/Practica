def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    pending = {}
    dependents = {name: [] for name in packages}

    for name, deps in packages.items():
        known = set(dep for dep in deps if dep in packages)
        pending[name] = len(known)
        for dep in known:
            dependents[dep].append(name)

    wave = sorted(name for name, count in pending.items() if count == 0)
    order = []

    while wave:
        order.extend(wave)
        following = []
        for name in wave:
            for other in dependents[name]:
                pending[other] -= 1
                if pending[other] == 0:
                    following.append(other)
        wave = sorted(following)

    return order if len(order) == len(packages) else []

# print(package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []}))
# print(package_dependency_resolver({"X": ["Y"], "Y": ["X"]}))
# print(package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]}))
