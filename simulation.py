from qiskit import QuantumCircuit, Aer, execute
import math


# Returns the angle of a rotation about the x-axis for a qubit to measure
# the given probability of being in the |1> state
def angle_from_prob(prob):
    return math.acos((2 * (1 - prob)) - 1)


# Use the angle of rotation of the qubit to reconstruct the probability
# of the qubit representing an infected population.
def extract_prob(count):
    return 1 - ((2 * math.acos(math.sqrt(count))) / math.pi)


def simulate_transmission(init_prob, transmit_rates, num_nodes, origin, backend):
    qc = QuantumCircuit(num_nodes)

    # Initialize the origin qubit with its initial probability to be infected prior to the circuit
    qc.rx(angle_from_prob(init_prob[origin]), origin)

    for target in range(num_nodes):
        if target == origin:
            continue

        # Use Hadamard gates so that rotations occur along the x-y plane which ensures
        # the target qubits have no Z component, allowing for less confusion with the origin
        qc.h(target)

        init_infected_prob = init_prob[target]
        transmit_rate = transmit_rates[origin][target]

        infected_by_transmit_prob = (1 - init_infected_prob) * transmit_rate

        # If the control bit is |0>, total rotation is equal to rotation_1 + rotation_2.
        # If the control bit is |1>, total rotation is equal to rotation_1 - rotation_2.
        rotation_1 = (-infected_by_transmit_prob / 2) * math.pi
        rotation_2 = ((infected_by_transmit_prob / 2) + init_infected_prob) * math.pi

        qc.rz(rotation_1, target)

        qc.cx(origin, target)

        qc.rz(rotation_2, target)

        # Return to standard basis before measurement.
        qc.h(target)

    results = execute(qc, backend).result()
    counts = results.get_counts()

    new_prob = [0] * num_nodes

    # Parse the results for the probabilities of a qubit being in the |1> state.
    for target in range(num_nodes):

        if target == origin:
            # The probability of infection for the origin node does not change.
            new_prob[origin] = init_prob[origin]
            continue

        results_sum = sum([counts[j] for j in counts if j[num_nodes - target - 1:num_nodes - target] == '1'])

        # Account for rounding errors which produce a sum greater than 1.
        new_prob[target] = extract_prob(results_sum if results_sum <= 1 else 1)

    return new_prob


def do_timestep(init_prob, transmit_rates, num_nodes):
    backend = Aer.get_backend('statevector_simulator')
    cur_prob = init_prob

    for origin in range(num_nodes):
        cur_prob = simulate_transmission(cur_prob, transmit_rates, num_nodes, origin, backend)

    return cur_prob
