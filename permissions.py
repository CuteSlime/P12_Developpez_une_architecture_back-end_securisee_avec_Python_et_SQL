class PermissionManager:
    def __init__(self):
        self.permissions = {
            "Management": {"Exit", "Validate_Change",
                           "user_menu", "handle_create_user", "handle_get_user", "handle_update_user", "handle_delete_user",
                           "Update_user_fullname", "Update_user_email", "Update_user_password", "Update_user_group",
                           "group_menu",
                           "customer_menu", "handle_get_customer",
                           "contract_menu", "handle_create_contract", "handle_get_contract", "handle_update_contract",
                           # should be able to filter the event, update only to update the Support
                           "event_menu", "handle_get_event", "handle_update_event",
                           "Update_event_support"
                           },
            "Commercial": {"Exit", "Validate_Change",
                           # update only customer that he is responsible for
                           "customer_menu", "handle_create_customer", "handle_get_customer", "handle_update_customer",
                           # update only contract that he is responsible for, filter on sign or remaining price
                           "contract_menu", "handle_get_contract", "handle_update_contract",
                           # create event only for this own customer that have signed a contract
                           "event_menu", "handle_create_event", "handle_get_event"},
            "Support": {"Exit", "Validate_Change",
                        "customer_menu", "handle_get_customer",
                        "contract_menu", "handle_get_contract",
                        # filter event to see event who is attributed to them, update only event they are responsible of.
                        "event_menu", "handle_get_event", "handle_update_event"}
        }

    def has_permission(self, role_name, menu_name):
        return menu_name in self.permissions.get(role_name, set())
