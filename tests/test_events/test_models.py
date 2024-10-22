def test_string_representation(event):
    assert str(event) == f"{event.name} on {event.start_date}"
