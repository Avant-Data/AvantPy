import avantpy
API_END_OF_LIFE = 'https://endoflife.date/api/'

try:
    allAPIs = avantpy.download.JSON(API_END_OF_LIFE+'all.json').data
except Exception:
    allAPIs = ['almalinux', 'alpine', 'amazon-eks', 'amazon-linux', 'android',
               'angular', 'ansible', 'apache', 'apache-airflow', 'api-platform',
               'azure-devops', 'blender', 'bootstrap', 'centos', 'cfengine',
               'citrix-vad', 'coldfusion', 'composer', 'consul', 'cortexxdr',
               'couchbase-server', 'debian', 'django', 'docker-engine', 'dotnet',
               'dotnetfx', 'drupal', 'drush', 'elasticsearch', 'electron', 'elixir',
               'emberjs', 'esxi', 'fedora', 'ffmpeg', 'filemaker', 'firefox', 'fortios',
               'freebsd', 'gitlab', 'go', 'godot', 'google-kubernetes-engine', 'haproxy',
               'hashicorp-vault', 'hbase', 'horizon', 'intel-processors', 'internet-explorer',
               'iphone', 'java', 'jquery', 'kde-plasma', 'kindle', 'kotlin', 'kubernetes',
               'laravel', 'lineageos', 'linux', 'linuxmint', 'log4j', 'looker',
               'macos', 'magento', 'mariadb', 'mediawiki', 'mongodb', 'moodle',
               'msexchange', 'mssqlserver', 'mysql', 'nextcloud', 'nginx', 'nix',
               'nixos', 'nodejs', 'nokia', 'nomad', 'nvidia', 'nvidia-gpu',
               'office', 'openbsd', 'opensearch', 'openssl', 'opensuse',
               'openzfs', 'oraclelinux', 'pangp', 'panos', 'perl', 'php',
               'pixel', 'postfix', 'postgresql', 'powershell', 'python',
               'qt', 'rabbitmq', 'rails', 'react', 'readynas', 'redis',
               'rhel', 'rocky-linux', 'ros', 'roundcube', 'ruby', 'samsung-mobile',
               'sharepoint', 'sles', 'solr', 'splunk', 'spring-framework',
               'surface', 'symfony', 'tarantool', 'tomcat', 'ubuntu',
               'unity', 'unrealircd', 'varnish', 'visualstudio', 'vue', 'wagtail',
               'windows', 'windowsembedded', 'windowsserver', 'wordpress', 'yocto', 'zabbix', 'zookeeper']

dataList = []

for api in allAPIs:
    try:
        productInfo = avantpy.download.JSON(API_END_OF_LIFE+api+'.json').data
        productInfo = avantpy.utils.add(productInfo,
                                        product=api)
        dataList.extend(productInfo)
    except Exception as e:
        pass


def dateOrNone(value):
    try:
        return avantpy.utils.dateToEpochMillis(value)
    except Exception:
        return {'.*': ''}


dataList = avantpy.utils.edit(dataList,
                              entire={
                                  'releaseDate': dateOrNone,
                                  'support': dateOrNone,
                                  'eol': dateOrNone,
                                  'latestReleaseDate': dateOrNone,
                                  'discontinued': dateOrNone
                              })
dataList = avantpy.utils.edit(dataList,
                              values=avantpy.utils.removeEmpty
                              )
avantpy.upload.Template(name='end_of_life',
                        aliases='TWI',
                        template=dataList,
                        baseurl='https://prod.avantdata.com.br/',
                        typeMap={
                            'releaseDate': 'date',
                            'support': 'date',
                            'eol': 'date',
                            'latestReleaseDate': 'date',
                            'discontinued': 'date'
                        }
                        )
dataList = avantpy.utils.add(dataList,
                             type='end_of_life',
                             index='end_of_life',
                             id=avantpy.utils.generateID,
                             )

avantpy.upload.UpsertBulk(dataList,
                          baseurl='https://prod.avantdata.com.br/'
                          )
