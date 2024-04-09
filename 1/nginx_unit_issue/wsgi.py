import os
import pwd


# if 'VCAP_OVERRIDE' in os.environ:
#     uid=pwd.getpwnam('vcap')[2]
#     os.setuid(uid)
#     os.environ['HOME'] = '/home/vcap'


from nginx_unit_issue.__main__ import issues_api
application = issues_api
