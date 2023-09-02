# QuantumAmplifier
A Novel Quantum Amplifier Circuit Simulated in QuTiP.

This script simulates a novel quantum amplifier circuit in QuTiP.  The amplification circuit is as follows.

![alt text](https://github.com/Northerneye/QuantumAmplifier/blob/main/AmplificationCircuit.png?raw=true)

This circuit operates off of two interactions, one of which turns signal and drive excitations into storage and cooling excitation as follows.  The cooling excitation is quickly lost.

![alt text](https://github.com/Northerneye/QuantumAmplifier/blob/main/Drive1_wcoupl0.3__g1.0__ext_strength3_len_1000_coolext_0.2.png?raw=true)

The second interaction turns a storage and drive excitation into two signal excitations as follows.

![alt text](https://github.com/Northerneye/QuantumAmplifier/blob/main/DriveStorage0_wcoupl0.3__g1.0__ext_strength3_len_1000_coolext_0.2.png?raw=true)

This is an example of a full round of amplification of the circuit, which turns the expectation value of photons in the signal resonator from 1 to 1.6.

![alt text](https://github.com/Northerneye/QuantumAmplifier/blob/main/Signal_wcoupl0.3__g1.0__ext_strength3_len_1000_coolext_0.2.png?raw=true)

This is two rounds of amplification, which sadly returns a lower average excitation as the signal resonator tends to relax faster than it can be amplified in the current design.

![alt text](https://github.com/Northerneye/QuantumAmplifier/blob/main/Signal_wcoupl0.3__g1.0__ext_strength3_len_3000_coolext_0.2.png?raw=true)

The paper on this quantum amplifier circuit further describing its operation can be found here.

[embed]https://cameroncianci.com/wp-content/uploads/2023/09/Quantum_Pre_Amplifier.pdf[/embed]
