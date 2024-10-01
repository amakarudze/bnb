def test_room_model_string_representation(room):
    assert str(room) == room.name
