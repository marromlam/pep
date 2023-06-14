#!/usr/bin/python
# (C) CERN 2007-2014
# (C) Andrzej Nowak 2014-2020
# Additional credit: Mirela-Madalina Botezatu
# needs libpfm >= 4.5
# Updated events for Haswell, Ivy Bridge Stalls

import sys, os, re, locale, traceback, getopt, subprocess

locale.setlocale(locale.LC_ALL, 'en_US')

#re_result = re.compile("[CPU0]*\s*(\d+)(\,)([\w:]+)")
re_result = re.compile("(\d+)(\,)([\w:]+)")
#perf = "/usr/bin/perf stat"
perf = "/var/opt/PEP/perf stat"
args = ""
timeout = 10
andreas_mode = False
    
def fprint(arg1, arg2):
    print "%31s: %s" % (arg1, arg2)

cpuinfo = {}
def read_cpuinfo():
    global cpuinfo
    f = open("/proc/cpuinfo")
    lines = f.readlines()
    f.close()
    
    for line in lines:
        tempstr = line.split(":")
        if cpuinfo.has_key(tempstr[0]):
            break
        if len(tempstr) < 2:
            continue
        key = tempstr[0].replace(" ", "_").lower().strip("\n\t")
        val = tempstr[1].strip("\n\t")
        try:
            cpuinfo[key] = int(val)
        except:
            cpuinfo[key] = val
        

       
class Results(dict):
	def __init__(self):
		dict.__init__(self)
        
	def get(self, arg):
		return float(self[arg])

results = Results()

