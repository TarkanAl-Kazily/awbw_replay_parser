"""Classes specific to AWBW Game States and Actions"""

import logging
from enum import Enum
from copy import deepcopy

from awbw_replay import game

class GameInfo(game.DefaultDict):
    """Stores general information about the game"""

    ALLOWED_DATA = {
        "games_id": 0,
        "active_player_id": 0,
        "maps_id": 0,
        "turn": 0,
        "day": 0,
        "game_over": False,
    }

class Player(game.DefaultDict):
    """Stores per player information."""

    ALLOWED_DATA = {
        "id": 0,
        "team": "",
        "users_id": 0,
        "countries_id": 0,
        "co_id": 0,
        "co_max_power": 0,
        "co_max_spower": 0,
        "co_power": 0,
        "co_power_on": False,
        "super_co_power_on": False,
        "eliminated": False,
        "funds": 0,
    }

class Unit(game.DefaultDict):
    """Stores per unit information."""

    ALLOWED_DATA = {
        "id": 0,
        "players_id": 0,
        "name": "Unit",
        "movement_points": 0,
        "vision": 0,
        "fuel": 0,
        "fuel_per_turn": 0,
        "sub_dive": False,
        "ammo": 0,
        "short_range": 0,
        "long_range": 0,
        "second_weapon": False,
        "symbol": "U",
        "cost": 0,
        "movement_type": "F",
        "x": 0,
        "y": 0,
        "moved": False,
        "capture": False,
        "fired": False,
        "hit_points": 10,
        "cargo1_units_id": 0,
        "cargo2_units_id": 0,
        "carried": False,
    }

class Building(game.DefaultDict):
    """Stores per building information."""

    ALLOWED_DATA = {
        "id": 0,
        "last_capture": 20,
        "capture": 20,
        # Corresponds to a terrain type, which includes the information about which
        # country owns the building.
        # TODO": Reverse lookup the terrain ID to determine which player owns the property
        # TODO": Reverse lookup the terrain ID to determine what type of property this is
        "terrain_id": 0,
        "x": 0,
        "y": 0,
        "players_id": 0,
        # Only used in team battles
        "team": "",
    }

# Derived classes for AWBW

