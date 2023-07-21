import requests
import os
from _datetime import datetime, timezone
from tabulate import tabulate
from dateutil.parser import parse

DOCKERHUB_BASE = "https://hub.docker.com"
MAX_UNPULLED_DAYS= 180


def headers(token):
  return {
    "Authorization": f"JWT {token}"
  }

def should_delete(last_pulled):
    if last_pulled is not None:
      time = parse(last_pulled)
      today = datetime.now(timezone.utc)
      duration = today - time
      days = duration.days
      return days > MAX_UNPULLED_DAYS
    else:
      # was never pulled
      return True

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
    repo = "opentripplanner"

    token = get_token(user, pw)

    url = f"{DOCKERHUB_BASE}/v2/repositories/{user}/{repo}/tags/?page_size=10000"

    resp = requests.get(url, headers=headers(token))

    tags = resp.json()['results']

    table = [["Tag", "Last pulled", "To be deleted"]]
    for tag in tags:
        last_pulled = tag['tag_last_pulled']

        row = [tag['name'], last_pulled, should_delete(last_pulled)]
        table.append(row)


    print("")
    print(f"Tags for repo {user}/{repo} on {DOCKERHUB_BASE}")
    print("")
    print(tabulate(table, headers="firstrow"))