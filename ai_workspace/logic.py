def upload_photo(farm_id, photo_url):
    if not photo_url:
        raise ValueError("Photo URL required")
    return {'farm_id': farm_id, 'photo_url': photo_url}

def record_observation(farm_id, observation):
    if not observation:
        raise ValueError("Observation required")
    return {'farm_id': farm_id, 'observation': observation}

def get_observation_history(farm_id):
    if not farm_id:
        raise ValueError("Farm ID required")
    return {'farm_id': farm_id, 'observations': []}