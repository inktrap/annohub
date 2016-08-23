#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from _Login import Login


class CreateProject(Login):

    def test_tokenize_project(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Projects").click()
        # driver.find_element_by_link_text("Tokenize").click()
        first_tokenize_link = ".table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > a:nth-child(1)"
        driver.find_element_by_css_selector(first_tokenize_link).click()
        driver.close()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:
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


if __name__ == "__main__":
    unittest.main()
