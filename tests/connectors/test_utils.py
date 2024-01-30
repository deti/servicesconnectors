from src.connectors.utils import generate_uuid_from_dict


def test_generate_uuid_from_dict():
    """Test generate_uuid_from_dict"""
    data_dict = {
        "connector_type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    uuid = generate_uuid_from_dict(data_dict)
    assert uuid == "06772414-c83e-42c4-a5fb-8d1b914282e6"


def test_generate_uuid_from_dict_with_different_order():
    """Test generate_uuid_from_dict with different order"""
    data_dict = {
        "connector_type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    reordered_dict = {
        "appid": "284882215",
        "connector_type": "appstore",
        "region": "us",
        "slug": "facebook",
    }
    expected_uuid = "06772414-c83e-42c4-a5fb-8d1b914282e6"
    assert expected_uuid == generate_uuid_from_dict(data_dict)
    assert expected_uuid == generate_uuid_from_dict(reordered_dict)


def test_generate_uuid_from_dict_with_different_case():
    """Test generate_uuid_from_dict with different case"""
    data_dict = {
        "connector_type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    upper_dict = {
        "connector_type": "APPSTORE",
        "region": "US",
        "slug": "FACEBOOK",
        "appid": "284882215",
    }
    expected_uuid = "06772414-c83e-42c4-a5fb-8d1b914282e6"
    assert expected_uuid == generate_uuid_from_dict(data_dict)
    assert expected_uuid == generate_uuid_from_dict(upper_dict)
