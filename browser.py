from selenium import webdriver
from selenium.common import exceptions as EX
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BrowserNotSupportError(Exception):
  pass


class BrowserOptions:
  pass


class ChromeOpts(BrowserOptions):
  def __init__(self) -> None:
    # https://blog.csdn.net/dragongreenfire/article/details/114915966
    # https://www.cnblogs.com/superhin/p/12607074.html
    # Headless
    self.headless = False
    # Disable GPU acceleration (recommended for headless)
    self.disable_gpu = False
    
    # Don't load images
    self.disable_images = False
    
    # Private browser mode
    self.incognito = False
    
    # Disable all Chrome plugins
    self.disable_plugins = False

    # INFO = 0; WARNING = 1; LOG_ERROR = 2; LOG_FATAL = 3 default is 0
    # https://blog.csdn.net/wm9028/article/details/107536929
    self.log_level = 0
    # don't outpur "DevTools listening on ws://127.0.0.1"
    # https://blog.csdn.net/wm9028/article/details/107536929
    self.enable_logging = False

  @property
  def applied(self) -> webdriver.ChromeOptions:
    applied_options = webdriver.ChromeOptions()
    if self.headless: 
      applied_options.add_argument('headless') #
      # chrome_opts.headless=True
    if self.disable_gpu:
      applied_options.add_argument('disable-gpu') #
    if self.disable_images:
      applied_options.add_argument('blink-settings=imagesEnabled=false') #
      # prefs = {"profile.managed_default_content_settings.images", 2}
      # chrome_opts.add_experimental_option("prefs", prefs)
    if self.incognito:
      applied_options.add_argument('incognito') #
    if self.disable_plugins:
      applied_options.add_argument('disable-plugins') #
    applied_options.add_argument(f"log-level={self.log_level}") 
    if self.enable_logging:
      applied_options.add_experimental_option('excludeSwitches', ['enable-logging']) #

    # chrome_opts.page_load_strategy = 'eager'
    # https://blog.csdn.net/qq_34562959/article/details/121730935

    ##############################
    # BUG (NOT FIXED): can't download picture in headless mode
    # https://sqa.stackexchange.com/questions/37459/how-to-download-in-headless-mode-with-selenium
    # https://bugs.chromium.org/p/chromium/issues/detail?id=696481
    # https://github.com/shawnbutton/PythonHeadlessChrome/blob/master/driver_builder.py
    # https://github.com/SeleniumHQ/selenium/issues/5159
    # https://www.cnblogs.com/7749ha/p/9474949.html
    # https://www.jianshu.com/p/06269a22004d
    #
    # download_location = os.path.abspath(os.path.dirname(__file__)) + '\\static' 
    # download_location = "D:\\russe\\Downloads"  #  +  '\\static' 
    # prefs = {
    #   'download.default_directory': download_location, 
    #   'profile.default_content_settings.popups': 0,
    #   'download.prompt_for_download': False, 
    #   'download.directory_upgrade': True, 
    #   'safebrowsing.enabled': False, 
    #   'safebrowsing.disable_download_protection': True
    # }
    # chrome_opts.add_experimental_option('prefs', prefs)
    ##############################
    return applied_options

  @property
  def headless_mode(self):
    return all([
      self.headless, 
      self.disable_gpu,
    ])
  
  @headless_mode.setter
  def headless_mode(self, boolean: bool):
    if boolean:
      self.headless = self.disable_gpu = True
    else:
      del self.headless_mode

  @headless_mode.deleter
  def headless_mode(self):
    self.headless = self.disable_gpu = False

  @property
  def no_log_mode(self):
    return all([
      self.log_level == 3, 
      self.enable_logging, 
    ])
  
  @no_log_mode.setter
  def no_log_mode(self, boolean: bool):
    if boolean:
      self.log_level = 3
      self.enable_logging = True
    else:
      del self.no_log_mode

  @no_log_mode.deleter
  def no_log_mode(self):
    self.log_level = 0
    self.enable_logging = False

  @property
  def quick_mode(self):
    return all([
      self.headless_mode, 
      self.disable_images, 
      self.incognito, 
      self.disable_plugins, 
      self.no_log_mode, 
    ])
  
  @quick_mode.setter
  def quick_mode(self, boolean: bool):
    if boolean:
      self.headless_mode = True
      self.disable_images = True
      self.incognito = True
      self.disable_plugins = True
      self.no_log_mode = True
    else:
      del self.quick_mode
      
  @quick_mode.deleter
  def quick_mode(self):
    self.headless_mode = False
    self.disable_images = False
    self.incognito = False
    self.disable_plugins = False
    self.no_log_mode = False


