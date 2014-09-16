# coding=utf-8
import json
import os
import tempfile
import uuid
import re

from django.test import Client
from nose.plugins.attrib import attr
import xlrd

from datawinners.utils import random_string
from framework.base_test import HeadlessRunnerTest
from framework.utils.common_utils import by_css
from pages.loginpage.login_page import login
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.testsettings import UI_TEST_TIMEOUT


DIR = os.path.dirname(__file__)

@attr('functional_test')
class TestAdvancedQuestionnaireSubmissionExport(HeadlessRunnerTest):
    def setUp(self):
        self.test_data = os.path.join(DIR, 'testdata')
        self.client = Client()
        self.project_name = random_string()

    def _verify_main_sheet(self, workbook):
        self.assertEqual(
            "[u'Data Sender', u'Datasender Id', u'Submission Date', u'Status', u'Date(Year)', u'Date(Month-Year)', u'Date(DD-MM-YYYY)', u'Outer text', u'Select one outer', u'Select multiple outer', u'Date(Year)', u'Date(Month-Year)', u'Date(DD-MM-YYYY)', u'Text in a group', u'Yes or No?', u'Yes No or both', u'Date(Year)', u'Date(Month-Year)', u'Date(DD-MM-YYYY)', u'Text in a group', u'Yes or No?', u'Yes No or both', u'_index', u'_parent_index']",
            str(workbook.sheet_by_index(0).row_values(0)))
        self.assertEqual(
            "[u'Tester Pune', u'rep276']",
            str(workbook.sheet_by_index(0).row_values(1, 0, 2)))
        self.assertEqual(
            "[u'Success', 43466.0, 41791.0, 41900.0, u'Outer text', u'Yes', u'Yes, No', 43466.0, 41640.0, 41900.0, u'text in group', u'Yes', u'No', 42005.0, 41640.0, 41891.0, u'text123', u'No', u'Yes, No', 1.0, '']",
            str(workbook.sheet_by_index(0).row_values(1, 3)))
        self.assertEqual(
            "[u'Tester Pune', u'rep276']",
            str(workbook.sheet_by_index(0).row_values(2, 0, 2)))
        self.assertEqual(
            "[u'Success', 43466.0, 41791.0, 41900.0, u'Outer text', u'Yes', u'Yes, No', 43466.0, 41640.0, 41900.0, u'text in group', u'Yes', u'No', 42005.0, 41640.0, 41891.0, u'text123', u'No', u'Yes, No', 2.0, '']",
            str(workbook.sheet_by_index(0).row_values(2, 3)))
        self.assertEquals(3, workbook.sheet_by_index(0).nrows)

    def _verify_second_sheet(self, workbook):
        self.assertEqual(
            "[u'Yes No or both', u'Text in a group', u'Date(DD-MM-YYYY)', u'Yes or No?', u'Date(Month-Year)', u'Date(Year)', u'_index', u'_parent_index']",
            str(workbook.sheet_by_index(1).row_values(0)))
        self.assertEqual(
            "[u'Yes', u'text in group - repeat1', 41907.0, u'Yes', 41640.0, 40544.0, '', 1.0]",
            str(workbook.sheet_by_index(1).row_values(1)))
        self.assertEqual(
            "[u'Yes, No', u'text in group - repeat2', 41901.0, u'No', 41640.0, 40909.0, '', 1.0]",
            str(workbook.sheet_by_index(1).row_values(2)))
        self.assertEqual(
            "[u'Yes', u'text in group - repeat1', 41907.0, u'Yes', 41640.0, 40544.0, '', 2.0]",
            str(workbook.sheet_by_index(1).row_values(3)))
        self.assertEqual(
            "[u'Yes, No', u'text in group - repeat2', 41901.0, u'No', 41640.0, 40909.0, '', 2.0]",
            str(workbook.sheet_by_index(1).row_values(4)))
        self.assertEquals(5, workbook.sheet_by_index(1).nrows)

    def _verify_third_sheet(self, workbook):
        self.assertEqual(
            "[u'Date(Year)', u'Date(Month-Year)', u'Date(DD-MM-YYYY)', u'Text in a group', u'Yes No or both', u'Yes or No?', u'_index', u'_parent_index']",
            str(workbook.sheet_by_index(2).row_values(0)))
        self.assertEqual(
            "[40544.0, 41640.0, 41893.0, u'group22', u'Yes', u'No', '', 1.0]",
            str(workbook.sheet_by_index(2).row_values(1)))
        self.assertEqual(
            "[40544.0, 41640.0, 41894.0, u'group4', u'No', u'Yes', '', 1.0]",
            str(workbook.sheet_by_index(2).row_values(2)))
        self.assertEqual(
            "[40544.0, 41640.0, 41893.0, u'group22', u'Yes', u'No', '', 2.0]",
            str(workbook.sheet_by_index(2).row_values(3)))
        self.assertEqual(
            "[40544.0, 41640.0, 41894.0, u'group4', u'No', u'Yes', '', 2.0]",
            str(workbook.sheet_by_index(2).row_values(4)))
        self.assertEquals(5, workbook.sheet_by_index(1).nrows)

    def _verify_fourth_sheet(self, workbook):
        self.assertEqual(
            "[u'Date(DD-MM-YYYY)', u'Yes or No?', u'Date(Month-Year)', u'Text in a group', u'Date(Year)', u'Yes No or both', u'_index', u'_parent_index']",
            str(workbook.sheet_by_index(3).row_values(0)))
        self.assertEqual(
            "[41896.0, u'Yes', 41640.0, u'group', 41640.0, u'Yes', '', 1.0]",
            str(workbook.sheet_by_index(3).row_values(1)))
        self.assertEqual(
            "[41892.0, u'No', 41640.0, u'group3', 40179.0, u'Yes, No', '', 1.0]",
            str(workbook.sheet_by_index(3).row_values(2)))
        self.assertEqual(
            "[41896.0, u'Yes', 41640.0, u'group', 41640.0, u'Yes', '', 2.0]",
            str(workbook.sheet_by_index(3).row_values(3)))
        self.assertEqual(
            "[41892.0, u'No', 41640.0, u'group3', 40179.0, u'Yes, No', '', 2.0]",
            str(workbook.sheet_by_index(3).row_values(4)))
        self.assertEquals(5, workbook.sheet_by_index(1).nrows)

    def test_export(self):
        self.client.login(username='tester150411@gmail.com', password='tester150411')
        self.global_navigation_page = login(self.driver, VALID_CREDENTIALS)
        questionnaire_code = self._verify_questionnaire_creation(self.project_name)
        temporary_project_name = self._navigate_and_verify_web_submission_page_is_loaded()
        # Make 2 submissions
        self._do_web_submission(temporary_project_name, questionnaire_code, 'tester150411@gmail.com', 'tester150411')
        self._do_web_submission(temporary_project_name, questionnaire_code, 'tester150411@gmail.com', 'tester150411')

        resp = self.client.post('/project/export/log?type=all',
                                {'project_name': self.project_name,
                                 'search_filters': "{\"search_text\":\"\",\"dateQuestionFilters\":{}}",
                                 'questionnaire_code': questionnaire_code})

        xlfile_fd, xlfile_name = tempfile.mkstemp(".xls")
        os.write(xlfile_fd, resp.content)
        os.close(xlfile_fd)
        workbook = xlrd.open_workbook(xlfile_name)
        self.assertEquals(workbook.sheet_names(),
                          [u'main', u'my-repeat-in-a-group', u'my-group-in-a-repeat', u'my-outer-repeat'])

        self._verify_main_sheet(workbook)
        self._verify_second_sheet(workbook)
        self._verify_third_sheet(workbook)
        self._verify_fourth_sheet(workbook)

    def _navigate_and_verify_web_submission_page_is_loaded(self):
        all_data_page = self.global_navigation_page.navigate_to_all_data_page()
        all_data_page.navigate_to_web_submission_page(self.project_name)
        form_element = self._verify_advanced_web_submission_page_is_loaded()
        return form_element.get_attribute('id')

    def _verify_advanced_web_submission_page_is_loaded(self):
        form_element = self.driver.wait_for_element(UI_TEST_TIMEOUT, by_css("form"), True)
        self.driver.wait_until_element_is_not_present(UI_TEST_TIMEOUT, by_css(".ajax-loader"))
        return form_element

    def _verify_questionnaire_creation(self, project_name):
        r = self.client.post(
            path='/xlsform/upload/?pname=' + project_name + '&qqfile=ft_advanced_questionnaire_export.xls',
            data=open(os.path.join(self.test_data, 'ft_advanced_questionnaire_export.xls'), 'r').read(),
            content_type='application/octet-stream')
        self.assertEquals(r.status_code, 200)
        self.assertNotEqual(r._container[0].find('project_name'), -1)
        response = json.loads(r._container[0])
        self.project_id = response.get('project_id')
        return response['form_code']

    def _do_web_submission(self, project_temp_name, form_code, user, password):
        submission_data = open(os.path.join(self.test_data, 'advanced_questionnaire_export_submission.xml'), 'r').read()
        submission_data = re.sub("tmpdt7nQf", project_temp_name, submission_data)
        submission_data = re.sub("<form_code>053", "<form_code>" + form_code, submission_data)
        client = Client()
        client.login(username=user, password=password)
        r = client.post(path='/xlsform/web_submission/', data={'form_data': submission_data, 'form_code': form_code})
        self.assertEquals(r.status_code, 201)
        self.assertNotEqual(r._container[0].find('submission_uuid'), -1)

    def create_submissions(self):
        _from = "917798987116"
        _to = "919880734937"
        for i in [17, 18]:
            message = "cli001 cid001 export%s %d 02.02.2012 a a 2,2 a" % (i, i)
            data = {"message": message, "from_msisdn": _from, "to_msisdn": _to, "message_id": uuid.uuid1().hex}
            self.client.post("/submission", data)


