import pytest


@pytest.fixture
def search_report_form(db):
    return {
        "start_date": "2020-10-24",
        "end_date": "2020-10-29",
    }
