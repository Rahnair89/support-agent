#!/usr/bin/env python3
"""Turn a task definition as AWS returns it into one AWS will accept."""
import json
import sys

READ_ONLY = (
    "taskDefinitionArn", "revision", "status", "requiresAttributes",
    "compatibilities", "registeredAt", "registeredBy", "deregisteredAt",
)

path, version = sys.argv[1], sys.argv[2]

with open(path) as fh:
    taskdef = json.load(fh)

for field in READ_ONLY:
    taskdef.pop(field, None)

for container in taskdef["containerDefinitions"]:
    env = {e["name"]: e["value"] for e in container.get("environment", [])}
    env["PROMPT_VERSION"] = version
    container["environment"] = [
        {"name": k, "value": v} for k, v in sorted(env.items())
    ]

with open(path, "w") as fh:
    json.dump(taskdef, fh, indent=2)

print(f"rendered {path} with PROMPT_VERSION={version}")