def analysis_standard_snb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("load instructions %", "%.3f%%" % (results.get("MEM_UOPS_RETIRED:ALL_LOADS") / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("store instructions %", "%.3f%%" % (results.get("MEM_UOPS_RETIRED:ALL_STORES") / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("load and store instructions %", "%.3f%%" % ((results.get("MEM_UOPS_RETIRED:ALL_LOADS") + results.get("MEM_UOPS_RETIRED:ALL_STORES")) / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("resource stalls % (of cycles)", "%.3f%%" % (results.get("RESOURCE_STALLS:ANY") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("branch instructions % (approx)", "%.3f%%" % (results.get("BR_INST_EXEC:ALL_BRANCHES") / results.get("INSTRUCTIONS_RETIRED") * 100))
    fprint("% of branch instr. mispredicted", "%.3f%%" % (float(results["BR_MISP_EXEC:ALL_BRANCHES"])*100 / float(results["BR_INST_EXEC:ALL_BRANCHES"])))
    fprint("% of L3 loads missed", "%.3f%%" % (results.get("LAST_LEVEL_CACHE_MISSES") / results.get("LAST_LEVEL_CACHE_REFERENCES") * 100))
    fprint("computational x87 instr. %", "%.3f%%" % (results.get("FP_COMP_OPS_EXE:X87") / results.get("INSTRUCTIONS_RETIRED") * 100))

def analysis_standard_hsw(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("load instructions %", "%.3f%%" % (results.get("MEM_UOPS_RETIRED:ALL_LOADS") / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("store instructions %", "%.3f%%" % (results.get("MEM_UOPS_RETIRED:ALL_STORES") / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("load and store instructions %", "%.3f%%" % ((results.get("MEM_UOPS_RETIRED:ALL_LOADS") + results.get("MEM_UOPS_RETIRED:ALL_STORES")) / results.get("UOPS_RETIRED:ANY") * 100))
    fprint("resource stalls % (of cycles)", "%.3f%%" % (results.get("RESOURCE_STALLS:ANY") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("branch instructions % (approx)", "%.3f%%" % (results.get("BR_INST_EXEC:ALL_BRANCHES") / results.get("INSTRUCTIONS_RETIRED") * 100))
    fprint("% of branch instr. mispredicted", "%.3f%%" % (float(results["BR_MISP_EXEC:ALL_BRANCHES"])*100 / float(results["BR_INST_EXEC:ALL_BRANCHES"])))
    fprint("% of L3 loads missed", "%.3f%%" % (results.get("LONGEST_LAT_CACHE:MISS") / results.get("LONGEST_LAT_CACHE:REFERENCE") * 100))
#    fprint("computational x87 instr. %", "%.3f%%" % (results.get("FP_COMP_OPS_EXE:X87") / results.get("INSTRUCTIONS_RETIRED") * 100))

def analysis_simd1_snb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    all_simd_comp = results.get("FP_COMP_OPS_EXE:SSE_FP_PACKED_DOUBLE") + \
	    results.get("FP_COMP_OPS_EXE:SSE_PACKED_SINGLE") + \
	    results.get("FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE") + \
	    results.get("FP_COMP_OPS_EXE:SSE_FP_SCALAR_SINGLE") + \
	    results.get("SIMD_FP_256:PACKED_SINGLE") + \
	    results.get("SIMD_FP_256:PACKED_DOUBLE") 

    all_comp = all_simd_comp + \
            results.get("FP_COMP_OPS_EXE:X87")

    fprint("all computational SIMD uops.", "%s" % locale.format("%d", all_simd_comp, 1))
    fprint("all computational uops.", "%s" % locale.format("%d", all_comp, 1))
    fprint("% of SIMD in comp. uops.", "%s" % locale.format("%.3f%%", all_simd_comp / all_comp * 100.0, 1))
    if all_simd_comp > 0:
        fprint("", "")
        fprint("breakdown", "% of comp. SIMD")
        fprint("DOUBLE_PRECISION", "%.3f%%" % ((results.get("FP_COMP_OPS_EXE:SSE_FP_PACKED_DOUBLE") + results.get("FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE")+results.get("SIMD_FP_256:PACKED_DOUBLE"))/ all_simd_comp * 100))
        fprint("SINGLE_PRECISION", "%.3f%%" % ((results.get("FP_COMP_OPS_EXE:SSE_PACKED_SINGLE") + results.get("FP_COMP_OPS_EXE:SSE_FP_SCALAR_SINGLE")+results.get("SIMD_FP_256:PACKED_SINGLE"))/ all_simd_comp * 100))
        fprint("PACKED", "%.3f%%" % ((results.get("FP_COMP_OPS_EXE:SSE_FP_PACKED_DOUBLE") + results.get("FP_COMP_OPS_EXE:SSE_PACKED_SINGLE") +results.get("SIMD_FP_256:PACKED_SINGLE")+results.get("SIMD_FP_256:PACKED_DOUBLE"))/ all_simd_comp * 100))
        fprint("SCALAR", "%.3f%%" % ((results.get("FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE")+results.get("FP_COMP_OPS_EXE:SSE_FP_SCALAR_SINGLE")) / all_simd_comp * 100))


def analysis_stalls_snb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("breakdown", "% of cycles    % of stalls")
    fprint("res. stalls", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ANY") / results.get("UNHALTED_CORE_CYCLES") * 100, 100.))
    fprint("load buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:LB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:LB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("store buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:SB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:SB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("RS full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:RS") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("ROB full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ROB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:ROB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("FPU ctrl word", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:FCSW") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:FCSW") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("MXCSR register rename", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MXCSR") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MXCSR") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("LB SB RS all in use", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MEM_RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MEM_RS") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("free list empty", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("ctrl struct full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("branch order buffer", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("out of order resources full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("RESOURCE_STALLS:ANY") * 100))

def analysis_stalls_ivb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("breakdown", "% of cycles    % of stalls")
    fprint("res. stalls", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ANY") / results.get("UNHALTED_CORE_CYCLES") * 100, 100.))
#    fprint("load buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:LB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:LB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("store buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:SB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:SB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("RS full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:RS") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("ROB full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ROB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:ROB") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("FPU ctrl word", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:FCSW") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:FCSW") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("MXCSR register rename", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MXCSR") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MXCSR") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("LB SB RS all in use", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MEM_RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MEM_RS") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("free list empty", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("ctrl struct full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("branch order buffer", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("out of order resources full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("RESOURCE_STALLS:ANY") * 100))

def analysis_stalls_hsw(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("breakdown", "% of cycles    % of stalls")
    fprint("res. stalls", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ANY") / results.get("UNHALTED_CORE_CYCLES") * 100, 100.))
#    fprint("load buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:LB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:LB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("store buf", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:SB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:SB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("RS full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:RS") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("RS empty (!)", "%.3f%%           %.3f%%" % (results.get("RS_EVENTS:EMPTY_CYCLES") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RS_EVENTS:EMPTY_CYCLES") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("ROB full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:ROB") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:ROB") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("ILD LCP stalls", "%.3f%%           %.3f%%" % (results.get("ILD_STALL:LCP") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("ILD_STALL:LCP") / results.get("RESOURCE_STALLS:ANY") * 100))
    fprint("Inst Q full", "%.3f%%           %.3f%%" % (results.get("ILD_STALL:IQ_FULL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("ILD_STALL:IQ_FULL") / results.get("RESOURCE_STALLS:ANY") * 100))
    
#    fprint("FPU ctrl word", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:FCSW") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:FCSW") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("MXCSR register rename", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MXCSR") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MXCSR") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("LB SB RS all in use", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS:MEM_RS") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS:MEM_RS") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("free list empty", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_FL_EMPTY") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("ctrl struct full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:ALL_PRF_CONTROL") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("branch order buffer", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:BOB_FULL") / results.get("RESOURCE_STALLS:ANY") * 100))
#    fprint("out of order resources full", "%.3f%%           %.3f%%" % (results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("UNHALTED_CORE_CYCLES") * 100, results.get("RESOURCE_STALLS2:OOO_RSRC") / results.get("RESOURCE_STALLS:ANY") * 100))

def analysis_cycle_snb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("UOPS RETIRED ", " %.3f " % (results.get("UOPS_RETIRED:ANY") ))
    fprint("No exec uop ret. % (of cycles) ", " %.3f%% " % (results.get("UOPS_RETIRED:STALL_CYCLES") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("No uops issued % (of cycles) ", " %.3f%% " % (results.get("UOPS_ISSUED:STALL_CYCLES") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("Nr of retirement slots used ", " %.3f " % (results.get("UOPS_RETIRED:RETIRE_SLOTS") ))
    fprint("Nr of uops issued by the RAT ", " %.3f " % (results.get("UOPS_ISSUED:ANY") ))

def analysis_cycle_hsw(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("UOPS RETIRED ", " %.0f " % (results.get("UOPS_RETIRED:ANY") ))
    fprint("No exec uop ret. % (of cycles) ", " %.3f%% " % (results.get("UOPS_RETIRED:STALL_CYCLES") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("No uops issued % (of cycles) ", " %.3f%% " % (results.get("UOPS_ISSUED:STALL_CYCLES") / results.get("UNHALTED_CORE_CYCLES") * 100))
    fprint("Nr of retirement slots used ", " %.0f " % (results.get("UOPS_RETIRED:RETIRE_SLOTS") ))
    fprint("Nr of uops issued by the RAT ", " %.0f " % (results.get("UOPS_ISSUED:ANY") ))

def analysis_branch_snb(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("instructions per jump", "%.1f" % (results.get("INSTRUCTIONS_RETIRED") / results.get("BR_INST_RETIRED:ALL_BRANCHES")))
    fprint("instructions per call", "%.1f" % (results.get("INSTRUCTIONS_RETIRED") / results.get("BR_INST_RETIRED:NEAR_RETURN")))
    fprint("", "")
    fprint("breakdown", "% of branches")
    fprint("mispredicted", "%.3f%%" % (results.get("MISPREDICTED_BRANCH_RETIRED") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
#    fprint("conditional jumps", "%.3f%%" % (results.get("BR_INST_RETIRED:COND") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
    fprint("conditional jumps", "%.3f%%" % (results.get("BR_INST_RETIRED:CONDITIONAL") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
    fprint("calls", "%.3f%%" % (results.get("BR_INST_RETIRED:NEAR_RETURN") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))

def analysis_branch_hsw(results):
    print("")
    fprint("CPI", "%.4f" % (results.get("UNHALTED_CORE_CYCLES") / results.get("INSTRUCTIONS_RETIRED")))
    fprint("", "")
    fprint("instructions per jump", "%.1f" % (results.get("INSTRUCTIONS_RETIRED") / results.get("BR_INST_RETIRED:ALL_BRANCHES")))
    fprint("instructions per call", "%.1f" % (results.get("INSTRUCTIONS_RETIRED") / results.get("BR_INST_RETIRED:NEAR_RETURN")))
    fprint("", "")
    fprint("breakdown", "% of branches")
    fprint("mispredicted", "%.3f%%" % (results.get("MISPREDICTED_BRANCH_RETIRED") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
#    fprint("conditional jumps", "%.3f%%" % (results.get("BR_INST_RETIRED:COND") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
    fprint("conditional jumps", "%.3f%%" % (results.get("BR_INST_RETIRED:CONDITIONAL") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))
    fprint("calls", "%.3f%%" % (results.get("BR_INST_RETIRED:NEAR_RETURN") / results.get("BR_INST_RETIRED:ALL_BRANCHES") * 100))

setup_tbl_snb = {
    "standard": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,MEM_UOPS_RETIRED:ALL_STORES,MEM_UOPS_RETIRED:ALL_LOADS,UOPS_RETIRED:ANY,RESOURCE_STALLS:ANY,BR_INST_EXEC:ALL_BRANCHES,BR_MISP_EXEC:ALL_BRANCHES,LAST_LEVEL_CACHE_REFERENCES,LAST_LEVEL_CACHE_MISSES,FP_COMP_OPS_EXE:X87,UOPS_RETIRED:ANY",

    "simd1": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,FP_COMP_OPS_EXE:SSE_FP_PACKED_DOUBLE,FP_COMP_OPS_EXE:SSE_PACKED_SINGLE,FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE,FP_COMP_OPS_EXE:SSE_FP_SCALAR_SINGLE,FP_COMP_OPS_EXE:X87,SIMD_FP_256:PACKED_DOUBLE,SIMD_FP_256:PACKED_SINGLE,UOPS_RETIRED:ANY",

    "stalls": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,RESOURCE_STALLS:ANY,RESOURCE_STALLS:LB,RESOURCE_STALLS:SB,RESOURCE_STALLS:RS,RESOURCE_STALLS:ROB,RESOURCE_STALLS:FCSW,RESOURCE_STALLS:MXCSR,RESOURCE_STALLS:MEM_RS,RESOURCE_STALLS2:ALL_FL_EMPTY,RESOURCE_STALLS2:ALL_PRF_CONTROL,RESOURCE_STALLS2:BOB_FULL,RESOURCE_STALLS2:OOO_RSRC",
    
    "cycle": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,UOPS_RETIRED:ANY,UOPS_ISSUED:ANY,UOPS_RETIRED:STALL_CYCLES,UOPS_RETIRED:RETIRE_SLOTS,UOPS_ISSUED:STALL_CYCLES",

#    "branch": " -x, --pfm-events=UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,BR_INST_RETIRED:ALL_BRANCHES,BR_INST_RETIRED:COND,BR_INST_RETIRED:NEAR_RETURN,MISPREDICTED_BRANCH_RETIRED"
    
    "branch": " -x, --pfm-events=UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,BR_INST_RETIRED:ALL_BRANCHES,BR_INST_RETIRED:CONDITIONAL,BR_INST_RETIRED:NEAR_CALL,BR_INST_RETIRED:NEAR_RETURN,MISPREDICTED_BRANCH_RETIRED"
    
}

analysis_tbl_snb = {
    "standard": analysis_standard_snb,
    "simd1": analysis_simd1_snb,
    "stalls": analysis_stalls_snb,
    "cycle": analysis_cycle_snb,
    "branch": analysis_branch_snb
}

setup_tbl_ivb = {
    "standard": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,MEM_UOPS_RETIRED:ALL_STORES,MEM_UOPS_RETIRED:ALL_LOADS,UOPS_RETIRED:ANY,RESOURCE_STALLS:ANY,BR_INST_EXEC:ALL_BRANCHES,BR_MISP_EXEC:ALL_BRANCHES,LAST_LEVEL_CACHE_REFERENCES,LAST_LEVEL_CACHE_MISSES,FP_COMP_OPS_EXE:X87,UOPS_RETIRED:ANY",

    "simd1": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,FP_COMP_OPS_EXE:SSE_FP_PACKED_DOUBLE,FP_COMP_OPS_EXE:SSE_PACKED_SINGLE,FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE,FP_COMP_OPS_EXE:SSE_FP_SCALAR_SINGLE,FP_COMP_OPS_EXE:X87,SIMD_FP_256:PACKED_DOUBLE,SIMD_FP_256:PACKED_SINGLE,UOPS_RETIRED:ANY",

    "stalls": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,RESOURCE_STALLS:ANY,RESOURCE_STALLS:SB,RESOURCE_STALLS:RS,RESOURCE_STALLS:ROB",
#    RESOURCE_STALLS:MEM_RS,RESOURCE_STALLS2:ALL_FL_EMPTY,RESOURCE_STALLS2:ALL_PRF_CONTROL,RESOURCE_STALLS2:BOB_FULL,RESOURCE_STALLS2:OOO_RSRC",
    
    "cycle": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,UOPS_RETIRED:ANY,UOPS_ISSUED:ANY,UOPS_RETIRED:STALL_CYCLES,UOPS_RETIRED:RETIRE_SLOTS,UOPS_ISSUED:STALL_CYCLES",

#    "branch": " -x, --pfm-events=UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,BR_INST_RETIRED:ALL_BRANCHES,BR_INST_RETIRED:COND,BR_INST_RETIRED:NEAR_RETURN,MISPREDICTED_BRANCH_RETIRED"
    
    "branch": " -x, --pfm-events=UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,BR_INST_RETIRED:ALL_BRANCHES,BR_INST_RETIRED:CONDITIONAL,BR_INST_RETIRED:NEAR_CALL,BR_INST_RETIRED:NEAR_RETURN,MISPREDICTED_BRANCH_RETIRED"
    
}

analysis_tbl_ivb = {
    "standard": analysis_standard_snb,
    "simd1": analysis_simd1_snb,
    "stalls": analysis_stalls_ivb,
    "cycle": analysis_cycle_snb,
    "branch": analysis_branch_snb
}

setup_tbl_hsw = {
    "standard": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,MEM_UOPS_RETIRED:ALL_STORES,MEM_UOPS_RETIRED:ALL_LOADS,UOPS_RETIRED:ANY,RESOURCE_STALLS:ANY,BR_INST_EXEC:ALL_BRANCHES,BR_MISP_EXEC:ALL_BRANCHES,LONGEST_LAT_CACHE:REFERENCE,LONGEST_LAT_CACHE:MISS,UOPS_RETIRED:ANY",
    "stalls": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,RESOURCE_STALLS:ANY,RESOURCE_STALLS:SB,RESOURCE_STALLS:RS,RS_EVENTS:EMPTY_CYCLES,RESOURCE_STALLS:ROB,ILD_STALL:LCP,ILD_STALL:IQ_FULL",
    "cycle": " -x, --pfm-event UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,UOPS_RETIRED:ANY,UOPS_ISSUED:ANY,UOPS_RETIRED:STALL_CYCLES,UOPS_RETIRED:RETIRE_SLOTS,UOPS_ISSUED:STALL_CYCLES",
    "branch": " -x, --pfm-events=UNHALTED_CORE_CYCLES,INSTRUCTIONS_RETIRED,BR_INST_RETIRED:ALL_BRANCHES,BR_INST_RETIRED:CONDITIONAL,BR_INST_RETIRED:NEAR_CALL,BR_INST_RETIRED:NEAR_RETURN,MISPREDICTED_BRANCH_RETIRED"
}

analysis_tbl_hsw = {
    "standard": analysis_standard_hsw,
    "stalls": analysis_stalls_hsw,
    "cycle": analysis_cycle_hsw,
    "branch": analysis_branch_hsw
}

print ""
print "Perf deluxe v.2 (Haswell ready)"
print "A simple script wrapping perf in pink paper. Comments to Andrzej Nowak"
print ""

read_cpuinfo()

# startup - determine if we're in stdin mode
stdin_mode = 0
if sys.argv[0].count("stdin") == 0:
    stdin_mode = 0
else:
    stdin_mode = 1

# get options
focus = "standard"
extra = ""

del sys.argv[0]
optlist, arglist = getopt.getopt(sys.argv[0:], "af:t:e:h", ["andreas-mode", "focus=", "timeout=", "extra=", "help"])

for o, a in optlist:
    if o in ("-f", "--focus"):
        print "Focus: %s" % a
        focus = a

    elif o in ("-t", "--timeout"):
        print "Setting timeout to %d ms" % int(a)
        timeout = int(a)

    elif o in ("-h", "--help"):
        print "what do you mean, 'help'?"
        print "Usage: ./perf_del.py [-a] [-f focus (standard/simd1/stalls/cycle)]  -e \"additional perf options and binary\""
        print "  -f: focus on a certain group of events"
        print "  -t: multiplexing switch timeout in ms"
        sys.exit(0)

    elif o in ("-e", "--extra"):
        extra = a

    elif o in ("-a", "--andreas"):
        andreas_mode = True

for a in arglist:
    extra += " " + a

if cpuinfo['model'] == 63:
    print "Setting up for Haswell"
    setup_tbl = setup_tbl_hsw
    analysis_tbl = analysis_tbl_hsw
    try:
        setup = setup_tbl[focus]
    except:
        print "Unknown focus or other error. Exiting"
        sys.exit(0)


if cpuinfo['model'] == 62:
    print "Setting up for Ivy Bridge (with SNB events)"
    setup_tbl = setup_tbl_ivb
    analysis_tbl = analysis_tbl_ivb
    try:
        setup = setup_tbl[focus]
    except:
        print "Unknown focus or other error. Exiting"
        sys.exit(0)

if cpuinfo['model'] == 45:
    print "Setting up for Sandy Bridge"
    setup_tbl = setup_tbl_snb
    analysis_tbl = analysis_tbl_snb
    try:
        setup = setup_tbl[focus]
    except:
        print "Unknown focus or other error. Exiting"
        sys.exit(0)

if stdin_mode == 0:
    print "Running %s with arguments: %s" % (perf, extra)
    cmd = perf + " " + setup + " " + extra
    print "Command line: %s" % cmd
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (no_thing___, p) = (p.stdin, p.stdout)
else:
    p = sys.stdin


resultlines = []
duplicate_counter = 1
stri=""
for line in p.readlines():
	line = line.strip("\n")
	result = re_result.match(line)
	if result:
		if not results.has_key(result.group(3)):
			results[result.group(3)] = result.group(1)
		else:
			results[result.group(3) + "--%d" % duplicate_counter] = result.group(1)
			duplicate_counter += 1
                resultlines.append(line)
                print locale.format("%d", int(result.group(1)), True).rjust(20), result.group(3)
	else:
        	print line

#print results

print "-----------------------------------------------------------------------"
print "Ratios:"

try:
    analysis_tbl[focus](results)
except:
    print "\nStop right there, sailor! Bogus results. Results processing interrupted due to an exception."
    print sys.exc_info()[0:2]
    traceback.print_exc()
print ""
