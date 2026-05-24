import unittest

from password_cracker import check_password, check_password_constant_time, list_users, password_strength, random_str, set_password


class PasswordCrackerTests(unittest.TestCase):
    def test_check_password_returns_true_for_correct_password(self):
        self.assertTrue(check_password("sophie", "password lol"))

    def test_check_password_returns_false_for_incorrect_password(self):
        self.assertFalse(check_password("sophie", "wrong password"))

    def test_constant_time_check_matches_same_password(self):
        self.assertTrue(check_password_constant_time("nathalie", "fehxpwnl"))

    def test_list_users_contains_default_accounts(self):
        self.assertIn("sophie", list_users())
        self.assertIn("nathalie", list_users())

    def test_password_strength_classification(self):
        self.assertEqual(password_strength("password lol"), "weak")
        self.assertEqual(password_strength("Str0ng!Pass"), "strong")

    def test_random_str_produces_correct_length(self):
        self.assertEqual(len(random_str(12)), 12)

    def test_set_password_updates_database(self):
        set_password("tester", "abc123")
        self.assertTrue(check_password("tester", "abc123"))


if __name__ == "__main__":
    unittest.main()
