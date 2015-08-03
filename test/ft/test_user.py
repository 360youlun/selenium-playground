# -*- coding: utf-8 -*-

import unittest
from ..base_selenium import SeleniumTestCase

class UserSeleniumTest(SeleniumTestCase):

    def test_create_user(self):
        self.get('http://127.0.0.1:5000/')
        self.click('a')
        self.fill_field('#name', 'guoyangguang')
        self.click('input[type="submit"]')
        name = self.find_element('.user-name')
        self.assertEqual('name, guoyangguang', name.text)

if __name__ == '__main__':
    unittest.main()
