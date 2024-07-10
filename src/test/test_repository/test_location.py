from depends_test import location_repository

def test_repository():
    locations = location_repository.get_all()
    assert len(locations) > 0

    