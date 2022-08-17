class Resources:
    resources = {}
    def __init__(self, state=None, state_version=None) -> None:
        if state is not None:
            self.deserialize(state, state_version)

    def register_resource(self, name=None, starting_value=0, type='num'):
        if name in self.resources:
            raise

        if type != 'num':
            raise

        self.resources[name] = starting_value

    def get(self, name):
        return self.resources[name]

    def add(self, name, add_num):
        self.resources[name] += add_num

    def serialize(self):
        resources = self.resources
        return resources

    def deserialize(self, state, version):
        self.resources = { k: v for (k, v) in state.items() }
