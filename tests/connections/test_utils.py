from src.connections.utils import generate_uuid_from_dict


def test_generate_uuid_from_dict():
    """Test generate_uuid_from_dict"""
    data_dict = {
        "type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    assert generate_uuid_from_dict(data_dict) == "2b4f23be-cd66-7009-2388-048e75095ac0"


def test_generate_uuid_from_dict_with_different_order():
    """Test generate_uuid_from_dict with different order"""
    data_dict = {
        "type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    reordered_dict = {
        "appid": "284882215",
        "type": "appstore",
        "region": "us",
        "slug": "facebook",
    }
    expected_uuid = "2b4f23be-cd66-7009-2388-048e75095ac0"
    assert generate_uuid_from_dict(data_dict) == expected_uuid
    assert generate_uuid_from_dict(reordered_dict) == expected_uuid


def test_generate_uuid_from_dict_with_different_case():
    """Test generate_uuid_from_dict with different case"""
    data_dict = {
        "type": "appstore",
        "region": "us",
        "slug": "facebook",
        "appid": "284882215",
    }
    upper_dict = {
        "type": "APPSTORE",
        "region": "US",
        "slug": "FACEBOOK",
        "appid": "284882215",
    }
    expected_uuid = "2b4f23be-cd66-7009-2388-048e75095ac0"
    assert generate_uuid_from_dict(data_dict) == expected_uuid
    assert generate_uuid_from_dict(upper_dict) == expected_uuid
