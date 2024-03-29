import requests
import socket
import json
from typing import Any, Optional
import logging
from urllib3.exceptions import InsecureRequestWarning

class Memory:
    """Memory Storage Uploader

    A class to manage storage of data in memory

    Args:
        key (str): The unique identifier for the data to be stored
        value (Any): The data to be stored in memory
        baseurl (str, optional): Base URL to execute the memory storage request
        expire (int, optional): Time (in seconds) before the stored data expires (default: 3600)
        api (str, optional): Endpoint for the memory storage API
        verify_SSL (bool, optional): Bool to verify SSL of requests

    Attributes:
        key (str): The unique identifier for the data to be stored
        value (Any): The data to be stored in memory
        baseurl (str): Base URL to execute the memory storage request
        expire (int): Time (in seconds) before the stored data expires
        api (str): Endpoint for the memory storage API
        verify_SSL (bool): Bool to verify SSL of requests
        log (logger): Logger with __name__
        url (str): Default to join the url path with api path

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> memory = Memory(key="example_key", value={"example": "data"})
        >>> memory.upload()
        INFO:memory.Memory:Memory store response status for example_key indexing: 200
    """

    def __init__(self,
                 key: str,
                 value: Any,
                 baseurl: Optional[str] = '',
                 expire: Optional[int] = 3600,
                 api: Optional[str] = '/avantapi/2.0/avantData/avantMem/index',
                 verify_SSL: Optional[str] = False,
                 **kwargs):
        self.key = key
        self.value = value
        self.baseurl = self.get_url(baseurl)
        self.expire = expire
        self.api = api
        self.verify_SSL = verify_SSL
        self.log = logging.getLogger(__name__)
        self.url = kwargs.get('url', self.baseurl+self.api)
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        
    def __repr__(self):
        return 'Data of type {} in memory as {}:\n{}'.format(type(self.value), self.key)

    def upload(self):
        if not isinstance(self.value, (list, set, tuple)):
            self.value = [self.value]
        payload = {
            'key': self.key,
            'value': str(self.value),
            'expire': self.expire
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), verify=self.verify_SSL)
            self.log.info('Memory store response status for {} indexing: {}'.format(self.key, response.status_code))
            self.log.debug(response.text)
        except Exception:
            self.log.error('Error indexing {} in memory.'.format(self.key), exc_info=True)

    def get_url(self, url: str) -> str:
        """This function returns a URL string.
        
        If the `url` argument is not empty, the function simply returns it.
        
        If the `url` argument is empty, the function creates a UDP socket and connects to the IP address and port
        of Google's public DNS server (8.8.8.8 on port 80) to get the IP address of the host. It then formats the IP
        address as a string and returns it with the `https://` protocol prefix.
        
        Args:
            url: string representing the URL that the function will try to retrieve.
        
        Returns:
            str: The URL to use for API requests.
        """
        if not url:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
            s.close()
            return 'https://{}'.format(host_ip)
        return url