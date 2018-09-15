from django.test import TestCase

from . import models


class ContactTests(TestCase):
    """Contact model tests."""

    def test_owner_str(self):
        owner = models.Owner(fio='Мучко М. В.', address='Минск Руссиянова 50')
        self.assertEquals(
            str(owner),
            'Мучко М. В. Минск Руссиянова 50',
        )
