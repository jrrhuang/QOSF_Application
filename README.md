# QOSF Assessment Task 3
<p>Download <a href = "https://github.com/jrrhuang/QOSF_Application/blob/main/HuangJ_package.zip?raw=true">here</a></p>

## Summary
The goal of the task is to implement a basic quantum circuit simulator using code. Quantum superposition can be represented as state vectors, with entries denoting 
amplitudes of the basis states. These quantum states are not directly observable as they will collapse to a classical state upon measurement, which is the outcome 
that we measure. The odds of observing a specific classical state is the square of the magnitude of the amplitude for a given state. This feature allows us to 
obtain information about the quantum state.<br/>
We can manipulate the states of qubits through the use of quantum gates, represented mathematically by a matrix operator. Our simulator will use a circuit
(consisting of several gates) to manipulate qubits given in the ground state and give a measurement of the final state. Because the classical outcome of the final
state is determined probabilistically, the simulator randomly selects the outcome based on a probabilty distribution obtained from the final state vector. It
performs this measurement many times in order to print a distribution of outcomes, reflective of the probabilities from the final state vector. So although we 
are unable to directly observe the quantum states, we can approximate the amplitudes corresponding to the results from this distribution by reverse calculation.
<br/>

## Completed
- quantum simulator performing multi-shot measurement using weighted random<br/>
- parametric gates<br/>
- global parameters for variational algorithms
- universal operator function (V2)
