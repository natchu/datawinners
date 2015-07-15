import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from datawinners.accountmanagement.decorators import valid_web_user, is_datasender
from datawinners.main.database import get_database_manager
from datawinners.project.preferences import get_columns_to_hide, create_preference, remove_preferences
from datawinners.search.submission_headers import HeaderFactory
from mangrove.form_model.form_model import get_form_model_by_code


def get_column_indices(post_data, dbm, form_model, tab):
    all_columns = post_data.get('all_columns', None)
    if not all_columns:
        return [post_data.get('column')]
    header = HeaderFactory(dbm, form_model).create_header(tab)
    headers = header.get_field_names_as_header_name()
    column_indices = []
    for index in range(headers.__len__()):
        column_indices.append(index+1)
    return column_indices


def _update_preferences(tab, column_indices, questionnaire, user, visible):
    if not visible:
        create_preference(tab, column_indices, questionnaire, user)
    else:
        remove_preferences(tab, column_indices, questionnaire, user)


@valid_web_user
@is_datasender
@csrf_exempt
def hide_submission_log_column(request):
    user = request.user
    post_data = json.loads(request.POST.get('data'))
    tab = post_data.get('tab')
    visible = post_data.get('visible')
    form_code = post_data.get('questionnaire_code')
    manager = get_database_manager(request.user)
    questionnaire = get_form_model_by_code(manager, form_code)
    column_indices = get_column_indices(post_data, manager, questionnaire, tab)
    _update_preferences(tab, column_indices, questionnaire, user, visible)
    return HttpResponse(json.dumps({'success': True}))


@valid_web_user
@is_datasender
@csrf_exempt
def get_hidden_columns(request):
    user = request.user
    post_data = json.loads(request.POST.get('data'))
    form_code = post_data.get('questionnaire_code')
    manager = get_database_manager(request.user)
    questionnaire = get_form_model_by_code(manager, form_code)
    hide_columns = get_columns_to_hide(user, post_data.get('tab') , questionnaire.id)
    return HttpResponse(mimetype='application/json', content=json.dumps({"hide_columns": hide_columns}))
