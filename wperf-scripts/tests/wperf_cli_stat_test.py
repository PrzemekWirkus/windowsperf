#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Arm Limited
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

"""
This script runs simple wperf CLI tests.

Requires:
    pytest -    install with `pip install -U pytest`

Usage:
    >py.test wperf_cli_test.py

"""

import os
import re
from common import run_command, is_json, check_if_file_exists

import pytest

N_CORES = os.cpu_count()

### Test cases

@pytest.mark.parametrize("events,cores,metric,sleep",
[
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),

    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),
]
)
def test_wperf_stat_json(events,cores,metric,sleep):
    """ Test `wperf stat -json` command line output.

        Use pytest.mark.parametrize to set up below command line switches:

            ( -e <events>, -c <cores>, -m <metric>, sleep <value> )
    """
    cmd = 'wperf stat'.split()
    if events:
        cmd += ['-e', events]
    if cores:
        cmd += ['-c', cores]
    if metric:
        cmd += ['-m', metric]
    if sleep:
        cmd += ['sleep', str(sleep)]

    cmd += ['-json']

    stdout, _ = run_command(cmd)
    assert is_json(stdout)

def test_wperf_stat_no_events():
    """ Test for required -e for `wperf stat` """
    cmd = "wperf stat -c 0 sleep 1"
    _, stderr = run_command(cmd)
    assert b'no event specified' in stderr

@pytest.mark.parametrize("events,cores,metric,sleep",
[
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//2)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//6)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//8)), "", 1),

    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//2)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//6)), "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES,N_CORES//8)), "", 1),
]
)
def test_wperf_stat(events,cores,metric,sleep):
    """ Test `wperf stat` command line output.

        Use pytest.mark.parametrize to set up below command line switches:

            ( -e <events>, -c <cores>, -m <metric>, sleep <value> )
    """
    cmd = 'wperf stat'.split()
    if events:
        cmd += ['-e', events]
    if cores:
        cmd += ['-c', cores]
    if metric:
        cmd += ['-m', metric]
    if sleep:
        cmd += ['sleep', str(sleep)]

    stdout, _ = run_command(cmd)

    # Common CLI outputs
    assert b'seconds time elapsed' in stdout

    # Core number message
    if cores:
        for core in cores.split(','):
            assert b'Performance counter stats for core %d' % int(core) in stdout

    # Pretty table basic columns (no multiplexing)
    for col in [b'counter value' , b'event name', b'event idx', b'event note']:
        assert re.search(b'[\\s]+%s[\\s]+' % col, stdout)

    # Pretty table basic columns (multiplexing)
    if b', multiplexed' in stdout:
        for col in [b'multiplexed' , b'scaled value']:
            assert re.search(b'[\\s]+%s[\\s]+' % col, stdout)

    # Event names in pretty table
    if events:
        for event in events.split(b','):
            assert re.search(b'[\\d]+[\\s]+%s[\\s]+0x[0-9a-f]+' % event, stdout)
        assert re.search(b'[\\s]+cycle[\\s]+fixed', stdout)

    # Overall summary header when more than one CPU count
    # Note: if -c is not speciffied we count on all cores
    if not cores or len(cores.split(',')) > 1:
        assert b'System-wide Overall:' in stdout
    elif len(cores.split(',')) == 1:
        assert b'System-wide Overall:' not in stdout

@pytest.mark.parametrize("events,cores,metric,sleep",
[
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),

    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),
]
)
def test_wperf_stat_json_file_output_exists(events, cores, metric, sleep, tmp_path):
    """ Test `wperf stat` JSON output to file """
    file_path = tmp_path / 'test.json'
    cmd = 'wperf stat'.split()
    if events:
        cmd += ['-e', events]
    if cores:
        cmd += ['-c', cores]
    if metric:
        cmd += ['-m', metric]
    if sleep:
        cmd += ['sleep', str(sleep)]

    cmd += ['--output', str(file_path)]

    print(' '.join(str(c) for c in cmd))
    stdout, _ = run_command(cmd)
    print(stdout)
    assert check_if_file_exists(str(file_path))

@pytest.mark.parametrize("events,cores,metric,sleep",
[
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),

    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", "0,1", "", 1),
    (b"inst_spec,vfp_spec,ase_spec,dp_spec,ld_spec,st_spec,br_immed_spec,crypto_spec", ','.join(str(cores) for cores in range(0, N_CORES)), "", 1),
]
)
def test_wperf_stat_json_file_output_valid(events, cores, metric, sleep, tmp_path):
    """ Test `wperf stat` JSON output to file validity """
    file_path = tmp_path / 'test.json'
    cmd = 'wperf stat'.split()

    if events:
        cmd += ['-e', events]
    if cores:
        cmd += ['-c', cores]
    if metric:
        cmd += ['-m', metric]
    if sleep:
        cmd += ['sleep', str(sleep)]

    cmd += ['--output', str(file_path)]
    stdout, _ = run_command(cmd)
    try:
        f = open(file_path)
        json = f.read()
        f.close()
        assert is_json(json)
    except:
        assert 0