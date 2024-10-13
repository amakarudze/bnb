from events.forms import EventForm


def test_valid_event_form(valid_event_form, file_data):
    form = EventForm(valid_event_form, file_data)
    # assert form.is_valid()
    # assert form.errors == {}
    assert form.is_multipart()
