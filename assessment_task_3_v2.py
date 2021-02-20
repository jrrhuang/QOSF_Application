"""
Jerry Huang Task 3.
Version 2 implements everything in version 1 in addition to universal
operator function.
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


def get_operator(dim, gate_unitary_lst, target_qubits):
    """
    Return unitary operator for given operator (including universal operators)
    and target qubits.

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

    # operator

    O = np.zeros([dim, dim])

    # keep track of all projection combinations according to binary digits

    curr = ""
    for c in gate_unitary_lst:
        if c == "c":
            curr += "0"

    # loop through all combinations and add to operator

    for i in range(2 ** len(curr)):
        idx = 0
        if target_qubits[0] == 0:
            if len(curr) != 0:
                O_temp = choice(curr[idx])
            else:
                O_temp = gate_unitary_lst[idx]
            idx += 1
        else:
            O_temp = I

        for j in range(1, int(np.log2(dim))):
            if j in target_qubits:
                if idx < len(curr):
                    O_temp = np.kron(O_temp, choice(curr[idx]))
                    idx += 1
                elif curr.find("0") == -1:
                    gate = gate_unitary_lst[idx]
                    O_temp = np.kron(O_temp, gate)
                    idx += 1
                else:
                    O_temp = np.kron(O_temp, I)
            else:
                O_temp = np.kron(O_temp, I)
        O = O + O_temp
        curr = next_bin(curr)

    return O


def choice(c):
    """Return projection depending on character."""

    P0x0 = np.array([[1, 0], [0, 0]])
    P1x1 = np.array([[0, 0], [0, 1]])

    if c == "0":
        return P0x0
    return P1x1


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
    for spec in program:
        lst = []
        for c in spec["gate"]:
            if c == 'c':
                lst.append('c')
            elif c != 'u' and c != '3':
                lst.append(get_unitary(spec, par, c))
            if c == '3':
                lst.append(get_unitary(spec, par, 'u3'))

        O = get_operator(len(q), lst, spec["target"])
        q = np.dot(O, q)

    return q


def get_unitary(spec, par, gate):
    """Extract unitary matrix from circuit specifications."""

    unitary = gate_dict[gate]
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
            idx.append(next_bin(idx[-1]))
        prob.append(np.abs(state_vector[i] ** 2))

    return np.random.choice(idx, 1, p=prob)[0]


def next_bin(s):
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
