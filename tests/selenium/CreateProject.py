#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import os
from _Login import Login
from _Utils import select_option
import _UiMap


class CreateProject(Login):

    def _create_project(self, filename):
        if not os.path.isfile(filename):
            print "Setup error: The file %s does not exist or is not a file!" % filename
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Projects").click()
        driver.find_element_by_link_text("Add a new project").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(
            os.path.basename(filename) + u"-" + str(self.random))
        driver = select_option(driver, "language", "German")
        driver = select_option(driver, "genre", "Academic")

        driver.find_element_by_id("text").clear()
        driver.find_element_by_id("text").send_keys(
            filename)
        driver.find_element_by_css_selector("form.col-md-6 > button.btn.btn-default").click()
        time.sleep(600)
        driver.close()

    def _check_success(self):
        return self.driver.find_element_by_class_name('bg-success')

    def _check_success_message(self, element):
        assert "Tokenization and upload was successfull." in element.text
        return True

    def _check_danger(self):
        return self.driver.find_element_by_class_name('bg-danger')

    def _check_error(self):
        return self.driver.find_element_by_class_name('bg-danger')

    def test_create_project(self):
        ''' this is the default test '''
        filename = _UiMap.file_deflt
        self._create_project(filename)
        element = self._check_success()
        self._check_success_message(element)

    #def test_create_limit_project(self):
    #    """ this one is just below the limit"""
    #    filename = _UiMap.file_limit
    #    self._create_project(filename)
    #    element = self._check_success()
    #    self._check_success_message(element)

    #def test_create_large_project(self):
    #    """ large, but okay"""
    #    filename = _UiMap.file_large
    #    self._create_project(filename)
    #    element = self._check_success()
    #    self._check_success_message(element)

    #def test_create_crash_project(self):
    #    """ this one should crash it, because it is too huge"""
    #    filename = _UiMap.file_crash
    #    self._create_project(filename)
    #    element = self._check_danger()
    #    assert "The file you provided is too large" in element.text

    #def test_create_empty_project(self):
    #    """ empty, not okay"""
    #    filename = _UiMap.file_empty
    #    self._create_project(filename)
    #    element = self._check_danger()
    #    assert "The file you provided is empty" in element.text

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


if __name__ == "__main__":
    unittest.main(verbosity=5)
