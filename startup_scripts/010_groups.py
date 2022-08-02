import sys

from startup_script_utils import load_yaml
from users.models import AdminGroup, AdminUser

groups = load_yaml("/opt/netbox/initializers/groups.yml")
if groups is None:
    sys.exit()

for groupname, group_details in groups.items():
    group, created = AdminGroup.objects.get_or_create(name=groupname)

    if created:
        print("👥 Created group", groupname)

    for username in group_details.get("users", []):
        if user := AdminUser.objects.get(username=username):
            group.user_set.add(user)
            print(f" 👤 Assigned user {username} to group {group.name}")

    group.save()
