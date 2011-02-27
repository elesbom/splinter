from lxml.cssselect import CSSSelector
from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList
from selenium.webdriver.common.exceptions import WebDriverException, NoSuchElementException

import time

class BaseWebDriver(DriverAPI):

    def __init__(self):
        self.wait_time = 2

    @property
    def title(self):
        return self.driver.title

    @property
    def html(self):
        return self.driver.get_page_source()

    @property
    def url(self):
        return self.driver.current_url

    def visit(self, url):
        self.driver.get(url)

    def execute_script(self, script):
        self.driver.execute_script(script)

    def evaluate_script(self, script):
        return self.driver.execute_script("return %s" % script)

    def is_element_present(self, finder, selector):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            if finder(selector):
                return True
        return False

    def is_element_not_present(self, finder, selector):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            if not finder(selector):
                return True
        return False

    def is_element_present_by_css_selector(self, css_selector):
        return self.is_element_present(self.find_by_css_selector, css_selector)

    def is_element_not_present_by_css_selector(self, css_selector):
        return self.is_element_not_present(self.find_by_css_selector, css_selector)

    def is_element_present_by_xpath(self, xpath):
        return self.is_element_present(self.find_by_xpath, xpath)

    def is_element_not_present_by_xpath(self, xpath):
        return self.is_element_not_present(self.find_by_xpath, xpath)

    def is_element_present_by_tag(self, tag):
        return self.is_element_present(self.find_by_tag, tag)

    def is_element_not_present_by_tag(self, tag):
        return self.is_element_present(self.find_by_tag, tag)

    def is_element_present_by_name(self, name):
        return self.is_element_present(self.find_by_name, name)

    def is_element_not_present_by_name(self, name):
        return self.is_element_not_present(self.find_by_name, name)

    def is_element_present_by_id(self, id):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                self.find_by_id(id)
                return True
            except NoSuchElementException:
                pass
        return False

    def is_element_not_present_by_id(self, id):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                self.find_by_id(id)
            except NoSuchElementException:
                return True
        return False

    def find_option_by_value(self, value):
        return self.find_by_xpath('//option[@value="%s"]' % value)

    def find_option_by_text(self, text):
        return self.find_by_xpath('//option[normalize-space(text())="%s"]' % text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href)

    def find_link_by_text(self, text):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_link_text(text)])

    def find_by_css_selector(self, css_selector):
        selector = CSSSelector(css_selector)
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_xpath(selector.path)])

    def find_by_xpath(self, xpath):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_xpath(xpath)])

    def find_by_name(self, name):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_name(name)])

    def find_by_id(self, id):
        return ElementList([self.element_class(self.driver.find_element_by_id(id), self)])

    def find_by_tag(self, tag):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_tag_name(tag)])

    def fill_in(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    fill = fill_in
    attach_file = fill

    def choose(self, name):
        field = self.find_by_name(name).first
        field.click()

    def check(self, name):
        field = self.find_by_name(name).first
        field.check()

    def uncheck(self, name):
        field = self.find_by_name(name).first
        field.uncheck()

    def select(self, name, value):
        self.find_by_xpath('//select[@name="%s"]/option[@value="%s"]' % (name, value)).first._element.select()

    def quit(self):
        self.driver.quit()


class WebDriverElement(ElementAPI):

    def __init__(self, element, browser):
        self._element = element
        self.browser = browser
        self._css_selector = None

    def _get_value(self):
        try:
            return self._element.value
        except WebDriverException:
            return self._element.text

    def _set_value(self, value):
        self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    @property
    def css_selector(self):
        if not self._css_selector:
            if self['id']:
                self._css_selector = '#%s' % self['id']
            else:
                self._css_selector = '%s.%s' % (self._element.tag_name, self['class'])

        return self._css_selector

    @property
    def text(self):
        return self._element.text

    def _trigger_event(self, event_name):
        self.browser.execute_script('$("%s").%s();' % (self.css_selector, event_name))

    def mouseover(self):
        self._trigger_event('mouseover')

    def mouseout(self):
        self._trigger_event('mouseout')

    def click(self):
        self._element.click()

    def check(self):
        if not self.checked:
            self._element.toggle()

    def uncheck(self):
        if self.checked:
            self._element.toggle()

    @property
    def checked(self):
        return self._element.is_selected()

    selected = checked

    @property
    def visible(self):
        return self._element.is_displayed()

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)
