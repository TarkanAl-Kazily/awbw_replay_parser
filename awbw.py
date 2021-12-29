# awbw.py
#
# Classes specific to AWBW

import pdb
import logging
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
    turn_count: int = 0

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
    capture: bool = False
    fired: bool = False
    hit_points: int = 10
    cargo1_units_id: int = 0
    cargo2_units_id: int = 0
    carried: bool = False

class Building(typing.TypedDict, total=False):
    id: int = 0
    capture: int = 20
    # Corresponds to a terrain type, which includes the information about which country owns the building
    # TODO: Reverse lookup the terrain ID to determine which player owns the property
    # TODO: Reverse lookup the terrain ID to determine what type of property this is
    terrain_id: int = 0
    x: int = 0
    y: int = 0
    # Same as player id
    team: int = 0

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
        self.game_map = deepcopy(game_map)

        # Setup game_info as an awbw.GameInfo type
        self.game_info = deepcopy(game_info)

        # Setup players as a dictionary mapping player id -> awbw.Player type
        self.players = deepcopy(players)

        # Setup units as a dictionary mapping unit id -> awbw.Unit type
        self.units = deepcopy(units)

        # TODO: Setup buildings as a dictionary mapping building id -> awbw.Building type
        self.buildings = deepcopy(buildings)

        if replay_initial is not None:
            # Overwrite passed in values with info from the replay
            self._construct_from_replay_initial(replay_initial)

    def _construct_initial_players(self, replay_initial_players):
        """Helper for just the players info"""
        self.players = {}
        for key, player in replay_initial_players.items():
            player_info = {
                "turn_count": 0
            }
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
        first_player = replay_initial_players[0]
        self.players[int(first_player["id"])]["turn_count"] = 1

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
        self.buildings = {}
        for i, building in replay_initial_buildings.items():
            building_info = {}
            building_keys_int = [
                    "id",
                    "capture",
                    "last_capture",
                    "terrain_id",
                    "x",
                    "y",
            ]
            for k in building_keys_int:
                building_info[k] = int(building[k])
            self.buildings[building_info["id"]] = Building(**building_info)

    def _construct_initial_game_info(self, replay_initial):
        """Helper for the global game info"""
        game_info_info = {}
        game_info_info["games_id"] = replay_initial["id"]
        game_info_info["maps_id"] = replay_initial["maps_id"]
        game_info_info["active_player_id"] = replay_initial["players"][0]["id"]
        game_info_info["turn"] = 0
        game_info_info["day"] = 1
        self.game_info = GameInfo(**game_info_info)

    def _construct_from_replay_initial(self, replay_initial):
        """Helper to construct a GameState from an AWBW Replay"""
        self._construct_initial_players(replay_initial["players"])
        self._construct_initial_units(replay_initial["units"])
        self._construct_initial_buildings(replay_initial["buildings"])
        self._construct_initial_game_info(replay_initial)

    def _apply_fire_action(self, action_data):
        """
        Helper for fire actions
        """
        logging.debug("Fire action")

        # Unit info
        # - position change
        move_state = deepcopy(self)
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = move_state._apply_move_action(action_data["Move"])

        fire_action = action_data["Fire"]
        assert isinstance(fire_action, dict)

        # Player info
        # - power meters
        new_player_info = deepcopy(move_state.players)
        for combatant, values in fire_action["copValues"].items():
            p_id = int(values["playerId"])
            # For some reason, the replay data has the co power meter multiplied by a magnitude of 10
            new_player_info[p_id]["co_power"] = int(values["copValue"]) / 10

        # Unit info
        # - ammo change
        # - health change
        new_unit_info = deepcopy(move_state.units)
        for p_id, combatinfo in fire_action["combatInfoVision"].items():
            p_id = int(p_id)
            if not isinstance(combatinfo, dict) or not isinstance(combatinfo["combatInfo"], dict):
                continue
            for role, unit in combatinfo["combatInfo"].items():
                if not isinstance(unit, dict):
                    # Indicates a unseen attacker
                    continue
                u_id = int(unit["units_id"])
                assert u_id in new_unit_info
                new_unit_info[u_id] = new_unit_info[u_id] | {
                        "hit_points": unit["units_hit_points"],
                        "ammo": unit["units_ammo"],
                        "fired": role == "attacker"
                }
        
        return AWBWGameState(
                game_map=self.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_join_action(self, action_data):
        """
        Helper for join actions
        """
        logging.debug("Join action")
        # To join two units, one must be moved
        assert "Move" in action_data
        move_state = self._apply_move_action(action_data["Move"])

        join_action = action_data["Join"]
        # The unit that now has 0 health due to joining
        joined_u_id = None
        for p_id, u_id in join_action["joinID"].items():
            p_id = int(p_id)
            if isinstance(u_id, int):
                joined_u_id = u_id
                break
        assert joined_u_id is not None
        assert joined_u_id in move_state.units
        new_unit_info = deepcopy(move_state.units)
        # Set hit points of old unit to 0 to indicate it no longer exists
        new_unit_info[joined_u_id]["hit_points"] = 0

        # Player info
        # - funds change
        new_player_info = deepcopy(move_state.players)
        for p_id, funds in join_action["newFunds"].items():
            p_id = int(p_id)
            new_player_info[p_id]["funds"] = funds

        # Unit info
        # - ammo change
        # - health change
        unit_info = join_action["unit"]
        for p_id, unit in unit_info.items():
            p_id = int(p_id)
            if not isinstance(unit, dict):
                continue
            if not unit["units_players_id"] == p_id:
                # Not the unit that moved, just another player's view of the unit.
                # Because it's another player's view, it won't have the full unit info
                # in the case where the unit moves back into the fog.
                continue
            u_id = unit["units_id"]
            assert u_id in new_unit_info
            # Overwrite every value for the unit, to be detail oriented.
            # I don't know what the answer is if two APCs carrying units try to join...
            for k in new_unit_info[u_id]:
                new_unit_info[u_id][k] = unit["units_" + k]

        return AWBWGameState(
                game_map=move_state.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    def _apply_resign_action(self, action_data):
        """
        Helper for resign actions
        """
        print("Resign action")
        print("IMPLEMENT ME")
        return deepcopy(self)

    def _apply_move_action(self, action_data):
        """
        Helper for move actions
        """
        logging.debug("Move action")
        new_unit_info = deepcopy(self.units)
        # Unit info
        # - position change
        # - fuel change
        for p_id, unit in action_data["unit"].items():
            p_id = int(p_id)
            if not isinstance(unit, dict):
                continue
            if not unit["units_players_id"] == p_id:
                # Not the unit that moved, just another player's view of the unit.
                # Because it's another player's view, it won't have the full unit info
                # in the case where the unit moves back into the fog.
                continue
            u_id = unit["units_id"]
            assert u_id in new_unit_info
            new_unit_info[u_id] = new_unit_info[u_id] | {
                "x" : unit["units_x"],
                "y": unit["units_y"],
                "moved": True,
                "fuel": unit["units_fuel"]
            }
        
        return AWBWGameState(
                game_map=self.game_map,
                players=self.players,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_build_action(self, action_data):
        """
        Helper for build actions
        """
        logging.debug("Build action")

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
        logging.debug("End action")
        info = action_data["updatedInfo"]
        # GameInfo Info - new active player
        new_global_info = self.game_info | {
            "active_player_id": int(info["nextPId"]),
            "turn": self.game_info["turn"] + 1,
        }

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
        new_player_info[new_global_info["active_player_id"]]["turn_count"] += 1

        # Increment day by using the maximum turn count of all players
        turn_counts = [p["turn_count"] for p in new_player_info.values()]
        new_global_info["day"] = max(turn_counts)

        # Unit info
        # - TODO resupply
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
        # Unmark moved, captured, fired flags
        for u_id, unit in new_unit_info.items():
            unit["moved"] = False
            unit["capture"] = False
            unit["fired"] = False

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
        print("IMPLEMENT ME")
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
        logging.debug("Capt action")
        move_state = self
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = move_state._apply_move_action(action_data["Move"])
        # Unit info
        # - position change
        # - fuel change

        # Building info
        # - capture status
        # - ownership status
        capt_action = action_data["Capt"]
        buildingInfo = capt_action["buildingInfo"]
        b_id = int(buildingInfo["buildings_id"])
        assert b_id in move_state.buildings
        new_building_info = deepcopy(move_state.buildings)
        new_building_info[b_id] = new_building_info[b_id] | {
            "capture": buildingInfo["buildings_capture"],
            "team": buildingInfo["buildings_team"],
        }

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=move_state.units,
                buildings=new_building_info,
                game_info=move_state.game_info)

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
    from replay import AWBWReplay
    with AWBWReplay(sys.argv[1]) as replay:
        state = AWBWGameState(replay_initial=replay.game_info())

        action_number = 0
        print("Press enter to step through the replay")
        for action in replay.actions():
            action = AWBWGameAction(replay_action=action)
            state = state.apply_action(action)
            for p, player in state.players.items():
                print(f"{p}: G {player['funds']}")
            action_number += 1

        action_types = replay.action_summaries()
        print(f"The action types were {set(action_types)}")
