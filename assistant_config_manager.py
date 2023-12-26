"""
Provides a function for managing the assistant configurations, including updating the list of assistant and thread ID pairs, and retrieving them from the 'assistants_config.json' file.
"""

import json

CONFIG_FILENAME = "assistants_config.json"

class AssistantConfigManager:

    @staticmethod
    def get_assistant_threads():
        """
        Reads the assistants configuration file and returns a list of
        assistant and thread ID pairs.
        """
        try:
            with open(CONFIG_FILENAME, "r") as file:
                config = json.load(file)
                return config.get("assistants", [])
        except FileNotFoundError:
            # If the configuration file doesn't exist, return an empty list
            return []

    @staticmethod
    def update_assistant_config(assistant_id, thread_id):
        try:
            # Read the existing configuration file
            with open(CONFIG_FILENAME, "r") as file:
                config = json.load(file)
        except FileNotFoundError:
            # If file doesn't exist, start with an empty config
            config = {"assistants": []}

        # Add the new assistant and thread ID to the configuration
        config["assistants"].append({
            "assistant_id": assistant_id,
            "thread_id": thread_id
        })

        # Write the updated configuration back to the file
        with open(CONFIG_FILENAME, "w") as file:
            json.dump(config, file, indent=2)

        return True