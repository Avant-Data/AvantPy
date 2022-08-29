import avantpy

jsonD = avantpy.Transfer(json = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
                         obj = 'vulnerabilities',
                         name = 'cisakevs_teste',
                         baseurl = 'https://avantnightly.avantsec.com.br/'
                         )