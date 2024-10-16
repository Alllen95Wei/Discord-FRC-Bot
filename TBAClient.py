# coding=utf-8
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "TOKEN.env"))


TBA_api_url = "https://www.thebluealliance.com/api/v3/"
TBA_api_key = {"X-TBA-Auth-Key": str(os.getenv("TBA_TOKEN"))}
FRC_api_url = "https://frc-api.firstinspires.org/v3.0/"
FRC_api_key = {"Authorization": str(os.getenv("FRC_TOKEN")),
               "If-Modified-Since": ""}
base_dir = os.path.abspath(os.path.dirname(__file__))


# TBA API Docs: https://www.thebluealliance.com/apidocs/v3
# FRC API Docs: https://frc-api-docs.firstinspires.org/
class Team:
    def __init__(self, team_id: int):
        self.id = team_id
        self.TBA_url = TBA_api_url + "team/frc" + str(self.id)
        self.FRC_url = FRC_api_url

    def get_basic_info(self):
        r = requests.get(self.TBA_url + "/simple", headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def get_info(self):
        r = requests.get(self.TBA_url, headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def get_avatar(self, year: int):
        r = requests.get(url=f"{self.FRC_url}{year}/avatars?teamNumber={self.id}", headers=FRC_api_key, timeout=10,
                             data={})
        if r.status_code == 200:
            try:
                raw_text = r.json()["teams"][0]["encodedAvatar"]
            except IndexError:
                raw_text = ""
            if raw_text != "":
                img_data = base64.b64decode(raw_text)
                file_name = f"avatar_{self.id}.png"
                with open(file_name, "wb") as f:
                    f.write(img_data)
                return file_name
            else:
                return None
        else:
            return None

    def get_social_media(self):
        r = requests.get(self.TBA_url + "/social_media", headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def get_awards(self):
        r = requests.get(self.TBA_url + "/awards", headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def get_attended_event_keys(self):
        r = requests.get(self.TBA_url + "/events/keys", headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r


def get_event_keys(year: int):
    r = requests.get(TBA_api_url + "/events/" + str(year) + "/keys", headers=TBA_api_key, timeout=10).json()
    if r:
        return r
    else:
        raise ValueError("No events found")


class Event:
    def __init__(self, event_key: str):
        self.key = event_key
        self.TBA_url = TBA_api_url + "event/" + str(self.key)
        self.FRC_url = FRC_api_url

    def get_info(self):
        r = requests.get(self.TBA_url, headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def get_team_list(self):
        r = requests.get(self.TBA_url + "/teams", headers=TBA_api_key, timeout=10).json()
        if "Error" in r:
            raise ValueError(r["Error"])
        else:
            return r

    def save_matches_as_json(self):
        r = requests.get(self.TBA_url + "/matches", headers=TBA_api_key, timeout=10).text
        with open(os.path.join(base_dir, "matches", self.key + ".json"), "w") as f:
            f.write(r)


if __name__ == "__main__":
    print(Event("2024tuis").save_matches_as_json())
