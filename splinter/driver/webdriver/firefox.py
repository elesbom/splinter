from selenium.firefox.webdriver import WebDriver as firefox_driver
from selenium.firefox.firefox_profile import FirefoxProfile as SeleniumFirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement

class WebDriver(BaseWebDriver):

    def __init__(self, **kwargs):
        if 'profile' in kwargs:
            self._extract_profile_preferences(kwargs['profile'])

        self.driver = firefox_driver()
        self.element_class = WebDriverElement

    def _extract_profile_preferences(self, profile):
        for key, value in profile.preferences:
            SeleniumFirefoxProfile.prefs[key] = value

class FirefoxProfile(object):

    def __init__(self):
        self._preferences = { }

    def set_preference(self, key, value):
        self._preferences[key] = value

    @property
    def preferences(self):
        for key, value in self._preferences.items():
            yield key, value
