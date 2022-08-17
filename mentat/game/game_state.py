from .faction import Faction
from .resources import Resources

class GameState:
    def __init__(self):
        self.game_resources = Resources()
        self.factions = {}

    def register_faction(self, id, name, emoji=None, info_channel_name=None):
        if id in self.factions:
            raise

        self.factions[id] = Faction(id, name, emoji, info_channel_name)

    def register_game_resource(self, name, starting_value=0, type='num'):
        self.game_resources.register_resource(name, starting_value, type)

    def register_faction_resource(self, faction_id, resource_name, starting_value=0, type='num'):
        self.factions[faction_id].resources.register_resource(resource_name, starting_value, type)

    def add_to_resource(self, resource_name, add_num):
        self.game_resources.add(resource_name, add_num)
        return self.get_resource(resource_name)

    def add_to_faction_resource(self, faction_id, resource_name, add_num):
        self.factions[faction_id].resources.add(resource_name, add_num)
        return self.get_faction_resource(faction_id, resource_name)

    def get_resource(self, resource_name):
        return self.game_resources.get(resource_name)

    def get_faction_resource(self, faction_id, resource_name):
        return self.factions[faction_id].resources.get(resource_name)

    def serialize(self):
        return {
            'factions': { k: v.serialize() for (k, v) in self.factions.items() },
            'game_resources': self.game_resources.serialize()
        }

    def deserialize(self, state, version):
        self.game_resources = Resources(state=state['game_resources'], state_version=version)

        self.factions = { k: Faction(state=v, state_version=version) for (k, v) in state['factions'].items() }
        
    