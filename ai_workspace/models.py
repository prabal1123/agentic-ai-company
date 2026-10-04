from dataclasses import dataclass

def create_farmer(name, email):
    if not name or not email:
        raise ValueError("Name and email required")
    return {'name': name, 'email': email}

def create_farm(name, farmer_id):
    if not name or not farmer_id:
        raise ValueError("Farm name and farmer ID required")
    return {'name': name, 'farmer_id': farmer_id}

class Farmer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Farm:
    def __init__(self, name, farmer_id):
        self.name = name
        self.farmer_id = farmer_id

class CropPhoto:
    def __init__(self, farm_id, photo_url):
        self.farm_id = farm_id
        self.photo_url = photo_url

class CropHealthObservation:
    def __init__(self, farm_id, observation):
        self.farm_id = farm_id
        self.observation = observation