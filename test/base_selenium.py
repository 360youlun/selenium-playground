#-*- coding: utf-8 -*-

"""
Selenium related base class.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

import config


class Browser(object):
    """
    Browser integrates methods of Selenium to make interaction with browser easier.
    """
    def __init__(self):
       self.browser = self.__class__.web_driver_singleton()

    def open(self):
        """
        close the current running browser,
        and open a new one.
        """
        if hasattr(self, 'browser') and self.browser:
            self.close()
        self.browser = self.__class__.web_driver_singleton()

    def close(self):
        """
        close the current running browser.
        """
        if self.browser:
            self.browser.quit()
            self.browser = None

    def get(self, url):
        """
        make a get request
        """
        self.browser.get(url)

    def current_url(self):
        return self.browser.current_url

    def wait_for_css_selector(self, selector):
        """
        Wait until webdriver loads a HTML element with specified CSS selector

        :param webdriver: Selenium webdriver
        :param selector: Specified CSS selector
        """
        WebDriverWait(self.browser, config.SELENIUM_WAIT_TIMEOUT).until(
            lambda driver: len(driver.find_elements_by_css_selector(selector)),
            "URL: %s | Waiting for %s, but didn't show up in time" % (
                self.browser.current_url, selector
            )
        )

    def wait_until_element_is_available(self, selector):
        """
        Wait until webdriver loads a HTML element with specified CSS selector which is enabled

        :param webdriver: Selenium webdriver
        :param selector: Specified CSS selector
        """
        def selector_is_displayed_and_enabled(driver):
            elements = driver.find_elements_by_css_selector(selector)
            elements = filter(lambda e: e.is_displayed() and e.is_enabled(), elements)
            return elements

        WebDriverWait(self.browser, config.SELENIUM_WAIT_TIMEOUT).until(
            selector_is_displayed_and_enabled,
            "URL: %s | Waiting for %s, but didn't show up in time" % (
                self.browser.current_url, selector
            )
        )

    def wait_until(self, func):
        """
        Wait until func returns True
        :param func: a lambda or function
        """
        WebDriverWait(self.browser, config.SELENIUM_WAIT_TIMEOUT).until(
            func,
            "URL: %s | fails to wait." % (self.browser.current_url)
        )

    def set_input_value(self, el, value):
        """
        use script to set element value
        """
        self.browser.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', el, value)

    def trigger_event_on_element(self, el, event):
        """
        trigger event
        """
        self.browser.execute_script('''
            var event; // The custom event that will be created
            var element = arguments[0];
            var event_name = arguments[1];

            if (document.createEvent) {
                event = document.createEvent("HTMLEvents");
                event.initEvent(event_name, true, true);
            } else {
                event = document.createEventObject();
                event.eventType = event_name;
            }

            event.eventName = event_name;

            if (document.createEvent) {
                element.dispatchEvent(event);
            } else {
                element.fireEvent("on" + event.eventType, event);
            }
        ''', el, event)

    def execute_script_from_file(self, path):
        """
        execute script from file
        """
        f = open(path)
        code = f.read()
        f.close()
        self.browser.execute_script(code)

    def append_html_to_element(self, element, html):
        """
        $(element).append(html)
        """
        self.browser.execute_script('''
            arguments[0].insertAdjacentHTML('beforeend', arguments[1]);
        ''', element, html)

    def find_element(self, selector):
        """
        Find single element and return it.
        """
        return self.browser.find_element_by_css_selector(selector)

    def find_elements(self, selector):
        """
        Find a collection of elements and return them.
        """
        return self.browser.find_elements_by_css_selector(selector)

    def fill_field(self, field_selector, value):
        """
        find a field on the page to input value.
        :field_selector: css selector to locate the field
        :value: value to be filled into the field
        """

        field = self.browser.find_element_by_css_selector(field_selector)
        field.clear()
        field.send_keys(value)
        return field

    def fill_ckeditor_field(self, selector, value):
        """
        find an iframe in ckeditor to input value.
        :selector: css selector to locate the element containing iframe.
        :value: value to be filled into the iframe.
        """
        selector = selector + ' iframe'
        iframe = self.browser.find_element_by_css_selector(selector)
        self.browser.switch_to.frame(iframe)
        body = self.browser.find_element_by_css_selector('body')
        body.send_keys(value)
        self.browser.switch_to.default_content()
        return iframe

    def click(self, selector):
        """
        find a field on the page to click, like link, button, text input, check box, radio input.
        :selector: css selector to locate the field
        """
        field = self.browser.find_element_by_css_selector(selector)
        field.click()
        return field

    def select_by_visible_text(self, select_tag_selector, text):
        """
        select an option that has the text from a select tag.
        :select_tag_selector: css selector to locate the select tag
        :text: text to locate the option
        """
        select_tag = self.browser.find_element_by_css_selector(select_tag_selector)
        Select(select_tag).select_by_visible_text(text)

    def select_by_index(self, select_tag_selector, index):
        """
        select an option that has the index from a select tag.
        :select_tag_selector: css selector to locate the select tag
        :index: index to locate the option
        """
        select_tag = self.browser.find_element_by_css_selector(select_tag_selector)
        Select(select_tag).select_by_index(index)

    def select_by_value(self, select_tag_selector, value):
        """
        select an option that has the value from a select tag.
        :select_tag_selector: css selector to locate the select tag
        :value: value to locate the option
        """
        select_tag = self.browser.find_element_by_css_selector(select_tag_selector)
        Select(select_tag).select_by_value(value)

    def accept_alert(self):
        """
        Wait for an alert to pop up, and accept the alert.
        :return: the text on the alert panel.
        """
        WebDriverWait(self.browser, config.SELENIUM_WAIT_TIMEOUT).until(
            lambda b: expected_conditions.alert_is_present(),
            'fails to wait for alert'
        )
        alert = self.browser.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def is_displayed(self, selector):
        element = self.browser.find_element_by_css_selector(selector)
        return element.is_displayed()
   
    @classmethod
    def web_driver_singleton(cls):
        user_agent = config.BROWSER_USER_AGENT
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.set_preference('browser.cache.memory.enable', True)
        profile.set_preference('browser.cache.disk.enable', True)
        profile.set_preference('browser.cache.offline.enable', True)
        profile.set_preference('network.http.use-cache', True)
        profile.set_preference('browser.cache.disk.parent_directory', '/tmp')
        browser = webdriver.Firefox(profile)
        browser.desired_capabilities["applicationCacheEnabled"] = True
        browser.set_window_size(1024, 768)
        return browser

class SeleniumTestCase(unittest.TestCase, Browser):
    """
    Base class for our selenium test cases, providing the browser instance.
    """

    def setUp(self):
        self.browser = Browser.web_driver_singleton()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        self.browser.close()
        unittest.TestCase.tearDown(self)