class AWBWGameAction(game.GameAction):
    """
    Represents a single action in the AWBW game.
    """

    class Type(Enum):
        """Possible AWBW action types."""
        FIRE = "Fire"
        JOIN = "Join"
        RESIGN = "Resign"
        MOVE = "Move"
        BUILD = "Build"
        END = "End"
        POWER = "Power"
        CAPT = "Capt"
        LOAD = "Load"
        UNLOAD = "Unload"
        REPAIR = "Repair"
        SUPPLY = "Supply"
        DELETE = "Delete"
        HIDE = "Hide"
        UNHIDE = "Unhide"

    def __init__(self, replay_action):
        super().__init__()

        self.type = self.Type(replay_action["action"])
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
        is_team = False
        for player in replay_initial_players.values():
            player_info = {
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
            ]
            for k in player_keys_int:
                player_info[k] = int(player[k])

            player_keys_bool = ["co_power_on", "eliminated"]
            for k in player_keys_bool:
                player_info[k] = (player[k] == "Y")
            player_info["team"] = player["team"]
            if "A" in player_info["team"] or "B" in player_info["team"]:
                is_team = True
            self.players[player_info["id"]] = Player(**player_info)

        # TODO: Support team battles
        if is_team:
            logging.warning("Team battles not supported")

        first_player = replay_initial_players[0]

    def _construct_initial_units(self, replay_initial_units):
        """Helper for just the unit info"""
        self.units = {}
        for unit in replay_initial_units.values():
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
            for k in unit_keys_str:
                unit_info[k] = unit[k]
            self.units[unit_info["id"]] = Unit(**unit_info)

    def _construct_initial_buildings(self, replay_initial_buildings):
        """Helper for just the building info"""
        self.buildings = {}
        for building in replay_initial_buildings.values():
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
        move_state = self
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = self._apply_move_action(action_data["Move"])

        fire_action = action_data["Fire"]
        assert isinstance(fire_action, dict)

        # Player info
        # - power meters
        new_player_info = deepcopy(move_state.players)
        for values in fire_action["copValues"].values():
            p_id = int(values["playerId"])
            # For some reason, the replay data has the co power meter multiplied
            # by a magnitude of 10.
            new_player_info[p_id]["co_power"] = int(values["copValue"]) / 10

        # Handle funds change in the case of Sasha's power
        gained_funds = {}

        # Unit info
        # - ammo change
        # - health change
        new_unit_info = deepcopy(move_state.units)
        for combatinfo in fire_action["combatInfoVision"].values():
            if not isinstance(combatinfo, dict) or not isinstance(combatinfo["combatInfo"], dict):
                continue
            for role in ["attacker", "defender"]:
                if role in combatinfo["combatInfo"]:
                    unit = combatinfo["combatInfo"][role]
                    if not isinstance(unit, dict):
                        # Indicates a unseen attacker
                        continue
                    u_id = int(unit["units_id"])
                    assert u_id in new_unit_info
                    updated_unit_data = {
                        "hit_points": unit["units_hit_points"],
                        "ammo": unit["units_ammo"],
                        "fired": role == "attacker",
                    }
                    new_unit_info[u_id] = {
                        **new_unit_info[u_id],
                        **updated_unit_data,
                    }
            if "gainedFunds" in combatinfo["combatInfo"]:
                fundsinfo = combatinfo["combatInfo"]["gainedFunds"]
                for p_id, funds in fundsinfo.items():
                    p_id = int(p_id)
                    if funds is not None:
                        gained_funds[p_id] = funds

        for p_id, funds in gained_funds.items():
            new_player_info[p_id]["funds"] += funds

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
        for u_id in join_action["joinID"].values():
            if isinstance(u_id, int):
                joined_u_id = u_id
                break
        assert joined_u_id is not None
        assert joined_u_id in move_state.units
        new_unit_info = deepcopy(move_state.units)
        # Set hit points of old unit to 0 to indicate it no longer exists
        new_unit_info[joined_u_id]["hit_points"] = 0
        p_id = new_unit_info[joined_u_id]["players_id"]

        # Player info
        # - funds change
        new_player_info = deepcopy(move_state.players)
        for funds in join_action["newFunds"].values():
            if isinstance(funds, int):
                new_player_info[p_id]["funds"] = funds
                break

        # Unit info
        # - ammo change
        # - health change
        unit_info = join_action["unit"]
        for unit in unit_info.values():
            if not isinstance(unit, dict):
                continue
            if "units_x" not in unit or "units_y" not in unit:
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
        logging.debug("Resign action")
        new_game_info = self.game_info
        if "GameOver" in action_data:
            new_game_info = deepcopy(self.game_info)
            new_game_info["game_over"] = True

        new_player_info = deepcopy(self.players)
        p_id = action_data["Resign"]["playerId"]
        new_player_info[p_id]["eliminated"] = True

        # TODO: The GameOver / Resign messages actual contain usernames.

        return AWBWGameState(
                game_map=self.game_map,
                players=new_player_info,
                units=self.units,
                buildings=self.buildings,
                game_info=new_game_info)

    def _apply_move_action(self, action_data):
        """
        Helper for move actions
        """
        logging.debug("Move action")
        new_unit_info = deepcopy(self.units)
        # Unit info
        # - position change
        # - fuel change
        for unit in action_data["unit"].values():
            if not isinstance(unit, dict):
                continue
            if not "units_x" in unit or not "units_y" in unit:
                # Just another player's view of the unit.
                # Because it's another player's view, it won't have the full unit info
                # in the case where the unit moves back into the fog.
                continue
            u_id = unit["units_id"]
            if u_id not in new_unit_info:
                logging.warning("Unknown unit id %d in move info", u_id)
                logging.debug("Creating new unit %d from move info", u_id)
                unit_info = {}
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
                    unit_info[k] = int(unit[prefix + k])
                for k in unit_keys_str:
                    unit_info[k] = unit[prefix + k]
                new_unit_info[u_id] = Unit(**unit_info)

            updated_unit_data = {
                "x" : unit["units_x"],
                "y": unit["units_y"],
                "moved": True,
                "fuel": unit["units_fuel"]
            }
            new_unit_info[u_id] = {**new_unit_info[u_id], **updated_unit_data}

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
        new_unit_info = deepcopy(self.units)
        unit_info = None

        # Figure out what information is the true info for the unit
        if "global" in info and len(info) == 1:
            # This is a normal standard match, where the unit is not Sonja's
            unit_info = info["global"]
        else:
            # This unit has special vision information (FOG or Sonja's unit)
            for p_id, unit in info.items():
                if p_id == "global":
                    continue
                p_id = int(p_id)
                # Only pick the unit that has full information
                # (since a player always has full view of their units)
                if unit["units_players_id"] == p_id:
                    unit_info = unit
                    break

        assert unit_info is not None

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
            built_unit[k] = int(unit_info[prefix + k])
        for k in unit_keys_str:
            built_unit[k] = unit_info[prefix + k]
        new_unit_info[built_unit["id"]] = Unit(**built_unit)

        # Player info
        # - funds change
        new_player_info = deepcopy(self.players)
        p_id = built_unit["players_id"]
        if not p_id == self.game_info["active_player_id"]:
            logging.warning("Build action for non-active player %d", p_id)
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
        # GameInfo Info - new active player, turn, and day
        updated_game_info = {
            "active_player_id": int(info["nextPId"]),
            "turn": self.game_info["turn"] + 1,
            "day": int(info["day"]),
        }
        new_global_info = {**self.game_info, **updated_game_info}

        # Player info
        # - funds change
        new_player_info = deepcopy(self.players)
        funds_info = info["nextFunds"]
        p_id = info["nextPId"]
        for value in funds_info.values():
            # This is definiely weird. We have to do it this way because in Fog
            # matches, funds are hidden from some players, and therefore there
            # is a view on the newFunds variable, with the hidden values being ''
            if isinstance(value, int):
                new_player_info[p_id]["funds"] = value
                break
        new_player_info[p_id]["co_power_on"] = False
        new_player_info[p_id]["super_co_power_on"] = False

        # Unit info
        # - TODO resupply
        # - fuel cost
        # - sank / crashed units
        new_unit_info = deepcopy(self.units)
        repaired_info = info["repaired"]
        if repaired_info and isinstance(repaired_info, dict):
            for value in repaired_info.values():
                assert isinstance(value, list)
                for unit in value:
                    u_id = int(unit["units_id"])
                    if u_id not in new_unit_info:
                        logging.warning("Unknown unit id %d in repair info", u_id)
                        continue
                    new_unit_info[u_id]["hit_points"] = unit["units_hit_points"]
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

    def _apply_power_action(self, action_data): # pylint: disable=unused-argument
        """
        Helper for power actions
        """
        logging.debug("Power action")

        # Player info
        # - power status
        # - funds change
        # - power meter change
        p_id = action_data["playerID"]
        co_meter = action_data["playersCOP"]
        new_player_info = deepcopy(self.players)
        new_player_info[p_id]["co_power"] = co_meter
        new_player_info[p_id]["co_power_on"] = (action_data["coPower"] == "Y")
        new_player_info[p_id]["super_co_power_on"] = (action_data["coPower"] == "S")

        # Unit info
        # - health change
        # - ammo change
        # - fuel change
        # - new unit(s)
        new_unit_info = deepcopy(self.units)
        if "unitAdd" in action_data:
            assert action_data["coName"] == "Sensei"
            unit_add_info = None
            if "global" in action_data["unitAdd"]:
                unit_add_info = action_data["unitAdd"]["global"]
            else:
                for p_id, info in action_data["unitAdd"].items():
                    if p_id == "global":
                        continue
                    p_id = int(p_id)
                    if p_id == info["playerId"]:
                        unit_add_info = info
                        break
            assert unit_add_info is not None

            # TODO: Improve unit creation from incomplete data
            name = unit_add_info["unitName"]
            # Infantry cost for Sensei
            cost = 1000
            if name == "Mech":
                cost = 3000
            new_unit_template = {
                "players_id": unit_add_info["playerId"],
                "name": name,
                "hit_points": 9, # Sensei's power creates the units all at 9hp...
                "cost": cost,
            }
            for unit in unit_add_info["units"]:
                u_id = unit["units_id"]
                unit_info = {
                    "id": u_id,
                    "x": unit["units_x"],
                    "y": unit["units_y"],
                }
                new_unit_info[u_id] = Unit(new_unit_template, **unit_info)

        # Hawke, Drake, Olaf, Andy, etc...
        if "hpChange" in action_data:
            for hp_type in ["hpGain", "hpLoss"]:
                if (hp_type in action_data["hpChange"] and
                    isinstance(action_data["hpChange"][hp_type], dict)):
                    hp_gain_info = action_data["hpChange"][hp_type]
                    hp = hp_gain_info["hp"]
                    # TODO: Handle units_fuel
                    for u_id, unit in new_unit_info.items():
                        if unit["players_id"] in hp_gain_info:
                            new_hp = new_unit_info[u_id]["hit_points"] + hp
                            new_unit_info[u_id]["hit_points"] += max(1, min(10, new_hp))

        # Von Bolt, Rachel, Sturm, Kindle...
        # And movement affecting abilities...
        if "unitReplace" in action_data:
            unit_replay_info = action_data["unitReplace"]
            # Iterate through all the values here. Since it's setting the new health
            # it's fine if we modify the same unit multiple times due to it showing
            # up in multiple views.
            for units in unit_replay_info.values():
                if not units or not units["units"]:
                    continue
                for unit in units["units"]:
                    u_id = unit["units_id"]
                    if "units_hit_points" in unit:
                        hp = unit["units_hit_points"]
                        new_unit_info[u_id]["hit_points"] = hp
                    if "units_moved" in unit:
                        new_unit_info[u_id]["moved"] = True

        return AWBWGameState(
                game_map=self.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_capt_action(self, action_data):
        """
        Helper for capt actions
        """
        logging.debug("Capt action")
        move_state = self
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = self._apply_move_action(action_data["Move"])
        # Unit info
        # - position change
        # - fuel change

        # Building info
        # - capture status
        # - ownership status
        capt_action = action_data["Capt"]
        building = capt_action["buildingInfo"]
        b_id = int(building["buildings_id"])
        assert b_id in move_state.buildings
        new_building_info = deepcopy(move_state.buildings)
        new_building_info[b_id]["capture"] = building["buildings_capture"]
        new_building_info[b_id]["team"] = building["buildings_team"]

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=move_state.units,
                buildings=new_building_info,
                game_info=move_state.game_info)

    def _apply_repair_action(self, action_data):
        """
        Helper for repair actions
        """
        logging.debug("Repair action")
        move_state = self
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = self._apply_move_action(action_data["Move"])
        # Unit info
        # - fuel change
        # - hitpoint change
        new_unit_info = deepcopy(move_state.units)

        repair_info = action_data["Repair"]
        p_id = None
        for value in repair_info["repaired"].values():
            if isinstance(value, dict):
                new_unit_info[value["units_id"]]["hit_points"] = value["units_hit_points"]
                p_id = new_unit_info[value["units_id"]]["players_id"]
                break
        assert p_id is not None

        # Player info
        # - funds change
        new_player_info = deepcopy(move_state.players)
        assert p_id in new_player_info
        funds = None
        for value in repair_info["funds"].values():
            if isinstance(value, int):
                funds = value
                break
        new_player_info[p_id]["funds"] = funds

        return AWBWGameState(
                game_map=move_state.game_map,
                players=new_player_info,
                units=new_unit_info,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    def _apply_supply_action(self, action_data):
        """
        Helper for supply actions
        """
        logging.debug("Supply action")
        move_state = self
        if "Move" in action_data and isinstance(action_data["Move"], dict):
            move_state = self._apply_move_action(action_data["Move"])

        # No funds change on supply.

        # Unit info
        # - fuel change
        # The supply data doesn't actually include the new fuel values,
        # so for now we'll only handle the move part.

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=move_state.units,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    def _apply_load_action(self, action_data):
        """
        Helper for load actions
        """
        logging.debug("Load action")

        # To load a unit into a transport, one must be moved
        assert "Move" in action_data
        move_state = self._apply_move_action(action_data["Move"])

        # Mark transport as carrying a unit, and the loaded unit as being carried
        load_action = action_data["Load"]
        loaded_id = 0
        transport_id = 0
        for u_id in load_action["loaded"].values():
            if isinstance(u_id, int):
                loaded_id = u_id
                break
        for u_id in load_action["transport"].values():
            if isinstance(u_id, int):
                transport_id = u_id
                break

        new_unit_info = deepcopy(move_state.units)
        # Units must already exist to be loaded / moved
        assert (loaded_id in new_unit_info) and (transport_id in new_unit_info)
        new_unit_info[loaded_id]["carried"] = True
        if new_unit_info[transport_id]["cargo1_units_id"] == 0:
            new_unit_info[transport_id]["cargo1_units_id"] = loaded_id
        else:
            new_unit_info[transport_id]["cargo2_units_id"] = loaded_id

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=new_unit_info,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    def _apply_unload_action(self, action_data):
        """
        Helper for unload actions
        """
        logging.debug("Unload action")

        new_unit_info = deepcopy(self.units)
        transport_id = action_data["transportID"]
        unit = None
        for value in action_data["unit"].values():
            if isinstance(value, dict) and "units_x" in value and "units_y" in value:
                unit = value
                break
        assert unit is not None
        loaded_id = unit["units_id"]
        if new_unit_info[transport_id]["cargo1_units_id"] == loaded_id:
            new_unit_info[transport_id]["cargo1_units_id"] = 0
        else:
            new_unit_info[transport_id]["cargo2_units_id"] = 0

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
            new_unit_info[loaded_id][k] = int(unit[prefix + k])
        for k in unit_keys_str:
            new_unit_info[loaded_id][k] = unit[prefix + k]
        new_unit_info[loaded_id]["carried"] = False

        return AWBWGameState(
                game_map=self.game_map,
                players=self.players,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_delete_action(self, action_data):
        """
        Helper for delete actions
        """
        logging.debug("Delete action")

        new_unit_info = deepcopy(self.units)
        for u_id in action_data["Delete"]["unitId"].values():
            if isinstance(u_id, int):
                # Set the unit's hp to zero to treat it as deleted
                new_unit_info[u_id]["hit_points"] = 0

        return AWBWGameState(
                game_map=self.game_map,
                players=self.players,
                units=new_unit_info,
                buildings=self.buildings,
                game_info=self.game_info)

    def _apply_hide_action(self, action_data):
        """
        Helper for hide actions
        """
        logging.debug("Hide action")

        move_state = self
        if "Move" in action_data:
            move_state = self._apply_move_action(action_data["Move"])

        hide_info = action_data["Hide"]
        new_unit_info = deepcopy(move_state.units)
        for u_id in hide_info["unit"].values():
            if isinstance(u_id, int):
                new_unit_info[u_id]["sub_dive"] = True

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=new_unit_info,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    def _apply_unhide_action(self, action_data):
        """
        Helper for unhide actions
        """
        logging.debug("Unhide action")

        move_state = self
        if "Move" in action_data:
            move_state = self._apply_move_action(action_data["Move"])

        unhide_info = action_data["Unhide"]
        new_unit_info = deepcopy(move_state.units)
        for unit in unhide_info["unit"].values():
            if isinstance(unit, dict) and "units_x" in unit and "units_y" in unit:
                u_id = unit["units_id"]
                new_unit_info[u_id]["sub_dive"] = False

        return AWBWGameState(
                game_map=move_state.game_map,
                players=move_state.players,
                units=new_unit_info,
                buildings=move_state.buildings,
                game_info=move_state.game_info)

    _ACTION_TYPE_TO_APPLY_FUNC = {
            AWBWGameAction.Type.FIRE : _apply_fire_action,
            AWBWGameAction.Type.JOIN : _apply_join_action,
            AWBWGameAction.Type.RESIGN : _apply_resign_action,
            AWBWGameAction.Type.MOVE : _apply_move_action,
            AWBWGameAction.Type.BUILD : _apply_build_action,
            AWBWGameAction.Type.END : _apply_end_action,
            AWBWGameAction.Type.POWER : _apply_power_action,
            AWBWGameAction.Type.CAPT : _apply_capt_action,
            AWBWGameAction.Type.LOAD : _apply_load_action,
            AWBWGameAction.Type.UNLOAD : _apply_unload_action,
            AWBWGameAction.Type.REPAIR : _apply_repair_action,
            AWBWGameAction.Type.SUPPLY : _apply_supply_action,
            AWBWGameAction.Type.DELETE : _apply_delete_action,
            AWBWGameAction.Type.HIDE : _apply_hide_action,
            AWBWGameAction.Type.UNHIDE : _apply_unhide_action,
            }

    def apply_action(self, action):
        return self._ACTION_TYPE_TO_APPLY_FUNC[action.type](self, action.info)

if __name__ == "__main__":
    import sys
    from awbw_replay.replay import AWBWReplay
    with AWBWReplay(sys.argv[1]) as replay:
        state = AWBWGameState(replay_initial=replay.game_info())

        print("Press enter to step through the replay")
        for _action in replay.actions():
            _action = AWBWGameAction(replay_action=_action)
            state = state.apply_action(_action)
            for p, p_info in state.players.items():
                print(f"{p}: G {p_info['funds']}")

        action_types = replay.action_summaries()
        print(f"The action types were {set(action_types)}")
