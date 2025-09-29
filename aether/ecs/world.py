from .entity import EntityId


class World:
    """Holds entities, components, and systems; runs update loop."""

    def __init__(self):
        self._next_id = 1
        self.components = {}  # {ComponentClass: {entity: component}}
        self.systems = []

    def create(self) -> EntityId:
        eid = EntityId(self._next_id)
        self._next_id += 1
        return eid

    def add(self, entity: EntityId, component):
        self.components.setdefault(type(component), {})[entity] = component

    def get(self, entity: EntityId, comp_cls):
        return self.components.get(comp_cls, {}).get(entity)

    def query(self, *comp_classes):
        stores = [self.components.get(c, {}) for c in comp_classes]
        if not stores:
            return
        common = set(stores[0].keys())
        for s in stores[1:]:
            common &= set(s.keys())
        for e in common:
            yield (e, *[s[e] for s in stores])

    def add_system(self, system):
        self.systems.append(system)
        self.systems.sort(key=lambda s: getattr(s, 'priority', 0))

    def update(self, dt: float):
        for sys in self.systems:
            sys.update(dt)


