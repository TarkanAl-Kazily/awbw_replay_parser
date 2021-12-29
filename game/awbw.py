# awbw.py
#
# Classes specific to AWBW

import pdb
from enum import Enum
from copy import deepcopy
import typing
import game

class GameInfo(typing.TypedDict, total=False):
    games_id: int = 0
    active_player_id: int = 0
    maps_id: int = 0
    turn: int = 0
    day: int = 0

class Player(typing.TypedDict, total=False):
    id: int = 0
    team: int = 0
    users_id: int = 0
    countries_id: int = 0
    co_id: int = 0
    co_max_power: int = 0
    co_max_spower: int = 0
    co_power: int = 0
    co_power_on: bool = False
    eliminated: bool = False
    funds: int = 0

class Unit(typing.TypedDict, total=False):
    id: int = 0
    players_id: int = 0
    name: str = "Unit"
    movement_points: int = 0
    vision: int = 0
    fuel: int = 0
    fuel_per_turn: int = 0
    sub_dive: bool = False
    ammo: int = 0
    short_range: int = 0
    long_range: int = 0
    second_weapon: bool = False
    symbol: str = "U"
    cost: int = 0
    movement_type: str = "F"
    x: int = 0
    y: int = 0
    moved: bool = False
    capture: int = 0
    fired: int = 0
    hit_points: int = 0
    cargo1_units_id: int = 0
    cargo2_units_id: int = 0
    carried: bool = False

class Building(typing.TypedDict, total=False):
    id: int = 0

# Derived classes for AWBW

class AWBWGameAction(game.GameAction):
    """
    Represents a single action in the AWBW game.
    """

    class Type(Enum):
        Fire = "Fire"
        Join = "Join"
        Resign = "Resign"
        Move = "Move"
        Build = "Build"
        End = "End"
        Power = "Power"
        Capt = "Capt"

    def __init__(self, replay_action):
        super().__init__()

        self.type = self.Type[replay_action["action"]]
        self.info = replay_action


