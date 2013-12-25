from django.test.testcases import TestCase
from factory_boy import MentionFactory
from ..models import Mention

class MentionModelTestCase(TestCase):
    def test_mention(self):
        """Test mention object can be created"""
        mention = MentionFactory.create()
        self.assertIsNotNone(mention.user)
        self.assertIsNotNone(mention.message)
        self.assertIsNone(mention.in_reply_to)
        self.assertFalse(mention.is_read)

    def test_unicode(self):
        """Test __unicode__() returns correct name"""
        mention = MentionFactory.create()
        self.assertEqual(unicode(mention), unicode(mention.message))

    def test_meta(self):
        """Test Meta class returns correct values"""
        self.assertEqual(Mention._meta.verbose_name.title(), 'Mention')
        self.assertEqual(Mention._meta.verbose_name_plural.title(), 'Mentions')
