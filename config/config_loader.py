import json

class ConfigLoader:
    
    @staticmethod
    def load_rules(site):
        with open(f"config/{site}.json", 'r', encoding="utf-8") as file:
            return json.load(file)