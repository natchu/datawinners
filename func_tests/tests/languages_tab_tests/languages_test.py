# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.base_test import HeadlessRunnerTest
from framework.utils.common_utils import by_css
from pages.languagespage.customized_languages_page import CustomizedLanguagePage
from pages.loginpage.login_page import login
from tests.testsettings import UI_TEST_TIMEOUT

default_en_messages = [u'Thank you {Name of Data Sender}. We received your SMS: {List of Answers}',
                        u'Error. Incorrect answer for question {Question Numbers for Wrong Answer(s)}. Please review printed Questionnaire and resend entire SMS.',
                        u'Error. Incorrect number of responses. Please review printed Questionnaire and resend entire SMS.',
                        u'Error. {Submitted Identification Number} is not registered. Check the Identification Number and resend entire SMS or contact your supervisor.',
                        u'Error. You are not authorized to submit data for this Questionnaire. Please contact your supervisor.']

class TestLanguageTab(HeadlessRunnerTest):
    @classmethod
    def setUpClass(cls):
        HeadlessRunnerTest.setUpClass()
        login(cls.driver, landing_page="languages/")

    def setUp(self):
        self.language_page = CustomizedLanguagePage(self.driver)

    def test_languages_tab(self):

        self.check_for_default_en_messages()

        self.language_page.select_language("French", wait_for_load=True)
        self.language_page = CustomizedLanguagePage(self.driver)
        expected_fr_messages = [u"{Name of Data Sender}. Nous avons recu votre SMS: {List of Answers}",
                                u'Erreur. Reponse incorrecte pour la question {Question Numbers for Wrong Answer(s)}. Veuillez revoir le Questionnaire imprime et renvoyez tout le SMS.',
                                u'Erreur. Nombre de reponses incorrect. Veuillez revoir le Questionnaire imprime et renvoyez tout le SMS.',
                                u"Erreur. {Submitted Identification Number} n'est pas enregistre. Verifiez le Numero d'Identification et renvoyez SMS en entier ou contactez votre superviseur.",
                                u"Erreur. Vous n'etes pas autorise a soumettre des donnees pour ce Questionnaire. Contactez votre superviseur."]
        french_messages = [r.get_attribute('value') for r in self.driver.find_elements_(by_css("textarea"))]
        self.assertListEqual(expected_fr_messages, french_messages)
        self.language_page.select_language("English")

    def clear_all_errormessages(self):
        [r.clear() for r in self.driver.find_elements_(by_css("textarea"))]

    def check_for_default_en_messages(self):
        english_messages = [r.get_attribute('value') for r in self.driver.find_elements_(by_css("textarea"))]
        self.assertListEqual(default_en_messages, english_messages)

    def test_validations(self):
        self.clear_all_errormessages()
        self.language_page.save_changes()

        self.assertListEqual([u'Enter reply SMS text.']*5, [e.text for e in self.driver.find_elements_(by_css(".validationText"))])

        self.assertTrue("ui-state-disabled" in self.driver.find(by_css("#language_save")).get_attribute('class'))

        self.language_page.refresh()

        self.check_for_default_en_messages()

        [r.send_keys("a"*170) for r in self.driver.find_elements_(by_css("textarea"))]
        self.assertListEqual([u'Text should be less than 160 chars']*5, [e.text for e in self.driver.find_elements_(by_css(".validationText"))])


    def test_modify_and_save(self):

        self.change_reply_messages()
        self.language_page.save_changes()
        self.language_page.refresh()
        self.assertListEqual([msg + " new" for msg in default_en_messages],  self.language_page.get_all_messages())

        self.language_page.set_message_boxes(default_en_messages)

        self.language_page.save_changes()

    def change_reply_messages(self):
        [r.send_keys(' new') for r in self.driver.find_elements_(by_css("textarea"))]

    def verify_warning_dialog_present(self):
        self.driver.find_visible_element(by_css(".ui-dialog-titlebar"))


    def test_unsaved_warning_dialog(self):
        def click_identification_number_page():
            self.driver.find(by_css("#global_subjects_link")).click()
        self.verify_unsaved_warning_dialog(click_identification_number_page)

    def verify_unsaved_warning_dialog(self, navigate_away_action):
        self.change_reply_messages()
        navigate_away_action()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".cancel_button")).click()
        self.assertListEqual([msg + " new" for msg in default_en_messages],  self.language_page.get_all_messages())

        navigate_away_action()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".no_button")).click()

        self.driver.find(by_css("#global_languages_link")).click()
        self.language_page = CustomizedLanguagePage(self.driver)
        self.check_for_default_en_messages()

        self.change_reply_messages()
        navigate_away_action()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".yes_button")).click()

        self.driver.find(by_css("#global_languages_link")).click()
        self.language_page = CustomizedLanguagePage(self.driver)
        self.assertListEqual([msg + " new" for msg in default_en_messages],  self.language_page.get_all_messages())

        self.language_page.set_message_boxes(default_en_messages)
        self.language_page.save_changes()

    def test_unsaved_warning_on_language_change(self):
        def click_identification_number_page():
            self.language_page.select_language("French")
        self.verify_unsaved_warning_dialog(click_identification_number_page)
