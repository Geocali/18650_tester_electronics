import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Spice.NgSpice.Shared import NgSpiceShared


ngspice = NgSpiceShared.new_instance()

# print(ngspice.exec_command('version -f'))
# print(ngspice.exec_command('print all'))
# print(ngspice.exec_command('devhelp'))
# print(ngspice.exec_command('devhelp resistor'))

circuit = '''
.title Voltage Multiplier

.SUBCKT 1N4148 1 2
*
R1 1 2 5.827E+9
D1 1 2 1N4148
*
.MODEL 1N4148 D
+ IS = 4.352E-9
+ N = 1.906
+ BV = 110
+ IBV = 0.0001
+ RS = 0.6458
+ CJO = 7.048E-13
+ VJ = 0.869
+ M = 0.03
+ FC = 0.5
+ TT = 3.48E-9
.ENDS

Vinput in 0 DC 0V AC SIN(0V 10V 50Hz 0s 0Hz)
C0 in 1 1mF
X0 1 0 1N4148
C1 0 2 1mF
X1 2 1 1N4148
C2 1 3 1mF
X2 3 2 1N4148
C3 2 4 1mF
X3 4 3 1N4148
C4 3 5 1mF
X4 5 4 1N4148
R1 5 6 1MegOhm
.options TEMP = 25°C
.options TNOM = 25°C
.options filetype = binary
.options NOINIT
.ic
.tran 0.0001s 0.4s 0s
.end
'''

circuit = "Multiple dc sources v1 1 0 dc 24 v2 3 0 dc 15 r1 1 2 10k r2 2 3 8.1k r3 2 0 4.7k .end "

circuit = '''
.title None
.subckt Fonte input output 
Vin input output 10V
.ends Fonte
X1 2 1 Fonte
R1 3 1 1K
R2 2 3 2K
.options TEMP = 25°C
.options TNOM = 25°C
.ic 
.tran 100us 3ms 0s
.end
'''

circuit = '''
* Simple RC Circuit

 

*Control section determines type of analysis

.control

destroy all

echo

TRAN 0.1MS 20MS

plot V(1) V(2) V(3)

.endc

 

*These next lines give circuit layout (netlist)

R1 1 2 1k

R2 2 0 1k

R3 3 0 1k

C1 2 3 1u

 

*form of pulse -- PULSE(V1 V2 TD TR TF PW PER)

VVin 1 0 PULSE(0 5 0 0 0 5m 10m)

 

.end
'''

ngspice.load_circuit(circuit)


print(ngspice.show('r1'))
print(ngspice.showmod('r1'))

ngspice.run()
print('Plots:', ngspice.plot_names)

print(ngspice.ressource_usage())
print(ngspice.status())

plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
print(plot)

