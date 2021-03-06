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
Defines classes for handling API keys and API call counts.
"""

# third party
from django.db import models

# local
from ambassador.emissaries.models import Emissary, EmissaryManager
from responder.actions.models import Action


class Courier(Emissary):
    """
    Handles an API key or token (KeySet) for a set of users of a Pipe.
    Uses a Meter to keep track of the number of calls made using that API key.
    """
    endpoints = models.ManyToManyField(
        Action,
        verbose_name='actions',
        related_name='emissaries',
        related_query_name='emissary'
    )

    objects = EmissaryManager()

