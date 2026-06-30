from pyrogram import filters
from database.sudoers import is_sudo
async def sudo_users_filter_fn(_, __, message):
    """Custom filter to check if the sender is a Sudo/Admin user."""
    if not message.from_user:
        return False
    return await is_sudo(message.from_user.id)
# Instantiate the custom filter
sudo_filter = filters.create(sudo_users_filter_fn)