class FirefoxOpts(BrowserOptions):
  def __init__(self) -> None:
    # https://blog.csdn.net/u010451638/article/details/109580906
    # https://blog.csdn.net/XianZhe_/article/details/120929106
    # Headless start (No GUI)
    self.headless = False
    # Disable GPU acceleration (recommended for headless)
    self.disable_gpu = False
    
    # Don't load images
    self.disable_images = False

  @property
  def applied(self) -> webdriver.FirefoxOptions:
    # https://developer.mozilla.org/en-US/docs/Web/WebDriver/Capabilities/firefoxOptions
    opts = webdriver.FirefoxOptions()
    if self.headless: 
      opts.add_argument('--headless')
    if self.disable_gpu:
      opts.add_argument('--disable-gpu')
    if self.disable_images:
      opts.set_preference('permissions.default.image',2)
      ##### or
      # firefox_opts.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})

    # Developer mode
    # opts.add_experimental_option('excludeSwitches', ['enable-automation'])

    # Window size can NOT be set by
    # firefox_opts.add_argument('window-size=500x500')
    # But can be set by, maybe can used to click that notice check box? Answer: NOPE!
    # self._driver.set_window_size(2000, 1000)
    return opts

  @property
  def headless_mode(self):
    return all([
      self.headless, 
      self.disable_gpu,
    ])

  @headless_mode.setter
  def headless_mode(self, boolean: bool):
    if boolean:
      self.headless = self.disable_gpu = True
    else:
      del self.headless_mode

  @headless_mode.deleter
  def headless_mode(self):
    self.headless = self.disable_gpu = False

  @property
  def quick_mode(self):
    return all([
      self.headless_mode, 
      self.disable_images, 
    ])

  @quick_mode.setter
  def quick_mode(self, boolean: bool):
    if boolean:
      self.headless_mode = True
      self.disable_images = True
    else:
      del self.quick_mode

  @quick_mode.deleter
  def quick_mode(self):
    self.headless_mode = False
    self.disable_images = False


