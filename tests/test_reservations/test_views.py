def test_reservations_list_view_guest(guest_client, reservations, reservations_1):
    pass


def test_reservations_list_view_front_desk_staff(
    front_desk_client, reservations, reservations_1
):
    pass


def test_reservations_list_view_manager(manager_client, reservations, reservations_1):
    pass


def test_update_reservation_view_guest(
    guest_client, reservation, valid_reservation_rooms
):
    pass


def test_update_reservation_view_front_desk_staff(
    front_desk_client, reservation, valid_reservation_rooms
):
    pass


def test_update_reservation_view_manager(
    manager_client, reservation, valid_reservation_rooms
):
    pass


def test_dashboard_view_guest(guest_client):
    pass


def test_dashboard_view_front_desk_staff(
    front_desk_client,
):
    pass


def test_dashboard_view_manager(
    manager_client,
):
    pass
