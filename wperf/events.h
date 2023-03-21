#pragma once
// BSD 3-Clause License
//
// Copyright (c) 2022, Arm Limited
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this
//    list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its
//    contributors may be used to endorse or promote products derived from
//    this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include "wperf-common\iorequest.h"


enum evt_type
{
    EVT_NORMAL,
    EVT_GROUPED,
    EVT_METRIC_NORMAL,
    EVT_METRIC_GROUPED,
    EVT_PADDING,
    EVT_HDR,                //!< Used to make beginning of a new group. Not real event
};

enum
{
#define WPERF_ARMV8_ARCH_EVENTS(a,b,c) PMU_EVENT_##a = b,
#include "wperf-common\armv8-arch-events.def"
#undef WPERF_ARMV8_ARCH_EVENTS
};

enum
{
#define WPERF_DMC_CLKDIV2_EVENTS(a,b,c) DMC_EVENT_##a = b,
#include "wperf-common\dmc-clkdiv2-events.def"
#undef WPERF_DMC_CLKDIV2_EVENTS
};


extern wchar_t* evt_class_name[EVT_CLASS_NUM];
extern const wchar_t* evt_name_prefix[EVT_CLASS_NUM];

wchar_t* get_dmc_clk_event_name(uint16_t index);
const wchar_t* get_dmc_clkdiv2_event_name(uint16_t index);
const wchar_t* get_core_event_name(uint16_t index);
const wchar_t* get_event_name(uint16_t index, enum evt_class e_class = EVT_CORE);
int get_core_event_index(std::wstring name);
int get_dmc_clk_event_index(std::wstring name);
int get_dmc_clkdiv2_event_index(std::wstring name);
int get_event_index(std::wstring name, enum evt_class e_class = EVT_CORE);