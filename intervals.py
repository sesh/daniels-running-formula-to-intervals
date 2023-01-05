from .thttp import request


def upload_to_intervals(
    workout_str, workout_name, athlete_id, api_key, folder_name="Daniels 2Q"
):
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/folders"

    # check to see if the folder_name folder already exists
    response = request(
        f"https://intervals.icu/api/v1/athlete/{athlete_id}/folders",
        basic_auth=("API_KEY", api_key),
    )
    if response.status != 200:
        print(f"Error requesting folders: {response.json}")
        return

    folders = [
        x for x in response.json if x["name"] == folder_name and x["type"] == "FOLDER"
    ]

    # create a folder if it doesn't exist
    if not folders:
        response = request(
            f"https://intervals.icu/api/v1/athlete/{athlete_id}/folders",
            json={"name": folder_name, "type": "FOLDER"},
            method="post",
            basic_auth=("API_KEY", api_key),
        )

        if response.status > 299:
            print(f"Error creating folder: {response.json}")
            return

        folder = response.json
    else:
        folder = folders[0]

    # upload our workout to that folder
    response = request(
        f"https://intervals.icu/api/v1/athlete/{athlete_id}/workouts",
        method="post",
        json=[
            {
                "description": workout_str,
                "folder_id": folder["id"],
                "indoor": False,
                "name": workout_name,
                "type": "Run",
            }
        ],
        basic_auth=("API_KEY", api_key),
    )

    if response.status > 299:
        print(f"Error creating workout: {response.json}")
        return
    else:
        print("Successfully created workout")

    return response.json
