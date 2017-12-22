from src.common import utils


def test_filter_json():
    json = {
        "_id": "58cd320f1ac463f48938d945",
        "index": 0,
        "picture": "http://placehold.it/32x32",
        "eyeColor": "green",
        "name": {
            "first": "Jones",
            "last": "Crosby"
        },
        "company": "CALCULA",
        "friends": [
            {
                "id": 0,
                "name": "Amy Kim"
            },
            {
                "id": 1,
                "name": "Small Fields"
            }
        ]
    }

    res = utils.filter_json(json, source_include=['name', 'company'])
    assert_res = {
        "name": {
            "first": "Jones",
            "last": "Crosby"
        },
        "company": "CALCULA",
    }

    assert res == assert_res

    res = utils.filter_json(json,
                            source_exclude=['friends', 'eyeColor', 'picture',
                                            'index', '_id'])

    assert res == assert_res
