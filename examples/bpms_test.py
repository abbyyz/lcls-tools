from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import (
    bmad_modeling_outputs as outfn,
)

# Instaintiate a tao object
OPTIONS = "-slice BEGINNING:END -noplot "
INIT = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}"
tao = Tao(INIT)
tao.cmd("set ele BEGINNING:ENDCOL0 field_master=True")


# Short cut command for user readable output
def tc(cmd):
    [print(line) for line in tao.cmd(cmd)]
