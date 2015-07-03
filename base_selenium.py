# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class Browser(object):
    """
    Browser integrates methods of Selenium to make interaction with browser easier.
    """
    def __init__(self):
        self.browser = webdriver.Firefox()

    def wait_for_css_selector(self, selector):
        """
        Wait until webdriver loads a HTML element with specified CSS selector

        :param webdriver: Selenium webdriver
        :param selector: Specified CSS selector
        """
        WebDriverWait(self.browser, 40).until(
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

        WebDriverWait(self.browser, 40).until(
            selector_is_displayed_and_enabled,
            "URL: %s | Waiting for %s, but didn't show up in time" % (
                self.browser.current_url, selector
            )
        )

    def wait_until_xpath_exists(self, xpath):
        """
        waint until xpath element exists
        :param webdriver: Selenium webdriver
        :param xpath: xpath selector
        """
        WebDriverWait(self.browser, 40).until(
            lambda driver: len(driver.find_element_by_xpath(xpath)),
            "URL: %s | Waiting for %s, but didn't show up in time" % (
                self.browser.current_url, xpath
            )
        )

    def wait_until_xpath_selector_is_displayed(self, xpath):
        """
        wait until xpath element is displayed
        :param webdriver: Selenium webdriver
        :param xpath: xpath selector
        """
        def selector_is_exist_and_active(driver):
            elements = driver.find_element_by_xpath(xpath)
            return elements and elements.is_displayed()

        WebDriverWait(self.browser, 40).until(
            selector_is_exist_and_active,
            "URL: %s | Waiting for %s, but didn't show up in time" % (
                self.browser.current_url, xpath
            )
        )

    def wait_until(self, func):
        """
        Wait until func returns True
        :param func: a lambda or function
        """
        WebDriverWait(self.browser, 40).until(
            func,
            "URL: %s | fails to wait." % (self.browser.current_url)
        )

    def assert_elements_exist(self, selectors):
        """
        Asserts if elements exist in DOM.
        :param selectors: a list of CSS selectors.
        """
        for selector in selectors:
            elements = self.browser.find_elements_by_css_selector(selector)
            self.assertGreater(len(elements), 0, "Element %s does not exists!" % selector)

    def set_select_element_value(self, el, index):
        """
        set select element index children selected attribute
        """
        self.browser.execute_script('''
            var el = arguments[0];
            var index = arguments[1];
            el.children[index].setAttribute('selected', 'selected');
        ''', el, index)

    def set_input_element_value(self, el, value):
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

    def get(self, url):
        """
        run a get request
        """
        self.browser.get(url)

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
        WebDriverWait(self.browser, 40).until(
            lambda b: expected_conditions.alert_is_present(),
            'fails to wait for alert'
        )
        alert = self.browser.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def open(self):
        """
        close the current running browser,
        and open a new one.
        """
        if hasattr(self, 'browser') and self.browser:
            self.close()
        self.browser = WebDriverSingleton().browser
        self.browser.maximize_window()

    def close(self):
        """
        close the current running browser.
        """
        if self.browser:
            self.browser.quit()
            self.browser = None

    def current_url(self):
        return self.browser.current_url

    def is_displayed(self, selector):
        element = self.browser.find_element_by_css_selector(selector)
        return element.is_displayed()
