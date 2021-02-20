# QOSF Assessment Task 3
<p>Download <a href = "https://github.com/jrrhuang/QOSF_Application/blob/main/HuangJ_package.zip?raw=true">here</a></p>

The goal of the task is to implement a basic quantum circuit simulator using code. Quantum states can be represented as vectors, with entries denoting amplitudes
of the basis states. Quantum states are not directly observable, so they will collapse to a classical state upon measurement, which is the outcome that we measure. 
This classical state is determined probabilistically as the square of the magnitude of the amplitude for a given state. We will see that this feature, in fact, 
allows us to determine information about the quantum state.<br/>
We can manipulate the states of qubits through the use of quantum gates, represented mathematically by a matrix operator. Our simulator will use a circuit
(consisting of several gates) to manipulate qubits given in ground state and give a measurement of the final state. Because the classical measurement of the final
state is determined probabilistically, the simulator randomly selects the outcome based on a probabilty distribution obtained from the final state vector. It
performs this measurement many times in order to print a distribution of outcomes, reflective of the probabilities from the final state vector. So although we 
are unable to directly observe the quantum states, we can infer the amplitudes of the quantum states from this distribution.

