#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2024, Arm Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Module is testing if all JSON schemas `wperf` emits match given schemas."""
import json
import os
import pytest
from jsonschema import validate
from common import run_command, get_schema
from common import wperf_metric_is_available

### Test cases

@pytest.mark.parametrize("scheme_name", [ "version", "list", "test", "stat", "detect", "man" ])
def test_wperf_json_schema(request, tmp_path, scheme_name):
    """ Test `wperf` JSON output against scheme """
    test_path = os.path.dirname(request.path)
    file_path = tmp_path / 'test.json'
    cmd_type = ""
    if "version" in scheme_name:
        cmd_type = "--version"
    elif "list" in scheme_name:
        cmd_type = "list"
    elif "test" in scheme_name:
        cmd_type = "test"
    elif "detect" in scheme_name:
        cmd_type = "detect"
    elif "stat" in scheme_name:
        cmd_type = "stat -e cpu_cycles sleep 1"
    elif "man" in scheme_name:
        cmd_type = "man neoverse-n1/Miss_Ratio"
    cmd = f'wperf {cmd_type} --output'
    _, _ = run_command(cmd.split() + [str(file_path)])

    with open(str(file_path)) as json_file:
        json_output = json.loads(json_file.read())
    try:
        validate(instance=json_output, schema=get_schema(scheme_name, test_path))
    except:
        assert False
    assert True

@pytest.mark.parametrize("scheme_name", [ "version", "list", "test", "stat", "detect", "man" ])
def test_wperf_json_stdout_schema(request, tmp_path, scheme_name):
    """ Test `wperf` JSON output against scheme """
    test_path = os.path.dirname(request.path)
    file_path = tmp_path / 'test.json'
    cmd_type = ""
    if "version" in scheme_name:
        cmd_type = "--version"
    elif "list" in scheme_name:
        cmd_type = "list"
    elif "test" in scheme_name:
        cmd_type = "test"
    elif "detect" in scheme_name:
        cmd_type = "detect"
    elif "stat" in scheme_name:
        cmd_type = "stat -e cpu_cycles sleep 1"
    elif "man" in scheme_name:
        cmd_type = "man neoverse-n1/Miss_Ratio"
    cmd = f'wperf {cmd_type} --json'
    stdout, _ = run_command(cmd.split())

    json_output = json.loads(stdout)

    try:
        validate(instance=json_output, schema=get_schema(scheme_name, test_path))
    except:
        assert False
    assert True

def test_wperf_timeline_json_schema(request, tmp_path):
    """ Test `wperf stat -t` aka timeline JSON output against scheme """
    test_path = os.path.dirname(request.path)
    file_path = tmp_path / 'test.json'

    cmd = "wperf stat -m imix -t -i 1 -n 2 --timeout 1 --json --output"
    _, _ = run_command(cmd.split() + [str(file_path)])

    json_output = {}

    try:
        with open(str(file_path)) as json_file:
            json_output = json.loads(json_file.read())
        validate(instance=json_output, schema=get_schema("timeline", test_path))
    except Exception as err:
        assert False, f"Unexpected {err=}, {type(err)=}"

    for stat in json_output["timeline"]:
        try:
            validate(instance=stat, schema=get_schema("stat", test_path))
        except Exception as err:
            assert False, f"Unexpected {err=}, {type(err)=}"
        assert True

def test_wperf_timeline_json_stdout_schema(request, tmp_path):
    """ Test `wperf stat -t` aka timeline JSON output against scheme """
    test_path = os.path.dirname(request.path)

    cmd = 'wperf stat -m imix -t -i 1 -n 2 --timeout 1 --json'
    stdout, _ = run_command(cmd.split())

    json_output = json.loads(stdout)

    try:
        validate(instance=json_output, schema=get_schema("timeline", test_path))
    except Exception as err:
        assert False, f"Unexpected {err=}, {type(err)=}"

    for stat in json_output["timeline"]:
        try:
            validate(instance=stat, schema=get_schema("stat", test_path))
        except Exception as err:
            assert False, f"Unexpected {err=}, {type(err)=}"
        assert True

@pytest.mark.parametrize("metric", [ ("ddr_bw") ])
def test_wperf_dmc_json_output(request, tmp_path, metric):
    """ Test for DMC / DDR part of the JSON schema.
    """
    test_path = os.path.dirname(request.path)

    if not wperf_metric_is_available(metric):
        pytest.skip(f"unsupported metric: {metric}")

    cmd = f"wperf stat -m {metric} --json --timeout 1"
    stdout, _ = run_command(cmd.split())

    json_output = json.loads(stdout)

    try:
        validate(instance=json_output, schema=get_schema("stat", test_path))
    except Exception as err:
        assert False, f"Unexpected {err=}, {type(err)=}"
