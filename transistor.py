import numpy as np
import matplotlib.pyplot as plt


import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


spice_library = SpiceLibrary("libraries")


figure = plt.figure(1, (20, 10))

circuit = Circuit('Transistor')

Vbase = circuit.V('base', '1', circuit.gnd, 1@u_V)
circuit.R('base', 1, 'base', 1@u_kΩ)
Vcollector = circuit.V('collector', '2', circuit.gnd, 0@u_V)
circuit.R('collector', 2, 'collector', 1@u_kΩ)
# circuit.BJT(1, 'collector', 'base', circuit.gnd, model='generic')
# circuit.model('generic', 'npn')
circuit.include(spice_library['2n2222a'])
circuit.BJT(1, 'collector', 'base', circuit.gnd, model='2n2222a')


simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.dc(Vbase=slice(0, 3, .01))

axe1 = plt.subplot(221)
axe1.plot(analysis.base, u_mA(-analysis.Vbase)) # Fixme: I_Vbase
axe1.axvline(x=.65, color='red')
axe1.legend(('Base-Emitter Diode curve',), loc=(.1,.8))
axe1.grid()
axe1.set_xlabel('Vbe [V]')
axe1.set_ylabel('Ib [mA]')



circuit = Circuit('Transistor')
Ibase = circuit.I('base', circuit.gnd, 'base', 10@u_uA) # take care to the orientation
Vcollector = circuit.V('collector', 'collector', circuit.gnd, 5)
# circuit.BJT(1, 'collector', 'base', circuit.gnd, model='generic')
# circuit.model('generic', 'npn')
circuit.include(spice_library['2n2222a'])
circuit.BJT(1, 'collector', 'base', circuit.gnd, model='2n2222a')

# Fixme: ngspice doesn't support multi-sweep ???
#   it works in interactive mode


axe2 = plt.subplot(222)
axe2.grid()
# axe2.legend(('Ic(Vce, Ib)',), loc=(.5,.5))
axe2.set_xlabel('Vce [V]')
axe2.set_ylabel('Ic [mA]')
axe2.axvline(x=.2, color='red')

axe3 = plt.subplot(223)
axe3.grid()
# axe3.legend(('beta(Vce)',), loc=(.5,.5))
axe3.set_xlabel('Vce [V]')
axe3.set_ylabel('beta')
axe3.axvline(x=.2, color='red')

for base_current in np.arange(0, 100, 10):
    base_current = base_current@u_uA
    Ibase.dc_value = base_current
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.dc(Vcollector=slice(0, 5, .01))
    # add ib as text, linear and saturate region
    # Plot Ic = f(Vce)
    axe2.plot(analysis.collector, u_mA(-analysis.Vcollector))
    # Plot β = Ic / Ib = f(Vce)
    axe3.plot(analysis.collector, -analysis.Vcollector/float(base_current))
    # trans-resistance U = RI   R = U / I = Vce / Ie
    # axe3.plot(analysis.collector, analysis.sweep/(float(base_current)-analysis.Vcollector))
    # Fixme: sweep is not so explicit


axe4 = plt.subplot(224)
axe4.grid()
axe4.set_xlabel('Ib [uA]')
axe4.set_ylabel('Ic [mA]')

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.dc(Ibase=slice(0, 100e-6, 10e-6))
# Fixme: sweep
axe4.plot(analysis.sweep*1e6, u_mA(-analysis.Vcollector), 'o-')
axe4.legend(('Ic(Ib)',), loc=(.1,.8))


plt.tight_layout()
plt.show()
plt.savefig('iop.png')