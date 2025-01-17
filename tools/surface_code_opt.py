import numpy as np


class Block:
    def __init__(self, number_of_tiles):
        self.number_of_tiles = number_of_tiles


class DistillationBlock(Block):
    def __init__(
        self,
        number_of_tiles,
        magic_production_time,
        error_rate_c,
        error_rate_t,
        name="",
    ):
        super().__init__(number_of_tiles)
        self.magic_production_time = magic_production_time
        self.error_rate_c = error_rate_c
        self.error_rate_t = error_rate_t
        self.name = name

    def error_rate(self, physical_error_rate):
        return self.error_rate_c * physical_error_rate**self.error_rate_t

    def __str__(self):
        return self.name


distillation_15_1 = DistillationBlock(
    number_of_tiles=11,
    magic_production_time=11,
    error_rate_c=35,
    error_rate_t=3,
    name="15-1",
)
distillation_116_12 = DistillationBlock(
    number_of_tiles=44,
    magic_production_time=9.27,
    error_rate_c=4.125,
    error_rate_t=4,
    name="116-12",
)


class DataBlock(Block):
    def __init__(
        self,
        magic_consumption_time,
        space_n_c,
        space_sqrt_n_c,
        space_c,
        name="",
    ):
        self.space_n_c = space_n_c
        self.space_sqrt_n_c = space_sqrt_n_c
        self.space_c = space_c
        self.magic_consumption_time = magic_consumption_time
        self.name = name

    def initialize(self, logical_qubits_n):
        number_of_tiles = (
            logical_qubits_n * self.space_n_c
            + np.sqrt(logical_qubits_n) * self.space_sqrt_n_c
            + self.space_c
        )
        super().__init__(number_of_tiles)

    def __str__(self):
        return self.name


# TODO: Add the freedom of choosing different ancilla distillation protocols
# distillation_116_12_ancilla = DistillationBlock(
#     number_of_tiles=81, magic_production_time=4.68, error_rate_c=4.125, error_rate_t=4
# )
distillation_225_1 = DistillationBlock(
    number_of_tiles=176,
    magic_production_time=5.5,
    error_rate_c=1.5,
    error_rate_t=7,
    name="225-1",
)  # not sure about the speed
distillation_protocals = [
    # the order is important, because we will choose the first one that satisfies the error rate
    distillation_15_1,
    distillation_116_12,
    # distillation_116_12_ancilla,
    distillation_225_1,
]


data_compact = DataBlock(
    magic_consumption_time=9, space_n_c=1.5, space_sqrt_n_c=0, space_c=3, name="Compact"
)
data_intermediate = DataBlock(
    magic_consumption_time=5,
    space_n_c=2,
    space_sqrt_n_c=0,
    space_c=4,
    name="Intermediate",
)
data_fast = DataBlock(
    magic_consumption_time=1,
    space_n_c=2,
    space_sqrt_n_c=np.sqrt(8),
    space_c=1,
    name="Fast",
)
data_protocals = [data_compact, data_intermediate, data_fast]


def initialize(logical_qubit_count):
    for data_protocol in data_protocals:
        data_protocol.initialize(logical_qubit_count)


def determine_distillation_protocol(physical_error_rate, target_error=0.01):
    """
    Step 1: Determine the most cost-effective distillation protocol that satisfies the error rate.
    """
    most_cost_effective = 3
    minimal_number_of_tiles = float("inf")
    for i, distillation_protocol in enumerate(distillation_protocals):
        if distillation_protocol.error_rate(physical_error_rate) < target_error:
            if distillation_protocol.number_of_tiles < minimal_number_of_tiles:
                most_cost_effective = i
                minimal_number_of_tiles = distillation_protocol.number_of_tiles

    return most_cost_effective


def construct_minimal_setup(distillation_block, T_count):
    """
    Step 2: Construct minimal tile setup. Decide minimal qubits needed for distillation and data blocks.
    """
    # TODO: In the paper, the total tiles has to add by storage tiles, but we omit it here.
    total_tiles = data_compact.number_of_tiles + distillation_block.number_of_tiles
    total_time_step = distillation_block.magic_production_time * T_count
    return total_tiles, total_time_step


def determine_code_distance(
    physical_error_rate, total_tiles, total_time_step, target_error=0.01
):
    """
    Step 3: Determine minimal code distance to meet target logical error rate.
    """

    def p_l(physical_error_rate, d):
        return 0.1 * (100 * physical_error_rate) ** ((d + 1) / 2)

    max_d = 100
    for d in range(1, max_d):
        if (
            total_tiles * total_time_step * d * p_l(physical_error_rate, d)
            < target_error
        ):
            return d

    return max_d  # This is a sign of failure


