import requests
import os
from tabulate import tabulate

DOCKERHUB_BASE = "https://hub.docker.com"


def headers(token):
  return {
    "Authorization": f"JWT {token}"
  }


def get_token(user, password):
  print(f"Getting token for user '{user}'")
  resp = requests.post(f"{DOCKERHUB_BASE}/v2/users/login/",
                       json={'username': user, 'password': password},
                       headers={'Content-Type': 'application/json'})
  if (resp.status_code != 200):
    raise f"Invalid credentials supplied. Service responded with {resp.status_code}"

  print("Token received")

  return resp.json()["token"]


if __name__ == "__main__":
    user = os.environ["CONTAINER_REGISTRY_USER"]
    pw = os.environ["CONTAINER_REGISTRY_PASSWORD"]

    token = get_token(user, pw)

    url = f"{DOCKERHUB_BASE}/v2/repositories/{user}/opentripplanner/tags/?page_size=10000"

    resp = requests.get(url, headers=headers(token))

    tags = resp.json()['results']

    for tag in tags:
        print(tag['name'])
        print(tag['tag_last_pushed'])
