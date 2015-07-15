from datawinners.preferences.models import ProjectPreferences


def get_columns_to_hide(user, tab, questionnaire_id=''):
    preference_name = tab + "_hide_column"
    preferences = ProjectPreferences.objects.filter(user=user, project_id=questionnaire_id,
                                                    preference_name=preference_name)
    hide_columns = []
    for preference in preferences:
        hide_columns.append(int(preference.preference_value))
    return hide_columns


def get_zero_indexed_columns_to_hide(user, tab, questionnaire_id=''):
    columns = get_columns_to_hide(user, tab, questionnaire_id)
    return [i - 1 for i in columns]


def delete_preferences(preferences):
    for preference in preferences:
        preference.delete()


def remove_hidden_columns_for_tab(user, tab, questionnaire_id=''):
    preference_name = tab + '_hide_column'
    preferences = ProjectPreferences.objects.filter(user=user, project_id=questionnaire_id,
                                                    preference_name=preference_name)
    delete_preferences(preferences)


def remove_all_hidden_columns(user, questionnaire_id):
    preferences = ProjectPreferences.objects.filter(user=user, project_id=questionnaire_id)
    delete_preferences(preferences)


def remove_hidden_columns_for_all_users(questionnaire_id):
    preferences = ProjectPreferences.objects.filter(project_id=questionnaire_id)
    delete_preferences(preferences)


def create_preference(tab, column_indices, questionnaire, user):
    preference_name = tab+"_hide_column"
    for column in column_indices:
        preference = ProjectPreferences(user_id=user.id, project_id=questionnaire.id,
                                        preference_name=preference_name, preference_value=column)
        preference.save()


def remove_preferences(tab, column_indices, questionnaire, user):
    preference_name = tab+"_hide_column"
    for column in column_indices:
        preferences = ProjectPreferences.objects.filter(user=user, project_id=questionnaire.id,
                                                        preference_name=preference_name,
                                                        preference_value=column)
        delete_preferences(preferences)