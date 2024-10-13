from django.urls import reverse


def test_add_event_view_guest(guest_client):
    response = guest_client.get(reverse("events:add_event"))
    assert response.status_code == 403


def test_add_event_view_staff(front_desk_client, valid_event_form):
    response = front_desk_client.get(reverse("events:add_event"))
    assert response.status_code == 200
    response = front_desk_client.post(
        reverse("events:add_event"), data=valid_event_form
    )
    assert response.status_code == 302


def test_add_event_view_manager(manager_client, valid_event_form):
    response = manager_client.get(reverse("events:add_event"))
    assert response.status_code == 200
    response = manager_client.post(reverse("events:add_event"), data=valid_event_form)
    assert response.status_code == 302


def test_view_events_guest(guest_client):
    response = guest_client.get(reverse("events:events_list"))
    assert response.status_code == 403


def test_view_events_front_desk(front_desk_client):
    response = front_desk_client.get(reverse("events:events_list"))
    assert response.status_code == 200


def test_view_events_manager(manager_client):
    response = manager_client.get(reverse("events:events_list"))
    assert response.status_code == 200


def test_update_event_view_guest(guest_client, event, valid_event_form_update):
    response = guest_client.get(reverse("events:update_event", args=(event.pk,)))
    assert response.status_code == 403
    response = guest_client.post(
        reverse("events:update_event", args=(event.pk,)), data=valid_event_form_update
    )
    assert response.status_code == 403


def test_update_event_view_manager(
    manager_client, event, valid_event_form_update, file_data
):
    response = manager_client.get(reverse("events:update_event", args=(event.pk,)))
    assert response.status_code == 200
    response = manager_client.post(
        reverse("events:update_event", args=(event.pk,)),
        data=valid_event_form_update,
        files=file_data,
    )
    assert response.status_code == 302


def test_update_event_view_front_desk(
    front_desk_client, event, valid_event_form_update, file_data
):
    response = front_desk_client.get(reverse("events:update_event", args=(event.pk,)))
    assert response.status_code == 200
    response = front_desk_client.post(
        reverse("events:update_event", args=(event.pk,)),
        data=valid_event_form_update,
        files=file_data,
    )
    assert response.status_code == 302
