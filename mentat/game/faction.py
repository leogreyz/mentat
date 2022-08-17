from .resources import Resources

class Faction:
    def __init__(self, id='0', name=None, emoji=None, info_channel_name=None, state=None, state_version=None):
        if state is None:
            self.id = id
            self.name = name
            self.emoji = emoji
            self.info_channel_name = info_channel_name
            self.resources = Resources()
        else:
            self.deserialize(state, state_version)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'emoji': self.emoji,
            'info_channel_name': self.info_channel_name,
            'resources': self.resources.serialize()
        }

    def deserialize(self, state, version):
        self.id = state['id']
        self.name = state['name']
        self.emoji = state['emoji']
        self.info_channel_name = state['info_channel_name']
        self.resources = Resources(state=state['resources'], state_version=version)