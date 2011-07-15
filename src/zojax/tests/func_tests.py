### -*- coding: utf-8 -*- ####################################################

import os
import tempfile

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail

from zojax.models import Document

class ZojaxTest(TestCase):

    fixtures = ["test",]

    def setUp(self):
        if self.client.login(username="admin", password="admin"):
            self.user = User.objects.get(username="admin")
        self.fname = tempfile.mkstemp()[1]
        file = open(self.fname, "w")
        file.write("Some Test Content")
        file.close()
        file = open(self.fname, "r")
        self.document = Document(user=self.user, title="Some title")
        self.document.file = SimpleUploadedFile(file.name, file.read())
        file.close()
        self.document.save()


    def test_upload(self):
        """Test upload view and form works correct"""

        file = open(self.fname, "r")
        response = self.client.post(reverse("index"),
                                    {'name': os.path.basename(self.fname),
                                     'file': file})
        file.close()
        # Check the Ok status
        self.assertEqual(response.status_code, 200)
        # Does response contain info about file (at least its name):
        self.assertContains(response, os.path.basename(self.fname))

    def test_ajax_index(self):
        """Test the index page return JSON data if request is AJAX"""
        response = self.client.get(reverse("index"),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check the Ok status
        self.assertEqual(response.status_code, 200)
        # Check content type
        self.assertEqual(response["Content-Type"],
                         'application/json; charset=utf-8')

    def test_share(self):
        """Test sharing the document"""
        message = "I think you may be interested in it."
        #mail
        # Check empty outbox
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse("share_document", args=[self.document.id,]),
                                    {'email': "test@example.com",
                                     'message': message})
        # Check outbox has email
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # check message in email
        assert message in email.body


    def test_ajax_delete(self):
        """Test the delete view"""
        assert hasattr(self, "user")

        id = self.document.id
        response = self.client.get(reverse("remove_document", args=[self.document.id,]),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check the Ok status
        self.assertEqual(response.status_code, 200)
        # Check that deleted is True
        self.assertEqual(response.content, 'true')
        # Check document doesn't exist
        self.assertRaises(Document.DoesNotExist, Document.objects.filter(id=id)[:1].get)

    def tearDown(self):
        os.remove(self.fname)
