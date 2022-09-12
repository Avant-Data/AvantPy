import avantpy

import logging
logging.basicConfig(level=logging.INFO)

SE = avantpy.download.Search('https://avantnightly.avantsec.com.br/', index='IANA', format=True)


print(SE.data[50:60])