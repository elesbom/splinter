import unittest
from should_dsl import should
from splinter.browser import Browser
from splinter.driver.webdriver.firefox import FirefoxProfile

class FirefoxProfileTest(unittest.TestCase):

    def test_should_be_able_to_customize_preferences_on_profile(self):
        "should be able to customize preferences on profile"
        profile = FirefoxProfile()
        profile.set_preference('network.manage-offline-status', 'true')
        browser = Browser(profile=profile)
        browser.driver.browser.profile.prefs['network.manage-offline-status'] |should| equal_to('true')
        browser.quit()