class AWBWGameState(game.GameState):
    """
    Represents a single state in the AWBW game.
    """

    def __init__(self,
            game_map=None,
            players=None,
            units=None,
            buildings=None,
            game_info=None,
            replay_initial=None):
        super().__init__()

        # TODO: Setup game map - assume this never changes
        self.game_map = game_map

        # Setup game_info as an awbw.GameInfo type
        self.game_info = game_info

        # Setup players as a dictionary mapping player id -> awbw.Player type
        self.players = players

        # Setup units as a dictionary mapping unit id -> awbw.Unit type
        self.units = units

        # TODO: Setup buildings as a dictionary mapping building id -> awbw.Building type
        self.buildings = buildings

        if replay_initial is not None:
            # Overwrite passed in values with info from the replay
            self._construct_from_replay_initial(replay_initial)

    def _construct_initial_players(self, replay_initial_players):
        """Helper for just the players info"""
        self.players = {}
        for key, player in replay_initial_players.items():
            player_info = {}
            player_keys_int = [
                    "id",
                    "funds",
                    "users_id",
                    "countries_id",
                    "co_id",
                    "co_max_power",
                    "co_max_spower",
                    "co_power",
                    "team"
            ]
            for k in player_keys_int:
                player_info[k] = int(player[k])

            player_keys_bool = ["co_power_on", "eliminated"]
            for k in player_keys_bool:
                player_info[k] = (player[k] == "Y")

            self.players[player_info["id"]] = Player(**player_info)

    def _construct_initial_units(self, replay_initial_units):
        """Helper for just the unit info"""
        self.units = {}
        for key, unit in replay_initial_units.items():
            unit_info = {}
            self.units[unit["id"]] = unit_info
            unit_keys_int = [
                    "id",
                    "players_id",
                    "fuel",
                    "fuel_per_turn",
                    "ammo",
                    "cost",
                    "x",
                    "y",
                    "hit_points"
            ]
            unit_keys_str = ["name", "symbol", "movement_type"]
            for k in unit_keys_int:
                unit_info[k] = int(unit[k])
            self.units[unit_info["id"]] = Unit(**unit_info)

    def _construct_initial_buildings(self, replay_initial_buildings):
        """Helper for just the building info"""
        pass

    def _construct_initial_game_info(self, replay_initial):
        """Helper for the global game info"""
        game_info_info = {}
        game_info_info["games_id"] = replay_initial["id"]
        game_info_info["maps_id"] = replay_initial["maps_id"]
        game_info_info["active_player_id"] = replay_initial["players"][0]["id"]
        game_info_info["turn"] = 0
        game_info_info["day"] = 0
        self.game_info = GameInfo(**game_info_info)

    def _construct_from_replay_initial(self, replay_initial):
        """Helper to construct a GameState from an AWBW Replay"""
        self._construct_initial_players(replay_initial["players"])
        self._construct_initial_units(replay_initial["units"])
        # TODO
        self.buildings = {}
        self._construct_initial_game_info(replay_initial)

    def _apply_fire_action(self, action_data):
        """
        Helper for fire actions
        """
        print("Fire action")
        # Player info
        # - power meters
        # - value change

        # Unit info
        # - ammo change
        # - health change
        # - position change
        return deepcopy(self)

    def _apply_join_action(self, action_data):
        """
        Helper for join actions
        """
        print("Join action")
        # Player info
        # - value change
        # - funds change

        # Unit info
        # - ammo change
        # - health change
        return deepcopy(self)

    def _apply_resign_action(self, action_data):
        """
        Helper for resign actions
        """
        print("Resign action")
        return deepcopy(self)

    def _apply_move_action(self, action_data):
        """
        Helper for move actions
        """
        print("Move action")
        # Unit info
        # - position change
        # - fuel change
        return deepcopy(self)

    def _apply_build_action(self, action_data):
        """
        Helper for build actions
        """
        print("Build action")

        info = action_data["newUnit"]
        # Unit info
        # - new unit
        built_unit = {}
        for k, unit in info.items():
            unit_keys_int = [
                    "id",
                    "players_id",
                    "fuel",
                    "fuel_per_turn",
                    "ammo",
                    "cost",
                    "x",
                    "y",
                    "hit_points"
            ]
            prefix = "units_"
            unit_keys_str = ["name", "symbol", "movement_type"]
            for k in unit_keys_int:
                built_unit[k] = unit[prefix + k]
            for k in unit_keys_str:
                built_unit[k] = unit[prefix + k]
            new_unit_info = deepcopy(self.units) | {built_unit["id"] : Unit(**built_unit)}

        # Player info
        # - funds change
        new_player_info = deepcopy(self.players)
        p_id = built_unit["players_id"]
        new_player_info[p_id]["funds"] -= built_unit["cost"]

        return AWBWGameState(
                game_map=self.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_end_action(self, action_data):
        """
        Helper for end actions
        """
        print("End action")
        info = action_data["updatedInfo"]
        # GameInfo Info - new active player
        new_global_info = self.game_info | {
            "active_player_id": int(info["nextPId"]),
            "turn": self.game_info["turn"] + 1,
        }
        # TODO: Increment day

        # Player info
        # - funds change
        new_player_info = {}
        funds_info = info["nextFunds"]
        for k, v in funds_info.items():
            p_id = int(k)
            if isinstance(v, int):
                new_player_info[p_id] = self.players[p_id] | {"funds": v}
            else:
                new_player_info[p_id] = self.players[p_id]

        # Unit info
        # - resupply
        # - fuel cost
        # - sank / crashed units
        new_unit_info = deepcopy(self.units)
        repaired_info = info["repaired"]
        for k, v in repaired_info.items():
            p_id = int(k)
            assert isinstance(v, list)
            for unit in v:
                u_id = int(unit["units_id"])
                assert u_id in new_unit_info
                new_unit_info[u_id] = new_unit_info[u_id] | {"hit_points" : unit["units_hit_points"]}

        return AWBWGameState(
                game_map=self.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=new_global_info)

    def _apply_power_action(self, action_data):
        """
        Helper for power actions
        """
        print("Power action")
        # Player info
        # - power status
        # - funds change
        # - value change
        # - power meter change

        # Unit info
        # - health change
        # - ammo change
        # - fuel change
        # - new unit(s)
        return deepcopy(self)

    def _apply_capt_action(self, action_data):
        """
        Helper for capt actions
        """
        print("Capt action")
        # Building info
        # - capture status
        # - ownership status

        # Unit info
        # - position change
        # - fuel change
        return deepcopy(self)

    _ACTION_TYPE_TO_APPLY_FUNC = {
            AWBWGameAction.Type.Fire : _apply_fire_action,
            AWBWGameAction.Type.Join : _apply_join_action,
            AWBWGameAction.Type.Resign : _apply_resign_action,
            AWBWGameAction.Type.Move : _apply_move_action,
            AWBWGameAction.Type.Build : _apply_build_action,
            AWBWGameAction.Type.End : _apply_end_action,
            AWBWGameAction.Type.Power : _apply_power_action,
            AWBWGameAction.Type.Capt : _apply_capt_action,
            }

    def apply_action(self, action):
        return self._ACTION_TYPE_TO_APPLY_FUNC[action.type](self, action.info)

    def _unused_merge_info(self, action):
        # TODO cleanup and delete
        new_players = deepcopy(self.players)
        # Overwrite all existing player info
        for player_id, player in action.players().items():
            assert player_id in new_players
            for k, v in player.items():
                new_players[player_id][k] = v

        new_units = deepcopy(self.units)
        # Overwrite all existing units
        for unit_id, unit in new_units.items():
            if unit_id in action.units():
                new_units[unit_id] = unit | action.units()[unit_id]
        # Add all new units
        for unit_id, unit in action.units().items():
            if not unit_id in new_units:
                new_units[unit_id] = unit

        new_buildings = deepcopy(self.buildings)
        for building_id, building in action.buildings().items():
            assert building_id in new_buildings
            for k, v in building.items():
                new_buildings[building_id][k] = v

        new_game_info = deepcopy(self.game_info)
        new_game_info = new_game_info | action.game_info()

        return AWBWGameState(
                game_info=new_game_info,
                players=new_players,
                units=new_units,
                buildings=new_buildings)

if __name__ == "__main__":
    import sys, os, pprint
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    from replay.replay import ReplayFile, Replay
    with ReplayFile(sys.argv[1]) as replayfile:
        r = Replay(replayfile)

        state = AWBWGameState(replay_initial=r.game_info())

        print("Press enter to step through the replay")
        for action in r.actions():
            action = AWBWGameAction(replay_action=action)
            state = state.apply_action(action)
            for p, player in state.players.items():
                print(f"{p}: G {player['funds']}")

        action_types = r.action_summaries()
        print(f"The action types were {set(action_types)}")
