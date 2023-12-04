# prune-container-repo

Delete tags in Dockerhub repos that have not been pulled for X days.

## Usage

```bash

CONTAINER_REGISTRY_PASSWORD='A-password' \
  prune-container-repo \
    -u a_user \
    -r user/repo \
    --days=365 \ # keep everything that has been published or pulled within the last 365 days
    --keep-semver \ # keep everything with x.z.y
```