teams_by_team_id = {
    1: "Carlitos",
    2: "Miguelito",
    3: "Carlos",
    4: "Fern",
    11: "Lui",
    12: "David",
    13: "Angel",
    14: "Anthony",
    16: "Mario",
    17: "Emy",
    18: "Jesse",
    19: "Julito",
}


def get_team_owner(team_id):
    if team_id not in teams_by_team_id:
        raise KeyError("Team ID not found")
    return teams_by_team_id.get(team_id)
