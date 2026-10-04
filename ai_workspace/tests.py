import pytest

from models import create_farmer, create_farm
from logic import upload_photo, record_observation, get_observation_history


def test_create_farmer():
    with pytest.raises(ValueError):
        create_farmer('', 'test@example.com')

def test_create_farm():
    with pytest.raises(ValueError):
        create_farm('', '123')

def test_upload_photo():
    with pytest.raises(ValueError):
        upload_photo('456', '')

def test_record_observation():
    with pytest.raises(ValueError):
        record_observation('789', '')

def test_get_observation_history():
    with pytest.raises(ValueError):
        get_observation_history('')