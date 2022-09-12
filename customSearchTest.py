import avantpy

import logging
logging.basicConfig(level=logging.DEBUG)

SE = avantpy.download.Search('https://avantnightly.avantsec.com.br/', index='IANA', size=10)

print(SE.data)