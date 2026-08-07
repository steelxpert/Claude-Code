"""ccxio — CalculiX .inp and .frd I/O plus imperfection seeding.

The full imperfection loop, scriptable end to end:

    from ccxio import read_inp, read_frd, seed_imperfection, write_inp

    model = read_inp("member.inp")                 # perfect mesh
    modes = read_frd("member_buckle.frd")          # *BUCKLE result
    mode1 = modes.result("DISP", 0)                # first eigenmode
    seeded = seed_imperfection(model, mode1, amplitude=0.64)
    write_inp(seeded, "member_imperfect.inp")
"""

from .model import Element, KeywordCard, Model
from .inp_reader import read_inp, InpSyntaxError, nnodes_for_type
from .inp_writer import write_inp
from .frd_writer import (
    NodalResult,
    write_frd,
    FrdWriteError,
    frd_element_type,
)
from .frd_reader import read_frd, FrdFile, FrdSyntaxError
from .imperfection import seed_imperfection, ImperfectionError

__version__ = "0.2.0"

__all__ = [
    "Element",
    "KeywordCard",
    "Model",
    "read_inp",
    "write_inp",
    "InpSyntaxError",
    "nnodes_for_type",
    "NodalResult",
    "write_frd",
    "FrdWriteError",
    "frd_element_type",
    "read_frd",
    "FrdFile",
    "FrdSyntaxError",
    "seed_imperfection",
    "ImperfectionError",
    "__version__",
]
