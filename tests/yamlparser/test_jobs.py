# Joint copyright:
#  - Copyright 2012,2013 Wikimedia Foundation
#  - Copyright 2012,2013 Antoine "hashar" Musso
#  - Copyright 2013 Arnaud Fabre
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
from operator import attrgetter
from pathlib import Path
import sys

import pytest

from tests.enum_scenarios import scenario_list


fixtures_dir = Path(__file__).parent / "job_fixtures"


@pytest.fixture(
    params=scenario_list(fixtures_dir),
    ids=attrgetter("name"),
)
def scenario(request):
    return request.param


def test_yaml_snippet(scenario, check_job):
    old_path = sys.path
    if str(fixtures_dir) not in sys.path:
        sys.path.append(str(fixtures_dir))
    # Some tests using config with 'include_path' expect JJB root to be current directory.
    os.chdir(Path(__file__).parent / "../..")
    if scenario.name.startswith("deprecated-"):
        with pytest.warns(UserWarning) as record:
            check_job()
        assert "is deprecated" in str(record[0].message)
    else:
        check_job()
    sys.path = old_path
