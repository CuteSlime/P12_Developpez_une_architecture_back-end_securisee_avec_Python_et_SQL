from datetime import datetime

from unittest.mock import patch

from Models import User, Event, Customer, Contract


def test_event_create(app, session):
    """test of handle_create and create function for event

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """
    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")

    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=1)
    contract = Contract(customer_id=1, total_price=50,
                        remaining_to_pay=0, statut=True)

    session.add(user)
    session.add(customer)
    session.add(contract)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # Mock questionary and display_message
    with patch('questionary.text') as mock_text, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'):

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "06/06/2025 17H", "06/06/2025 18H", "london", "10", "a new note"
        ]

        mock_select.return_value.unsafe_ask.side_effect = [
            "1", "1"
        ]

        app.menu.event_controller.handle_create_event(access_token)

        dummy_event = session.query(Event).filter_by(id=1).first()

        assert dummy_event is not None, "The Dummy was not created in the DB"

        assert mock_text.call_count == 5, f"""questionary.text called {
            mock_text.call_count}/5"""
        assert mock_select.call_count == 2, f"""{
            mock_select.call_count}/2 customer and contract selected"""


def test_event_get(app, session):
    """test of handle_get and get function for event

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """
    user = User(full_name="test_user", email="test@test.com", group_id=3)
    user.set_password("test_password")
    user2 = User(full_name="test_user2", email="test@test.com", group_id=1)
    user2.set_password("test_password")

    comercial = User(full_name="test_user3",
                     email="test2@test.com", group_id=2)
    comercial.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=3)

    contract = Contract(customer_id=1, total_price=50,
                        remaining_to_pay=0, statut=False)

    date_start = datetime.strptime("05/05/2025 17H", "%d/%m/%Y %HH")
    date_end = datetime.strptime("05/05/2025 17H", "%d/%m/%Y %HH")

    event = Event(contract_id=1, customer_id=1, event_start=date_start,
                  event_end=date_end, user_id=1, location="paris", attendees=24, notes="a note")
    event2 = Event(contract_id=1, customer_id=1, event_start=date_start,
                   event_end=date_end, user_id=None, location="paris", attendees=24, notes="a note")

    session.add(user)
    session.add(user2)
    session.add(comercial)
    session.add(customer)
    session.add(contract)
    session.add(event)
    session.add(event2)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()
    test_user2 = session.query(User).filter_by(
        full_name="test_user2").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    access_token2 = User.create_access_token(
        data={"username": test_user2.full_name, "role": test_user2.role.group_name})

    # mock questionary and the handle_update/delete
    with patch('questionary.select') as mock_select, \
            patch('questionary.print'), \
            patch.object(app.menu.event_controller, 'handle_update_event') as mock_handle_update_event:

        # mock selecting the menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Events Without Support", "1", "Update event",
            "All Events", "1", "Update event",
            "Events that you manage", "1", "Update event",
            "All Events", "1", "Exit to event Menu"
        ]
        app.menu.event_controller.handle_get_event(access_token2)

        for _ in range(3):

            app.menu.event_controller.handle_get_event(access_token)

        assert mock_handle_update_event.call_count == 3, f"""event update was called {
            mock_handle_update_event.call_count}/3"""

        assert mock_select.call_count == 12, f"""{
            mock_select.call_count}/12 menu tested"""


def test_event_update(app, session):
    """test of handle_update and update function for event

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """
    user = User(full_name="test_user", email="test@test.com", group_id=3)
    user.set_password("test_password")
    user2 = User(full_name="test_user2", email="test2@test.com", group_id=3)
    user2.set_password("test_password")
    comercial = User(full_name="test_user3",
                     email="test2@test.com", group_id=2)
    comercial.set_password("test_password")
    comercial2 = User(full_name="test_user4",
                      email="test2@test.com", group_id=2)
    comercial2.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=3)
    customer2 = Customer(information="information", full_name="Dummy2",
                         email="Dummy2@custom.com", phone_number="0987654321",
                         company_name="Dummy2 corp", user_id=4)
    contract = Contract(customer_id=1, total_price=50,
                        remaining_to_pay=0, statut=False)
    contract2 = Contract(customer_id=2, total_price=50,
                         remaining_to_pay=0, statut=False)

    date_start = datetime.strptime("05/05/2025 17H", "%d/%m/%Y %HH")
    date_end = datetime.strptime("05/05/2025 17H", "%d/%m/%Y %HH")

    event = Event(contract_id=1, customer_id=1, event_start=date_start,
                  event_end=date_end, user_id=1, location="paris", attendees=24, notes="a note")

    session.add(user)
    session.add(user2)
    session.add(comercial)
    session.add(comercial2)
    session.add(customer)
    session.add(customer2)
    session.add(contract)
    session.add(contract2)
    session.add(event)
    session.commit()

    test_user = session.query(User).filter_by(full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary
    with patch('questionary.text') as mock_text, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'):

        dummy_event = session.query(Event).filter_by(id=1).first()

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "06/06/2025 17H", "06/06/2025 18H", "london", "10", "a new note"
        ]

        mock_select.return_value.unsafe_ask.side_effect = [
            "Update Contract", "2", "Update Customer", "2", "Update Event start date",
            "Update Event end date", "Update Support", "2", "Update location",
            "Update number of atendees", "Update Notes",
            "Validate Change and return to event Menu"
        ]

        app.menu.event_controller.handle_update_event(
            dummy_event, access_token)

        new_date_start = datetime.strptime("06/06/2025 17H", "%d/%m/%Y %HH")
        new_date_end = datetime.strptime("06/06/2025 18H", "%d/%m/%Y %HH")

        assert dummy_event.contract_id == 2, "event contract_id is not 2"
        assert dummy_event.customer_id == 2, "event customer_id is not 2"
        assert dummy_event.event_start == new_date_start, "event event_start is not 2025-06-06 17:00:00"
        assert dummy_event.event_end == new_date_end, "event event_end is not 2025-06-06 18:00:00"
        assert dummy_event.user_id == 2, "event user_id is not 2"
        assert dummy_event.location == "london", "event location is not london"
        assert dummy_event.attendees == 10, "event attendees is not 10"
        assert dummy_event.notes == "a new note", "event notes is not 'a new note'"

        assert mock_text.call_count == 5, f"""questionary.text called {
            mock_text.call_count}/5"""

        assert mock_select.call_count == 12, f"""{
            mock_select.call_count}/12 menu tested"""
