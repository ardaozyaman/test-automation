from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from typing import Dict, Any, Optional, Union, List, Callable
from functools import lru_cache
import hashlib
import json
from queue import Queue
import threading

class ChromeDriver(webdriver.Chrome):
    _instance = None
    
    def __init__(
        self,
        headless: bool = False,
        disable_gpu: bool = False,
        start_maximized: bool = True,
        incognito: bool = False,
        window_size: tuple = (1920, 1080),
        disable_extensions: bool = True,
        disable_notifications: bool = True,
        disable_popup_blocking: bool = True,
        disable_web_security: bool = True,
        hide_scrollbars: bool = False,
        ignore_certificate_errors: bool = True,
        custom_prefs: Optional[Dict[str, Any]] = None,
        proxy: Optional[Dict[str, str]] = None,
        network_conditions: Optional[Dict[str, Union[int, bool]]] = None,
        bypass_urls: Optional[list] = None,
        interceptor: Optional[Dict[str, Any]] = None,
        implicit_wait: int = 0
    ):
        # Initialize config first
        self.config = {
            'headless': headless,
            'disable_gpu': disable_gpu,
            'start_maximized': start_maximized,
            'incognito': incognito,
            'window_size': window_size,
            'disable_extensions': disable_extensions,
            'disable_notifications': disable_notifications,
            'disable_popup_blocking': disable_popup_blocking,
            'disable_web_security': disable_web_security,
            'hide_scrollbars': hide_scrollbars,
            'ignore_certificate_errors': ignore_certificate_errors,
            'custom_prefs': custom_prefs or {},
            'proxy': proxy,
            'network_conditions': network_conditions or {
                'offline': False,
                'latency': 0,
                'download_throughput': -1,
                'upload_throughput': -1
            },
            'bypass_urls': bypass_urls or [],
            'interceptor': interceptor or {},
            'implicit_wait': implicit_wait
        }
        
        # Create options and service
        options = self._setup_chrome_options()
        service = Service()
        
        # Initialize parent Chrome class
        super().__init__(options=options, service=service)
        
        # Set implicit wait
        self.implicitly_wait(implicit_wait)
        
        # Initialize the _driver attribute
        self._driver = None
        
        self._request_queue = Queue()
        self._network_listener_active = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChromeDriver, cls).__new__(cls)
        return cls._instance

    def _get_config_hash(self) -> str:
        config_str = json.dumps(self.config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()

    @lru_cache(maxsize=1)
    def _create_driver(self, config_hash: str) -> webdriver.Chrome:
        options = self._setup_chrome_options()
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(self.config['implicit_wait'])  # Set implicit wait
        return driver

    def _setup_chrome_options(self) -> Options:
        chrome_options = Options()
        
        # Performance Options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if self.config['disable_gpu']:
            chrome_options.add_argument('--disable-gpu')
        if self.config['disable_extensions']:
            chrome_options.add_argument('--disable-extensions')
        
        # Browser Behavior
        if self.config['headless']:
            chrome_options.add_argument('--headless=new')
        if self.config['start_maximized']:
            chrome_options.add_argument('--start-maximized')
        if self.config['incognito']:
            chrome_options.add_argument('--incognito')
        if self.config['disable_popup_blocking']:
            chrome_options.add_argument('--disable-popup-blocking')
        if self.config['disable_notifications']:
            chrome_options.add_argument('--disable-notifications')
        
        # Window Settings
        chrome_options.add_argument(f'--window-size={self.config["window_size"][0]},{self.config["window_size"][1]}')
        if self.config['hide_scrollbars']:
            chrome_options.add_argument('--hide-scrollbars')
        
        # Network & Security
        if self.config['ignore_certificate_errors']:
            chrome_options.add_argument('--ignore-certificate-errors')
        if self.config['disable_web_security']:
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-web-security')
        
        # Proxy Configuration
        if self.config['proxy']:
            chrome_options.add_argument(f'--proxy-server={self.config["proxy"].get("server")}')
            if self.config['proxy'].get('bypass_list'):
                bypass_list = ','.join(self.config['proxy']['bypass_list'])
                chrome_options.add_argument(f'--proxy-bypass-list={bypass_list}')

        return chrome_options

    def __call__(self) -> webdriver.Chrome:
        config_hash = self._get_config_hash()
        if not self._driver:
            self._driver = self._create_driver(config_hash)
            self._setup_network_conditions()
        return self._driver

    def _setup_network_conditions(self):
        """Setup network conditions and request logging"""
        self._driver.execute_cdp_cmd('Network.enable', {})
        
        if self.config['network_conditions']:
            self._driver.execute_cdp_cmd('Network.emulateNetworkConditions', 
                self.config['network_conditions']
            )

        if self.config['interceptor']:
            self._driver.execute_cdp_cmd('Network.setRequestInterception', {
                'patterns': self.config['interceptor'].get('patterns', [])
            })

    def set_network_conditions(self, 
                             latency: int = 0, 
                             download_throughput: int = -1,
                             upload_throughput: int = -1,
                             offline: bool = False):
        """Dynamically update network conditions"""
        if self._driver:
            conditions = {
                'offline': offline,
                'latency': latency,
                'downloadThroughput': download_throughput,
                'uploadThroughput': upload_throughput
            }
            self._driver.execute_cdp_cmd('Network.emulateNetworkConditions', conditions)

    def start_network_logging(self):
        """Start logging network requests"""
        if not self._network_listener_active:
            self._network_listener_active = True
            self._driver.execute_cdp_cmd('Network.enable', {})
            
            def request_handler(request):
                self._request_queue.put({
                    'url': request.get('request', {}).get('url'),
                    'method': request.get('request', {}).get('method'),
                    'headers': request.get('request', {}).get('headers'),
                    'timestamp': request.get('timestamp'),
                    'type': request.get('type')
                })

            self._driver.execute_cdp_cmd('Network.responseReceived', lambda x: request_handler(x))
            self._driver.execute_cdp_cmd('Network.requestWillBeSent', lambda x: request_handler(x))

    def stop_network_logging(self):
        """Stop logging network requests"""
        if self._network_listener_active:
            self._network_listener_active = False
            self._driver.execute_cdp_cmd('Network.disable', {})

    def get_network_requests(self):
        """Get all captured network requests"""
        requests = []
        while not self._request_queue.empty():
            requests.append(self._request_queue.get())
        return requests

    def quit(self):
        if self._driver:
            self.stop_network_logging()
            self._driver.quit()
            self._driver = None
            self._create_driver.cache_clear()