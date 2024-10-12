from django.urls import reverse


def test_add_room_view_guest(guest_client):
    response = guest_client.get(reverse("rooms:add_room"))
    assert response.status_code == 405


def test_add_room_view_staff(front_desk_client, valid_room_form):
    response = front_desk_client.get(reverse("rooms:add_room"))
    assert response.status_code == 200
    response = front_desk_client.post(reverse("rooms:sadd_room"), data=valid_room_form)
    assert response.status_code == 200


def test_add_room_view_manager(manager_client, valid_room_form):
    response = manager_client.get(reverse("rooms:add_room"))
    assert response.status_code == 200
    response = manager_client.post(reverse("rooms:add_room"), data=valid_room_form)
    assert response.status_code == 200


def test_view_rooms_guest(guest_client, rooms):
    response = guest_client.get(reverse("rooms:rooms_list"))
    assert response.status_code == 200


def test_view_rooms_front_desk(front_desk_client, rooms):
    response = front_desk_client.get(reverse("rooms:rooms_list"))
    assert response.status_code == 200


def test_view_rooms_manager(manager_client, rooms):
    response = manager_client.get(reverse("rooms:rooms_list"))
    assert response.status_code == 200


def test_update_room_view_guest(guest_client, valid_room_form_update):
    response = guest_client.get(reverse("rooms:update_room"))
    assert response.status_code == 200
    response = guest_client.post(reverse("rooms:add_room"), data=valid_room_form_update)
    assert response.status_code == 200


def test_update_room_view_front_desk(front_desk_client, valid_room_form_update):
    response = front_desk_client.get(reverse("rooms:update_room"))
    assert response.status_code == 200
    response = front_desk_client.post(
        reverse("rooms:add_room"), data=valid_room_form_update
    )
    assert response.status_code == 200


def test_update_room_view_manager(manager_client, valid_room_form_update):
    response = manager_client.get(reverse("rooms:update_room"))
    assert response.status_code == 200
    response = manager_client.post(
        reverse("rooms:add_room"), data=valid_room_form_update
    )
    assert response.status_code == 200
