from unittest import TestCase
from pylint.lint import Run


class LintTest(TestCase):

    def setUp(self):
        disabled_rules = [
            'missing-docstring',
            'super-init-not-called'
        ]
        self.default_filter = '--disable={rules}'.format(rules=','.join(disabled_rules))

    def test_library(self):
        with self.assertRaises(SystemExit) as lint_check:
            Run([self.default_filter, 'pyscc'])

        self.assertEqual(lint_check.exception.code, 0)
