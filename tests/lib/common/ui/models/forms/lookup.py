import time

from selenium.webdriver.common.by import By

from groups import TextInput


class Lookup(TextInput):

    _lookup_button = (By.CLASS_NAME, 'Form-lookupButton')

    @property
    def lookup_button(self):
        return self.find_element(*self._lookup_button)

    #
    # The retry + poll logic in the two methods below are a temporary
    # workaround for https://github.com/ansible/ansible-tower/issues/1461
    # and should be removed when this issue is resolved.
    #
    def set_value(self, value, retry=True):
        if retry:
            self._set_value_with_retry(value)
        else:
            super(Lookup, self).set_value(value)

    def _set_value_with_retry(self, value):
        timeout = time.time() + 30
        while True:
            self.clear()
            super(Lookup, self).set_value(value)
            time.sleep(2)
            if not self.errors:
                break
            if time.time() > timeout:
                break
