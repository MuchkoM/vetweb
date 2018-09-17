import sys

import django

print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())
if 'setup' in dir(django):
    django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
permission = Permission.objects.create(codename='can_publish',
                                       name='Can Publish Posts',
                                       content_type=content_type)
user = User.objects.get(username='duke_nukem')
group = Group.objects.get(name='wizard')
group.permissions.add(permission)
user.groups.add(group)
