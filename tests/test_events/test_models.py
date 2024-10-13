def test_string_representation(event):
    assert str(event) == f"{event.name} from {event.start_date} to {event.end_date}"
