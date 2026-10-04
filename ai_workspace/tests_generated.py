import pytest

from models import create_farmer, create_farm, Farmer, Farm, CropPhoto, CropHealthObservation
from logic import upload_photo, record_observation, get_observation_history

def test_create_account():
    # Test valid account creation
    result = create_farmer('Alice', 'alice@example.com')
    assert result == {'name': 'Alice', 'email': 'alice@example.com'}

    # Test invalid name
    with pytest.raises(ValueError):
        create_farmer('', 'alice@example.com')

    # Test invalid email
    with pytest.raises(ValueError):
        create_farmer('Alice', '')

def test_add_farm():
    # Test valid farm creation
    result = create_farm('Apple Farm', 'farmer123')
    assert result == {'name': 'Apple Farm', 'farmer_id': 'farmer123'}

    # Test invalid farm name
    with pytest.raises(ValueError):
        create_farm('', 'farmer123')

    # Test invalid farmer ID
    with pytest.raises(ValueError):
        create_farm('Apple Farm', '')

def test_upload_photo():
    # Test valid photo upload
    result = upload_photo('farm123', 'https://example.com/photo.jpg')
    assert result == {'farm_id': 'farm123', 'photo_url': 'https://example.com/photo.jpg'}

    # Test invalid photo URL
    with pytest.raises(ValueError):
        upload_photo('farm123', '')

def test_record_observation():
    # Test valid observation recording
    result = record_observation('farm123', 'Healthy')
    assert result == {'farm_id': 'farm123', 'observation': 'Healthy'}

    # Test invalid observation
    with pytest.raises(ValueError):
        record_observation('farm123', '')

def test_get_observation_history():
    # Test valid history retrieval
    result = get_observation_history('farm123')
    assert result == {'farm_id': 'farm123', 'observations': []}

    # Test invalid farm ID
    with pytest.raises(ValueError):
        get_observation_history('')