class Browser:
  """
  Attributes
  ----------
  `_IMPLICITLY_TIMEOUT` : `float`, CONSTANT
    Sticky timeout to implicitly wait for an element to be found, or a 
    command to complete. Also the amount of time that the script should 
    wait during an `execute_async_script` call before throwing an error
  `_TIMEOUT` : `float`, CONSTANT
    Global timeout when find web elements
  `_POLL_MAX` : `int`, CONSTANT
    Maximun attempts to find a web elements
  `_POLL_FREQ` : `float`, CONSTANT
    Sleep interval between calls
  """
  supported_browsers = [ 'chrome', 'edge', 'firefox', 'safari' ]
  def __init__(self, name: str = '', url: str = '') -> None:
    ########## Necessary init begin
    self._IMPLICITLY_TIMEOUT = 0.1
    self._TIMEOUT = 0.2
    self._POLL_MAX = 4
    self._POLL_FREQ = self._TIMEOUT / self._POLL_MAX
    
    self._name = ''
    self._driver = None
    self._url = 'data:,'
    ########## Necessary init end
    self.name = name
    self.url = url

  def __del__(self) -> None:
    del self.driver

  def __repr__(self) -> str:
    args = [self.name, self.url]
    return "%s.%s(%s)" % (
      self.__class__.__module__, 
      self.__class__.__qualname__, 
      ", ".join(map(repr, args)), 
    )

  def __str__(self) -> str:
    return "%s(Name=%s, URL=%s)" % (
      self.__class__.__name__, 
      self.name, 
      self.url
    )

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    if not name:
      del self.name
      print(f"{self.__class__.__qualname__}: Warning! The browser name is not set!")
    else:
      name = str(name).lower()
      if self._name != name:
        self._name = name
        del self.driver
        if name == 'chrome':
          self.options = ChromeOpts()
          self.options.quick_mode = True
        elif name == 'firefox':
          self.options = FirefoxOpts()
          self.options.quick_mode = True
        elif name not in self.supported_browsers:
          raise BrowserNotSupportError(f"{name} is NOT a supported browser!")

  @name.deleter
  def name(self) -> None:
    self._name = ''
    del self.driver

  @property
  def driver(self) -> RemoteWebDriver:
    # If no active driver then create one
    if not self._driver:
      if self.name == 'chrome':
        self._driver = webdriver.Chrome(options=self.options.applied)
        ##############################
        # BUG (NOT FIXED): can't download picture in headless mode
        # https://sqa.stackexchange.com/questions/37459/how-to-download-in-headless-mode-with-selenium
        # https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        # https://github.com/shawnbutton/PythonHeadlessChrome/blob/master/driver_builder.py
        # https://github.com/SeleniumHQ/selenium/issues/5159
        # https://www.cnblogs.com/7749ha/p/9474949.html
        # https://www.jianshu.com/p/06269a22004d
        #############
        # add missing support for chrome "send_command" to selenium webdriver 
        # self._driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        # params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "D:\\russe\\Downloads"}} 
        # self._driver.execute("send_command", params=params)
        #############
        # params = {'behavior': 'allow', 'downloadPath': '/path/for/download'}
        # self._driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
        ##############################
      elif self.name == 'edge':
        self._driver = webdriver.Edge()
      elif self.name == 'firefox':
        self._driver = webdriver.Firefox(options=self.options.applied)
      elif self.name == 'safari':
        self._driver = webdriver.Safari()
      else:
        raise BrowserNotSupportError(f"{self.name} is NOT a supported browser!")
      # Set global implicityly wait timeout
      # https://blog.csdn.net/baidu_24030347/article/details/106744201
      self._driver.implicitly_wait(self._IMPLICITLY_TIMEOUT)
      self._driver.set_script_timeout(self._IMPLICITLY_TIMEOUT)
      self._wait = WebDriverWait(self._driver, self._TIMEOUT, self._POLL_FREQ)
    return self._driver

  @driver.deleter
  def driver(self) -> None:
    if isinstance(self._driver, RemoteWebDriver):
      # https://blog.csdn.net/idestina/article/details/88977322
      self._driver.close()
      # self._driver.quit()
    self._driver = None

  @property
  def url(self) -> str:
    return self._url

  @url.setter
  def url(self, url) -> None:
    if not url:
      del self.url
    else:
      self._url = str(url)

  @url.deleter
  def url(self) -> None:
    self._url = 'data:,'

  @property
  def wait(self) -> WebDriverWait:
    return self._wait
  
  @property
  def title(self) -> str:
    return self.driver.title

  @property
  def current_url(self) -> str:
    return self.driver.current_url

  @property
  def page_info(self) -> str:
    return "WebPage(Title= '%s', URL= '%s')" % (
      self.title, 
      self.current_url, 
    )

  @property
  def BY(self) -> By:
    """Set of supported locator strategies.

    Returns
    -------
    `By`

    """
    return By

  @property
  def EC(self) -> EC:
    """An alias of `expected_conditions`

    Canned "Expected Conditions" which are generally useful 
    within webdrivertests.
    """
    return self.expected_conditions

  @property
  def expected_conditions(self) -> EC:
    """
    Canned "Expected Conditions" which are generally useful 
    within webdrivertests.
    
    Aliased as `EC`
    """
    return EC

  @property
  def EX(self) -> EX:
    """An alias of `exceptions`

    Exceptions that may happen in all the webdriver code.
    """
    return self.exceptions
  
  @property
  def exceptions(self) -> EX:
    """Exceptions that may happen in all the webdriver code.
    
    Aliased as `EX`
    """
    return EX

  @property
  def KEYS(self) -> Keys:
    """
    Set of special keys codes.

    Returns
    -------
    `Keys`
      
    """
    return Keys

  @property
  def switch_to(self) -> SwitchTo:
    """
    Usage
    -----
    ```python
    element = browser.switch_to.active_element
    alert = browser.switch_to.alert
    browser.switch_to.default_content()
    browser.switch_to.frame('frame_name')
    browser.switch_to.frame(1)
    browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[0])
    browser.switch_to.parent_frame()
    browser.switch_to.window('main')
    ```

    Returns
    -------
    `SwitchTo`
      an object containing all options to switch focus into
    """
    return self.driver.switch_to

  @property
  def active_element(self) -> WebElement:
    return self.driver.switch_to.active_element

  def close(self) -> None:
    del self.driver

  def get(self, url: str = '') -> None:
    """Loads a web page in the current browser session.
    """
    if not url:
      url = self.url
    self.driver.get(url)

  def refresh(self) -> None:
    """Refreshes the current page.

    Usage
    -----
    ```python
    browser.refresh()
    ```
    """
    self.driver.refresh()

  def find_element(self, by: str = By.ID, value: None = None) -> WebElement:
    """Find an element given a By strategy and locator. 

    Usage
    -----
    ```python
    element = browser.find_element(By.ID, 'foo')
    ```

    Parameters
    ----------
    `by` : `str`

    `value` : `str`
    

    Returns
    -------
    `WebElement`

    """
    return self.driver.find_element(by, value)

  def find_elements(self, by: str = By.ID, value: None = None) -> list:
    """Find elements given a By strategy and locator. 

    Usage
    -----
    ```python
    element = broswer.find_element(By.ID, 'foo')
    ```

    Parameters
    ----------
    `by` : `str`

    `value` : `str`


    Returns
    -------
    `list(selenium.webdriver.remote.webelement.WebElement)`
    """
    return self.driver.find_elements(by, value)
    
  def wait_find_element(self, by: str = By.ID, value: None = None) -> WebElement:
    """Explicit wait when find an element by a `By` strategy and locator 
    through the WHOLE page
    
    Usage
    -----
    ```python
    browser.wait_find_element(By.ID, 'foo')
    ```

    Parameters
    ----------
    `by` : `str`
      
    `value` : `str`
      

    Returns
    -------
    `WebElement`

    """
    return self.wait.until(lambda d : d.find_element(by, value))
  
  def wait_find_elements(self, by: str = By.ID, value: None = None) -> list:
    """Explicit wait when find an element by a `By` strategy and locator 
    through the WHOLE page
    
    Usage
    -----
    ```python
    browser.wait_find_element(By.ID, 'foo')
    ```

    Parameters
    ----------
    `by` : `str`

    `value` : `str`


    Returns
    -------
    `list(WebElement)`

    """
    return self.wait.until(lambda d : d.find_elements(by, value))

  def wait_until(self, method, message: str = '') -> WebElement:
    """Fluent wait until expected conditions are `True`

    Calls the method provided with the driver as an argument until the return value is not False.

    Examples
    --------
    ```python
    EC = browser.EC
    browser.name = 'Firefox'
    browser.url = "http://somedomain/url_that_delays_loading"
    wait = WebDriverWait(brwoser.driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div")))
    ```
    
    For more examples: 
    https://www.selenium.dev/documentation/webdriver/waits/

    Parameters
    ----------
    `expected_condition` : `bool`
      One of classes of `selenium.webdriver.support.expected_conditions`

    Returns
    -------
    `WebElement`
    """
    return self.wait.until(method, message)

  def execute_js(self, script, *args) -> None:
    """Synchronously Executes JavaScript in the current window/frame.

    Usage
    -----
    ```python
    browser.execute_script('return document.title;')
    browser.execute_script("arguments[0].click();", self.ntc_cbx)
    ```

    Parameters
    ----------
    `script` : Any
      The JavaScript to execute.
    `*args` : Any
      Any applicable arguments for your JavaScript.
    """
    return self.driver.execute_script(script, args)

  def js_click(self, element: WebElement) -> None:
    """Click a webelement by executing JavaScript

    The `ElementNotInteractableException` may be raise if directly 
    click on some not visible elements. But JavaScript click may 
    solve this kind of situation in some cases. 

    Parameters
    ----------
    `element` : WebElement
      Element to be click
    """
    script="arguments[0].click();"
    self.execute_js(script, element)

  def _dev_print_active_element_info(self, propertys: list) -> None:
    prpts = propertys if propertys else [
      'class', 'id', 'type', 'value'
    ]
    for prpt in prpts:
      print(f"'{prpt}': '{self.active_element.get_property(prpt)}'")

  def _dev_click_test(self, element: WebElement) -> None:
    sum_msg = ''
    # try:
    #   # Re-get element and operate
    #   session.notice_checkbox = self.browser.wait_find_element(self.By.CSS_SELECTOR, '#read_already')
    #   session.notice_checkbox.send_keys(self.Keys.SPACE)
    # except Exception:
    #   print("Re-get failed")
    # else:
    #   print("Re-get success")
    # try:
    #   # Get by XPath
    #   session.notice_checkbox = self.browser.wait_find_element(self.By.XPATH, '//*[@id="read_already"]')
    #   session.notice_checkbox.send_keys(self.Keys.SPACE)
    # except Exception:
    #   print("XPath failed")
    # else:
    #   print("XPath success")
    try:
      # Click directly
      element.click()
    except Exception as e:
      print(f"Failed: click directly: {e}")
      sum_msg += 'f'
    else:
      print("Success: click directly")
      sum_msg += '.'
    try:
      # Directly press enter
      element.send_keys(self.KEYS.ENTER)
    except Exception as e:
      print(f"Failed: press ENTER key: {e}")
      sum_msg += 'f'
    else:
      print("Success: press ENTER key: 'el.send_keys(Keys.ENTER)'")
      sum_msg += '.'
    try:
      # Directly press space
      element.send_keys(self.KEYS.SPACE)
    except Exception as e:
      print(f"Failed: press SPACE key: {e}")
      sum_msg += 'f'
    else:
      print("Success: press SPACE key: 'el.send_keys(Keys.SPACE)'")
      sum_msg += '.'
    try:
      # Operate using JavaScript
      self.execute_js("arguments[0].click();", element)
    except Exception as e:
      print(f"Failed: click using JavaScript: {e}")
      sum_msg += 'f'
    else:
      print('Success: click using JavaScript')
      sum_msg += '.'
    print(f"\n{sum_msg}")
