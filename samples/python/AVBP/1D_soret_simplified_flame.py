import cantera as ct
import numpy as np


"""
Simplified Soret effect for H2 and H for mixture-averaged transport. [1]
User must use mixture-averaged transport :
f.transport_model = "mixture-averaged"
User must also activate soret effect
f.soret_enabled = True
User must change alpha (correction factor) for H2 and H.
For hydrogen chemistry, recommended values are :

f.flame.alphaH2 = 0.664
f.flame.alphaH = 0.580
[1] T. L. Howarth, M. S. Day, H. Pitsch, and A. J. Aspden, “Thermal diffusion , exhaust gas recirculation and blending effects on lean premixed hydrogen flames,” Proc. Combust. Inst., vol. 40, no. 1–4, p. 105429, 2024, doi: 10.1016/j.proci.2024.105429.
"""

gas = ct.Solution('./inputs/SanDiego_H2.yaml')
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

flame_velocity_with_soret = f.velocity[0]
f.save("./RESULTS/flame_SD_soret_on_phi06.yaml",overwrite=True)


gas = ct.Solution('./inputs/SanDiego_H2.yaml')
gas.TP = 300, ct.one_atm
phi = 0.6
gas.set_equivalence_ratio(phi, 'H2', 'O2:1, N2:3.76')

f = ct.FreeFlame(gas, width=0.02)
f.transport_model = 'mixture-averaged'
f.soret_enabled = False


f.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.05)

f.solve(loglevel=1, refine_grid="refine")

flame_velocity_without_soret = f.velocity[0]
f.save("./RESULTS/flame_SD_soret_off_phi06.yaml",overwrite=True)


print("Flame velocity with and without soret effect: ",flame_velocity_with_soret," ",flame_velocity_without_soret)



