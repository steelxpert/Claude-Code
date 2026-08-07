"""ccxio — CalculiX .inp mesh reader and .frd result writer.

Typical use: read a mesh from a CalculiX input deck, attach nodal fields
(e.g. a scaled buckling mode as a DISP field for PrePoMax's
"Update Nodal Coordinates From File"), and write a cgx/PrePoMax-compatible
.frd file.

    from ccxio import read_inp, write_frd, NodalResult

    model = read_inp("member.inp")
    disp = NodalResult("DISP", ("D1", "D2", "D3"),
                       {nid: (0.0, 0.0, 0.0) for nid in model.nodes})
    write_frd(model, "member.frd", results=[disp])
"""

from .model import Element, KeywordCard, Model
from .inp_reader import read_inp, InpSyntaxError, nnodes_for_type
from .frd_writer import (
    NodalResult,
    write_frd,
    FrdWriteError,
    frd_element_type,
)

__version__ = "0.1.0"

__all__ = [
    "Element",
    "KeywordCard",
    "Model",
    "read_inp",
    "InpSyntaxError",
    "nnodes_for_type",
    "NodalResult",
    "write_frd",
    "FrdWriteError",
    "frd_element_type",
    "__version__",
]
