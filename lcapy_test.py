import lcapy

# from lcapy import R, C, L
# ((R(1) + L(2)) | C(3)).s_model().draw('schematic.pdf')

netlist = '''
Q1 3 0 2 pnp; up
R1 1 2;right
R2 4 0_4;down
P1 1 0_1;down
W 0_1 0;right
W 0 0_4;right
W 3 4;right

V 1 0_1 1V; right
'''

cct = lcapy.Circuit(netlist)
cct.draw('voltage-divider.pdf')

from PySpice.Spice.Netlist import Circuit
circuit = Circuit(netlist)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.dc(Vbase=slice(0, 3, .01))