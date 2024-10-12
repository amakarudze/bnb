from rooms.forms import RoomForm


def test_valid_room_form(valid_room_form, files):
    form = RoomForm(data=valid_room_form, files=files)
    # assert form.is_valid()
    assert form.errors == {}