def optimize_configuration(distillation_block, d, T_count, max_physical_qubits=1e6):
    """
    Step 4: Optimize configuration by adding distillation blocks and changing data block protocols.
    """

    # now we have the freedom to:
    # 1.change the number of distillation blocks (the type of distillation block is fixed)
    # 2.change the data block protocol

    space_time_cost = float("inf")
    optimal_distillation_block_count = None
    optimal_data_protocol = None
    optimal_cycle_count = None
    optimal_physical_qubit_count = None

    for n_distillation in range(1, 100):
        for data_protocol in data_protocals:

            magic_production_time = (
                distillation_block.magic_production_time / n_distillation
            )

            magic_time = max(
                magic_production_time, data_protocol.magic_consumption_time
            )

            total_clock_cycles = magic_time * T_count

            total_tiles = (
                data_protocol.number_of_tiles
                + distillation_block.number_of_tiles * n_distillation
            )

            total_physical_qubits = total_tiles * 2 * d * d
            if total_physical_qubits > max_physical_qubits:
                break

            total_space_time_cost = total_physical_qubits * total_clock_cycles
            if total_space_time_cost < space_time_cost:
                # print(
                #     f"n_distillation: {n_distillation}, data_protocol: {data_protocol},total_physical_qubits: {total_physical_qubits}, total_clock_cycles: {total_clock_cycles}"
                # )
                space_time_cost = total_space_time_cost
                optimal_distillation_block_count = n_distillation
                optimal_data_protocol = data_protocol
                optimal_cycle_count = total_clock_cycles
                optimal_physical_qubit_count = total_physical_qubits

                space_time_cost = total_space_time_cost

            if (
                data_protocol.magic_consumption_time
                < data_protocol.magic_consumption_time
            ):
                break  # we can skip the rest of the data protocols, because now the bottleneck is the number of distillation blocks
    return (
        optimal_distillation_block_count,
        optimal_data_protocol,
        optimal_cycle_count,
        optimal_physical_qubit_count,
    )


def find_optimal_setting(
    t_gate_count, logical_qubit_count, physical_error_rate, max_physical_qubits
):
    initialize(logical_qubit_count)

    distillation_protocal_index = determine_distillation_protocol(physical_error_rate)
    setup_tiles, setup_time = construct_minimal_setup(
        distillation_protocals[distillation_protocal_index], t_gate_count
    )
    code_distance = determine_code_distance(
        physical_error_rate, setup_tiles, setup_time
    )
    (
        optimal_distillation_block_count,
        optimal_data_protocol,
        optimal_cycle_count,
        optimal_physical_qubit_count,
    ) = optimize_configuration(
        distillation_protocals[distillation_protocal_index],
        code_distance,
        t_gate_count,
        max_physical_qubits,
    )

    return (
        optimal_distillation_block_count,
        optimal_data_protocol,
        optimal_cycle_count,
        optimal_physical_qubit_count,
    )


class Task:
    def __init__(
        self,
        logical_qubit_count,
        t_gate_count,
    ):
        self.logical_qubit_count = logical_qubit_count
        self.t_gate_count = t_gate_count


class HHL(Task):
    def __init__(
        self, n, sparsity, kappa, epsilon, precision  # n, number of input qubits
    ):
        hs_count = np.sqrt(80 / 3) * np.pi * kappa ** (5 / 2) * sparsity / epsilon**2
        t_count = hs_count * (
            12 * 4 * n + 4 * 2 * n + 15 * 54
        )  # precision is the number of bits
        self.ancilla_qubits = 20  # suppose HHL's ancilla qubits are 20
        clock_qubit_count = np.ceil(np.log2(np.sqrt(5 / 3) * kappa / epsilon))
        precision_qubit_count = precision
        logical_qubit_count = 2 * n + precision_qubit_count + clock_qubit_count
        # logical_qubit_count = n
        super().__init__(logical_qubit_count, t_count)


# if __name__ == "__main__":
#     # t_gate_count = 1e8
#     # logical_qubit_count = 100

#     physical_error_rate = 1e-4
#     clock_cycle_time = 1e-6
#     max_physical_qubits = 80000

#     # setting of HHl
#     kappa = 2
#     epsilon = 0.1
#     precision = 5

#     opt_dist_block_counts = []
#     opt_data_protos = []
#     opt_time = []
#     opt_physical_qubit_count = []

#     for n in range(10, 50):
#         sparsity = n / 16  # this is for consistency with the plots on the paper
#         hhl_task = HHL(n, sparsity, kappa, epsilon, precision)

#         (
#             optimal_distillation_block_count,
#             optimal_data_protocol,
#             optimal_cycle_count,
#             optimal_physical_qubit_count,
#         ) = find_optimal_setting(
#             hhl_task.t_gate_count,
#             hhl_task.logical_qubit_count,
#             physical_error_rate,
#             max_physical_qubits,
#         )

#         opt_dist_block_counts.append(optimal_distillation_block_count)
#         opt_data_protos.append(optimal_data_protocol)
#         opt_time.append(optimal_cycle_count * clock_cycle_time)
#         opt_physical_qubit_count.append(optimal_physical_qubit_count)
