import lcapy

str_circuit = """
Vbase 0_n4 n1 3; up
Rbase n1 n4 1; up
Qctrl n2 n4 n5; up
Vsource 0_n3 n3 1; up
Rload n3 n2 4; up
W 0_n3 0_n4; right=0.8
W 0_n4 0; right=0.8
W 0 n5; up
"""
cct = lcapy.Circuit(str_circuit)

cct.draw('test-circuit.png')