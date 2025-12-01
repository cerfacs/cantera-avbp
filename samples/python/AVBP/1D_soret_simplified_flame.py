import cantera as ct
import numpy as np


gas = ct.Solution('./inputs/SanDiego_hydrogen.yaml')
gas.TP = 300, ct.one_atm
phi = 0.6
gas.set_equivalence_ratio(phi, 'H2', 'O2:1, N2:3.76')

f = ct.FreeFlame(gas, width=0.02)
f.transport_model = 'mixture-averaged'
f.soret_enabled = True
f.flame.alphaH2 = 0.664
f.flame.alphaH = 0.580


f.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.05)

f.solve(loglevel=1, refine_grid="refine")


f.save("./RESULTS/flame_SD_soret_on_phi06.yaml",overwrite=True)



