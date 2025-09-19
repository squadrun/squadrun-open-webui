"""
Utility functions for user group management.
This module handles default group assignment for newly created users.
"""

import logging
from typing import Optional

from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])


def assign_user_to_default_group(user_id: str, user_email: str) -> bool:
    """
    Assign a user to the default group if one is configured.
    
    Args:
        user_id: The ID of the user to assign
        user_email: The email of the user (for logging purposes)
        
    Returns:
        bool: True if assignment was successful or no default group is configured, False if assignment failed
    """
    try:
        import os
        from open_webui.models.groups import Groups
        
        # Read directly from environment variable
        group_name = os.getenv("DEFAULT_USER_GROUP", "").strip()
        
        # Check if a default group is configured
        if not group_name:
            return True  # No default group configured, consider this successful
        
        # Find the group by name
        groups = Groups.get_groups()
        default_group = None
        for group in groups:
            if group.name == group_name:
                default_group = group
                break
        
        if not default_group:
            log.warning(f"Default group '{group_name}' not found. User {user_email} not assigned to any group.")
            return False
        
        # Add user to the group
        updated_group = Groups.add_users_to_group(default_group.id, [user_id])
        if updated_group:
            log.info(f"Assigned user {user_email} to default group: {group_name}")
            return True
        else:
            log.error(f"Failed to add user {user_email} to default group: {group_name}")
            return False
            
    except Exception as e:
        log.error(f"Failed to assign user {user_email} to default group: {str(e)}")
        return False
