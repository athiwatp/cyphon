# -*- coding: utf-8 -*-
# Copyright 2017 Dunbar Security Solutions, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""
Tests Alert filters.
"""

# third party
from django.http.request import QueryDict
from django.test import TestCase

# local
from alerts.models import Alert
from alerts.views import AlertFilter
from tags.models import Tag
from tests.fixture_manager import get_fixtures


class AlertFilterTestCase(TestCase):
    """

    """
    fixtures = get_fixtures(['alerts', 'comments', 'tags'])

    @classmethod
    def setUpClass(cls):
        super(AlertFilterTestCase, cls).setUpClass()
        query = QueryDict('content=threat')
        cls.alerts = Alert.objects.all()
        cls.alert_filter = AlertFilter(query, cls.alerts)

    def test_no_value(self):
        """
        Tests the filter_by_content method when no value is provided.
        """
        value = ''
        actual = self.alert_filter.filter_by_content(self.alerts, '', value)
        expected = self.alerts
        self.assertEqual(actual, expected)

    def test_filter_by_content_data(self):
        """
        Tests the filter_by_content function for a typical QuerySet and
        value.
        """
        val = 'user@example.com'
        filtered_alerts = self.alert_filter.filter_by_content(self.alerts, '', val)
        self.assertEqual(filtered_alerts.count(), 1)
        self.assertEqual(filtered_alerts[0].pk, 2)

    def test_filter_by_content_title(self):
        """
        Tests the filter_by_content function for a value appearing in an
        Alert title.
        """
        val = 'acme'
        filtered_alerts = self.alert_filter.filter_by_content(self.alerts, '', val)
        self.assertEqual(filtered_alerts.count(), 3)

    def test_filter_no_tags(self):
        """
        Tests the filter_by_content function for a value appearing in
        Alert content.
        """
        val = ''
        actual = self.alert_filter.filter_by_content(self.alerts, '', val)
        expected = self.alerts
        self.assertEqual(actual, expected)

    def test_filter_by_alert_tags(self):
        """
        Tests the filter_by_tags function associated with an Alert.
        """
        val = Tag.objects.filter(name='bird')
        filtered_alerts = self.alert_filter.filter_by_tags(self.alerts, '', val)
        self.assertEqual(filtered_alerts.count(), 1)
        self.assertEqual(filtered_alerts[0].pk, 3)

    def test_filter_by_comment_tags(self):
        """
        Tests the filter_by_tags function associated with a Comment.
        """
        val = Tag.objects.filter(name='dog')
        filtered_alerts = self.alert_filter.filter_by_tags(self.alerts, '', val)
        self.assertEqual(filtered_alerts.count(), 1)
        self.assertEqual(filtered_alerts[0].pk, 3)

    def test_filter_by_analysis_tags(self):
        """
        Tests the filter_by_tags function associated with an Analysis.
        """
        val = Tag.objects.filter(name='turtle')
        filtered_alerts = self.alert_filter.filter_by_tags(self.alerts, '', val)
        self.assertEqual(filtered_alerts.count(), 1)
        self.assertEqual(filtered_alerts[0].pk, 3)
