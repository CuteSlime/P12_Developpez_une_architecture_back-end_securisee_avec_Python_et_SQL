class PermissionManager:
    def __init__(self):
        self.permissions = {
            "Management": {"Exit", "Validate_Change",
                           "user_menu", "handle_create_user", "handle_get_user",
                           "handle_update_user", "handle_delete_user",
                           "Update_user_fullname", "Update_user_email", "Update_user_password", "Update_user_group",
                           "group_menu",
                           "customer_menu", "handle_get_customer",
                           "contract_menu", "handle_create_contract",
                           "handle_get_contract", "handle_update_contract",
                           "Update_contract_customer", "Update_contract_total_price",
                           "Update_contract_remaining_to_pay", "Update_contract_statut",
                           # should be able to filter the event,
                           "event_menu", "handle_get_event", "handle_update_event",
                           "Update_event_support"
                           },
            "Commercial": {"Exit", "Validate_Change",

                           "customer_menu", "handle_create_customer", "handle_get_customer", "handle_update_customer",
                           "Update_customer_information", "Update_customer_fullname", "Update_customer_email",
                           "Update_customer_phone_number", "Update_customer_company_name", "Update_customer_commercial",
                           # filter on sign or remaining price
                           "contract_menu", "handle_get_contract", "handle_update_contract",
                           "Update_contract_customer", "Update_contract_total_price",
                           "Update_contract_remaining_to_pay", "Update_contract_statut",
                           "event_menu", "handle_create_event", "handle_get_event"
                           },
            "Support": {"Exit", "Validate_Change",
                        "customer_menu", "handle_get_customer",
                        "contract_menu", "handle_get_contract",
                        # filter event to see event who is attributed to them,
                        "event_menu", "handle_get_event", "handle_update_event",
                        "Update_event_contract", "Update_event_customer", "Update_event_start", "Update_event_end",
                        "Update_event_support", "Update_event_location", "Update_event_atendees", "Update_event_notes",
                        }
        }

    def has_permission(self, role_name, menu_name):
        return menu_name in self.permissions.get(role_name, set())
