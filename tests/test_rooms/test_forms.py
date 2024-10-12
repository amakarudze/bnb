from rooms.forms import RoomForm


def test_valid_room_form(valid_room_form, file_data):
    form = RoomForm(valid_room_form, file_data)
    # assert form.is_valid()
    # assert form.errors == {}
    assert form.is_multipart()
