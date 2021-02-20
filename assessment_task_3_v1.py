"""
Jerry Huang Task 3.
Implements single qubit gates and CNOT.
"""

import numpy as np
from numpy import exp, pi, cos, sin

gate_dict = {
    "h": np.array([[0.70710678, 0.70710678], [0.70710678, -0.70710678]]),
    "x": np.array([[0, 1], [1, 0]]),
    "cx": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    "y": np.array([[0, -1j], [1j, 0]]),
    "z": np.array([[1, 0], [0, -1]]),
    "s": np.array([[1, 0], [0, exp(-pi / 2 * 1j)]]),
    "t": np.array([[1, 0], [0, exp(-pi / 4 * 1j)]]),
    "u3": np.array([["cos(th / 2)", "-exp(1j * la) * sin(th / 2)"],
                    ["exp(1j * phi) * sin(th / 2)",
                     "exp(1j * la + 1j * phi) * cos(th / 2)"]])
}


def get_ground_state(num_qubits):
    """
    Return vector of size 2**(num_qubits) with all zeroes except first element
    which is 1.

    :param num_qubits:
        int number of qubits
    :return:
        numpy array denoting ground state vector
    """

    psi = np.array([1] + [0] * (2 ** num_qubits - 1))
    return psi


def get_operator(total_qubits, gate_unitary, target_qubits):
    """
    Return unitary operator for given operator and target qubits.

    :param dim:
        int dimensions of state_vector in the form of 2**n
    :param gate_unitary_lst:
        list of control and unitary gates in operator
    :param target_qubits:
        list of control and gate indices
    :return:
        numpy array denoting unitary operator of size dim x dim
    """

    I = np.identity(2)
    O = []

    # single qubit gates

    if len(target_qubits) == 1:
        for i in range(total_qubits):
            if i == 0:
                if target_qubits[0] == i:
                    O = gate_unitary
                else:
                    O = I
            else:
                if target_qubits[0] == i:
                    O = np.kron(O, gate_unitary)
                else:
                    O = np.kron(O, I)

    # CNOT

    P0x0 = np.array([[1, 0], [0, 0]])
    P1x1 = np.array([[0, 0], [0, 1]])

    if len(target_qubits) == 2:
        gate = np.array([gate_unitary[2][2:], gate_unitary[3][2:]])
        if target_qubits[0] == 0:
            O_0 = P0x0
            O_1 = P1x1
        else:
            O_0 = I
            O_1 = I

        for i in range(1, total_qubits):
            O_0 = np.kron(O_0, I)
            if target_qubits[1] == i:
                O_1 = np.kron(O_1, gate)
            else:
                O_1 = np.kron(O_1, I)

        O = O_0 + O_1

    return O


def run_program(initial_state, program, par={}):
    """
    Read program, extract matrix operator for each gate, and obtain
    final state by multiplying state vector with operator.

    :param initial_state:
        numpy array denoting ground state vector
    :param
        program: list of specifications for gates
    :param par:
        (optional) parameters for variational algorithms
    :return:
        numpy array denoting final state vector
    """

    q = initial_state
    total = int(np.log2(len(q)))
    for spec in program:
        unitary = get_unitary(spec, par)
        O = get_operator(total, unitary, spec["target"])
        q = np.dot(O, q)

    return q


def get_unitary(spec, par):
    """Extract unitary matrix from circuit specifications."""

    unitary = gate_dict[spec["gate"]]
    if "params" in spec:
        th = spec["params"]["theta"]
        if th in par:
            th = par[th]

        phi = spec["params"]["phi"]
        if phi in par:
            phi = par[phi]

        la = spec["params"]["lambda"]
        if la in par:
            la = par[la]

        return np.array([[eval(unitary[0][0]), eval(unitary[0][1])],
                         [eval(unitary[1][0]), eval(unitary[1][1])]])

    return unitary


def measure_all(state_vector):
    """Choose element from state_vector using weighted random."""

    prob = []
    idx = ["0" * int(np.log2(len(state_vector)))]

    for i in range(len(state_vector)):
        if not i == 0:
            idx.append(next_idx(idx[-1]))
        prob.append(np.abs(state_vector[i] ** 2))

    return np.random.choice(idx, 1, p=prob)[0]


def next_idx(s):
    """Return string representing next binary index."""

    b_lst = list(s[::-1])

    for i, bit in enumerate(b_lst):
        if bit == "0":
            b_lst[i] = "1"
            break
        else:
            b_lst[i] = "0"

    return "".join(b_lst[::-1])


def get_counts(state_vector, num_shots):
    """
    Loop num_shots times, select index according to weighted random, and return
    statistic of result.

    :param state_vector:
        numpy array with final state vector
    :param num_shots:
        int number of times to loop
    :return:
        dictionary with results
    """

    dict = {}
    for i in range(num_shots):
        idx = measure_all(state_vector)
        if idx not in dict:
            dict[idx] = 1
        else:
            dict[idx] += 1

    return dict
