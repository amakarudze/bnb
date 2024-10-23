def test_reservation_model_string_representation(reservation):
    assert (
        str(reservation)
        == f"{reservation.user} {reservation.check_in_date} - {reservation.check_out_date}"
    )


def test_guest_model_string_representation(guest_1):
    assert str(guest_1) == guest_1.full_name
