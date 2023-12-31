"""
Provides a function for managing the assistant configurations, including updating the list of assistant and thread ID pairs, and retrieving them from the 'assistants_config.json' file.
"""

import json

CONFIG_FILENAME = "assistants_config.json"

class AssistantConfigManager:

    @staticmethod
    def update_assistant_config(assistant_id, thread_id):
        try:
            with open(CONFIG_FILENAME, "r") as file:
                config = json.load(file)
        except FileNotFoundError:
            config = {"assistants": []}

        found = False
        for assistant in config["assistants"]:
            if assistant["assistant_id"] == assistant_id and assistant["thread_id"] == thread_id:
                found = True
                break

        if not found:
            config["assistants"].append({
                "assistant_id": assistant_id,
                "thread_id": thread_id
            })

        with open(CONFIG_FILENAME, "w") as file:
            json.dump(config, file, indent=2)

        return True

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