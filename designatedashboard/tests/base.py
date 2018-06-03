# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

import fixtures
import testtools

from openstack_dashboard.test import helpers as test

from designatedashboard.dashboards.project.dns_domains import forms


_TRUE_VALUES = ('True', 'true', '1', 'yes')


class TestCase(testtools.TestCase):

    """Test case base class for all unit tests."""
    use_mox = False

    def setUp(self):
        """Run before each test method to initialize test environment."""

        super(TestCase, self).setUp()
        test_timeout = os.environ.get('OS_TEST_TIMEOUT', 0)
        try:
            test_timeout = int(test_timeout)
        except ValueError:
            # If timeout value is invalid do not set a timeout.
            test_timeout = 0
        if test_timeout > 0:
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))

        self.useFixture(fixtures.NestedTempfile())
        self.useFixture(fixtures.TempHomeDir())

        if os.environ.get('OS_STDOUT_CAPTURE') in _TRUE_VALUES:
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if os.environ.get('OS_STDERR_CAPTURE') in _TRUE_VALUES:
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        self.log_fixture = self.useFixture(fixtures.FakeLogger())


class BaseRecordFormCleanTests(test.TestCase):

    DOMAIN_NAME = 'foo.com.'
    HOSTNAME = 'www'
    use_mox = False

    MSG_FIELD_REQUIRED = 'This field is required'
    MSG_INVALID_HOSTNAME = 'Enter a valid hostname. The '\
                           'hostname should contain letters '\
                           'and numbers, and be no more than '\
                           '63 characters.'
    MSG_INVALID_HOSTNAME_SHORT = 'Enter a valid hostname'

    def setUp(self):
        super(BaseRecordFormCleanTests, self).setUp()

        # Request object with messages support
        self.request = self.factory.get('', {})

        # Set-up form instance
        kwargs = {}
        kwargs['initial'] = {'domain_name': self.DOMAIN_NAME}
        self.form = forms.RecordCreate(self.request, **kwargs)
        self.form._errors = {}
        self.form.cleaned_data = {
            'domain_name': self.DOMAIN_NAME,
            'name': '',
            'data': '',
            'txt': '',
            'priority': None,
            'ttl': None,
        }

    def assert_no_errors(self):
        self.assertEqual(self.form._errors, {})

    def assert_error(self, field, msg):
        self.assertIn(msg, self.form._errors[field])

    def assert_required_error(self, field):
        self.assert_error(field, self.MSG_FIELD_REQUIRED)
