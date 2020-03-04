""" Unit tests for the application security package """
from unittest import TestCase
from application.application_security.field_validation import GeneralRegexValidations


class TestFieldValidation(TestCase):
    """ Unit tests for field validation """

    def setUp(self):
        """ Set up class variables """
        self.regex_val = GeneralRegexValidations()
        self.script_injection = '`<alert>(1)</alert>'

    def test_email_validation(self):
        """ Test the email validation
        1. Set up test variables
        2. Validate email against regex with pass scenario
        3. Validate email against regex with fail scenario
        4. Validate email against regex with script scenario
        5. Validate email against regex with normal text scenario
        """

        # 1. Set up test variables
        pass_email = 'test_email@test.com'
        fail_email = 'not_an_email'
        normal_text = 'Not an eamil address'

        # 2. Validate email against regex with pass scenario
        chk = self.regex_val.email_validation(pass_email)
        self.assertTrue(chk)

        # 3. Validate email against regex with fail scenario
        chk = self.regex_val.email_validation(fail_email)
        self.assertFalse(chk)

        # 4. Validate email against regex with script scenario
        chk = self.regex_val.email_validation(self.script_injection)
        self.assertFalse(chk)

        # 5. Validate email against regex with normal text scenario
        chk = self.regex_val.email_validation(normal_text)
        self.assertFalse(chk)

    def test_name_validation(self):
        """ Test name validation
        1. Set up test variabels
        2. Validate name against pass scenario
        3. Validate name against fail scenario
        4. Validate name against valid special character scenario
        5. Validate name against valid case change scenario
        6. Validate name against script injection scenario
        7. Validate name against single name scenario
        """
        # 1. Set up test variables
        pass_scenario = 'John Doe'
        valid_special_character = "Jack O'Doyle"
        valid_case_chage = 'Frankie McClough'
        single_name = 'Rhetta'
        fail_sceanrio = '22345678'

        # 2. Validate name against pass scenario
        chk = self.regex_val.name_validation(pass_scenario)
        self.assertTrue(chk)

        # 3. Validate name against fail scenario
        chk = self.regex_val.name_validation(fail_sceanrio)
        self.assertFalse(chk)

        # 4. Validate name against valid special character scenario
        chk = self.regex_val.name_validation(valid_special_character)
        self.assertTrue(chk)

        # 5. Validate name against valid case change scenario
        chk = self.regex_val.name_validation(valid_case_chage)
        self.assertTrue(chk)

        # 6. Validate name against script injection scenario
        chk = self.regex_val.name_validation(self.script_injection)
        self.assertFalse(chk)

        # 7. Validate name against single name scenario
        chk = self.regex_val.name_validation(single_name)
        self.assertTrue(chk)

    def test_paragragh_validation(self):
        """ Test to validate paragragh inputs
        1. Set up test variables
        2. Validate paragragh pass scenario
        3. Validate paragragh fail scenario
        4. Validate paragragh scripting scenario
        """
        # 1. Set up test variables
        pass_scenario = """
        This is a long paragragh of text with multiple lines. I really don't know what to say,
        so this is just going to get a little winded and stupid after some point.  That point 
        has more than likely already passed.
        
        Well now that I'm wrapping this up, I'm really wondering why I did two paragraphs. This
        is just starting to get ridiculous. I don't even know why I keep typing, this is more
        than likely enough text.
        """
        fail_scenario = {
            'this_is_json': 'Just in case someone tries something cheeky',
            'another_layer': {
                'this_is_probably': 'Enough stuff',
                'some_inxed': 132563
            }
        }

        # 2. Validate paragragh pass scenario
        chk = self.regex_val.message_validation(pass_scenario)
        self.assertTrue(chk)

        # 3. Validate paragragh fail scenario
        chk = self.regex_val.message_validation(str(fail_scenario))
        self.assertFalse(chk)

        # 4. Validate paragragh scripting scenario
        chk = self.regex_val.message_validation(self.script_injection)
        self.assertFalse(chk)
