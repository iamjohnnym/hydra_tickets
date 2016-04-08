from app import api, models


callbacks_blueprint = api.create_api(models.Callbacks,
    methods=['DELETE', 'GET', 'POST', 'PUT'], max_results_per_page=-1)
callback_data_blueprint = api.create_api(models.CallbackDetails, methods=['DELETE', 'GET', 'PUT', 'POST'])
callback_data_blueprint = api.create_api(models.ActiveTickets, methods=['DELETE','GET', 'PUT', 'POST'])
callback_data_blueprint = api.create_api(models.User, methods=['DELETE','GET', 'PUT', 'POST'])
