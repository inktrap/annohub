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
from _Login import Login
import _UiMap


class CreateProject(Login):

    def test_is_logged_in(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.close()

if __name__ == "__main__":
    unittest.main()
