"""Shim (QA only): pycufsm's compiled solver breaks under numpy 2 (int() of a 1-element array).
Load its pure-Python solver with that one line patched and route fsm.strip to it."""
import importlib.util, os, types
import pycufsm.solve.analysis_p as _p
import pycufsm.solve.analysis as _pa
import pycufsm.fsm as _fsm

_src = open(_p.__file__, encoding="utf-8").read().replace(
    "int((np.argwhere(props[:, 0] == mat_num)).reshape(1))",
    "int(np.argwhere(props[:, 0] == mat_num).ravel()[0])")
_mod = types.ModuleType("_cufsm_analysis_fixed")
exec(compile(_src, _p.__file__, "exec"), _mod.__dict__)
_pa.analysis = _mod
_fsm.analysis = _mod
