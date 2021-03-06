#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re
import random
import sys


class Register(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:5000/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.random = random.randint(0, sys.maxint)

    def test_register(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Signup").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(self.random)
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(
            "%s@foo.int" % self.random)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.random)
        driver.find_element_by_id("confirm").clear()
        driver.find_element_by_id("confirm").send_keys(self.random)
        driver.find_element_by_css_selector("button.btn.btn-default").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
