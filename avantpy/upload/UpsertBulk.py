from urllib3.exceptions import InsecureRequestWarning
from collections import Counter
import concurrent.futures
import socket
import logging
import requests
import json
from typing import Optional, Union, List, Tuple, Set, Any


class UpsertBulk:
    """Bulk Uploader

    A class to manage bulk uploads of data

    Args:
        data (list(dict)): List of dictionaries to be indexed [{"id":..., "index":..., "type":..., ...},...]
        baseurl (str, optional): Baseurl to execute the upsert bulk 
        api (str, optional): Endpoint where the connection with database is set
        cluster (str, optional): Header parameter for communication with the api
        verify_SSL (bool, optional): Bool to verify SSL of requests
        chunk_size (int, optional): Number of documents to send in each bulk requests
        threads (int, optional): Number of threads to send each chunk of documents
        url (str, optional): Default to join the url path with api path

    Attributes:
        data (list(dict)): List of dictionaries to be indexed [{"id":..., "index":..., "type":..., ...},...]
        updated (int): Number of documents successfully updated
        created (int): Number of documents successfully created
        failed (int): Number of documents that failed indexing
        errors (dict): Dict subclass for counting hashable objects from collections (Counter)
        log (logger): Logger with __name__
        baseurl (str): Baseurl to execute the upsert bulk 
        api (str): Endpoint where the connection with database is set
        cluster (str): Header parameter for communication with the api
        verify_SSL (bool): Bool to verify SSL of requests
        chunk_size (int): Number of documents to send in each bulk requests
        threads (int): Number of threads to send each chunk of documents
        url (str): Default to join the url path with api path

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> import avantpy
        >>> dataList = []
        >>> dataList.append({'id':'6fee099da7dfbb67599d7fa7389de898', 'type':'test', 'index':'test', 'testKey': 'firstValue'})
        >>> dataList.append({'id':'58f77dcc14a41b2984e298e86db85c73', 'type':'test', 'index':'test', 'testKey': 'secondValue'})
        >>> dataList.append({'id':'ed23fa12819a63198b5c0b171ebbbf2d', 'type':'test', 'index':'test', 'testKey': 'thirdValue'})
        >>> avantpy.upload.UpsertBulk(dataList, baseurl='https://192.168.102.133/')
        INFO:avantpy.upload.UpsertBulk:Total: 3
        INFO:avantpy.upload.UpsertBulk:Updated: 0, Created: 3. 
        INFO:avantpy.upload.UpsertBulk:3 successfully executed with 0 failures
        INFO:avantpy.upload.UpsertBulk: Created: 3 / Updated: 0 / Failed: 0
    """

    def __init__(self,
                 data: Union[List[dict], Tuple[dict], Set[dict]],
                 baseurl: Optional[str] = '',
                 api: Optional[str] = '/avantapi/avantData/index/bulk/general/upsert',
                 cluster: Optional[str] = 'AvantData',
                 verify_SSL: Optional[bool] = False,
                 chunk_size: Optional[int] = 1000,
                 threads: Optional[int] = 1,
                 **kwargs: Any):
        self.log = logging.getLogger(__name__)
        self.baseurl = self.getUrl(baseurl)
        self.api = api
        self.cluster = cluster
        self.verify_SSL = verify_SSL
        self.chunk_size = chunk_size
        self.threads = threads
        self.data = data
        self.url = kwargs.get('url', self.baseurl+self.api)
        self.updated, self.created, self.failed = (0, 0, 0)
        self.errors = Counter()
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)

    def __repr__(self):
        return '{} documents ready to be uploaded to {}. Use upload() method to upload'.format(len(self.data), self.baseurl)

    def chunkSend(self, chunk: Union[List[dict], Tuple[dict], Set[dict]]):
        """Sends a chunk of data to be indexed into the Elasticsearch cluster.

        Args:
            chunk (list(dict) or tuple(dict) or set(dict)): A list of dictionaries to be indexed.

        The function sends a chunk of data to be indexed into the Elasticsearch cluster by making a PUT request
        to the Elasticsearch server. The data is sent as a JSON object in the request body, and the 'cluster' header 
        is set to the cluster name provided during object instantiation.

        The function then processes the response returned from the Elasticsearch server. It updates the 'updated'
        and 'created' counters based on the number of documents that were updated and created, respectively. If there
        were any errors during indexing, the function updates the 'errors' dictionary with the count of errors
        encountered, along with the reason for each error.
        """
        json_to_send = {'body': json.loads(json.dumps(chunk))}
        headers = {'cluster': self.cluster}
        response_bulk = requests.put(url=self.url,
                                    headers=headers,
                                    data=json.dumps(json_to_send),
                                    verify=self.verify_SSL)
        try:
            response_json = json.loads(response_bulk.text)
            if response_json.get('items'):
                results = Counter(item.get('update').get('result')
                                  for item in response_json.get('items'))
                self.updated += results.get('updated', 0)
                self.created += results.get('created', 0)
                if response_json.get('errors'):
                    self.errors.update(Counter(item.get('update').get('error').get(
                        'reason') for item in response_json.get('items') if item.get('update').get('error')))
                self.log.info('Updated: {}, Created: {}. '.format(
                    self.updated, self.created))
        except Exception as e:
            self.log.warning(response_bulk.text)
            self.log.error(e)

    def upload(self):
        """This function uploads data in chunks and returns a status message.
        
        If the `data` attribute of the object is not empty, the function logs the total number of items in the `data`
        list, and splits the list into chunks (of size `chunk_size`) for concurrent processing using threads (number of
        threads is `threads`).
        
        If `threads` is greater than 1, the function uses `concurrent.futures.ThreadPoolExecutor` to execute the
        `chunkSend` method on the chunks concurrently. If `threads` is 1 or less, the function executes the `chunkSend`
        method on each chunk sequentially.
        
        If there were any errors during execution, the function logs the reasons for the failures along with the number
        of items that failed.
        
        The function logs the number of items that were created and updated successfully, as well as the number of items
        that failed.
        
        Returns:
            A string representing the status of the upload operation. The string logs the total number of items in the `data`
        list, the number of items that were created and updated successfully, as well as the number of items that failed.
        """
        if self.data:
            self.log.info('Total: {}'.format(len(self.data)))
            chunks = [self.data]
            if len(self.data) > self.chunk_size:
                chunks = [self.data[x:x+self.chunk_size]
                          for x in range(0, len(self.data), self.chunk_size)]
            if self.threads > 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                    executor.map(self.chunkSend, chunks)
            else:
                for chunk in chunks:
                    self.chunkSend(chunk)
            if self.errors:
                self.failed += sum(self.errors.values())
                for k, v in self.errors.items():
                    self.log.warning('{} failed. Reason: {}'.format(v, k))
            self.log.info('{} successfully executed with {} failures'.format(
                self.updated+self.created, self.failed))
            self.log.info('Created: {} / Updated: {} / Failed: {}'.format(self.created, self.updated, self.failed))
        else:
            self.log.info('Empty list')

    def getUrl(self, url: str) -> str:
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