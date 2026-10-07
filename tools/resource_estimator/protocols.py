"""Litinski, arXiv:1808.02892v3, Sections 2--4.

Tile formulas are architecture estimates, not an automatic routing proof.
"""

import math
from typing import NamedTuple


class DataProtocol(NamedTuple):
    name: str
    magic_consumption_time: float

    def tiles(self, logical_qubits):
        if self.name == "Compact":
            return int(math.ceil(1.5 * logical_qubits + 3))
        if self.name == "Intermediate":
            # Sec. 2.2 and Sec. 4.4 agree on 2n+4. Fig. 13(a)'s 2.5n+4
            # caption is inconsistent; preserve the original script's 2n+4.
            return 2 * logical_qubits + 4
        if self.name == "Fast":
            # Pair patches in a near-square array, shortening the last column
            # as described in Sec. 2.3. An odd input pads to a full pair.
            pairs = (logical_qubits + 1) // 2
            width = max(1, int(round(math.sqrt(pairs))))
            height = (pairs + width - 1) // width
            return 4 * pairs + 2 * (width + height) + 1
        raise ValueError("Unknown data protocol: " + self.name)


class DistillationProtocol(NamedTuple):
    name: str
    number_of_tiles: int
    batch_steps: float
    output_states: int
    error_rate_c: float
    error_rate_t: int
    rejection_exponent: int
    buffer_tiles: int

    def error_rate(self, physical_error_rate):
        return self.error_rate_c * physical_error_rate ** self.error_rate_t

    def production_steps(self, physical_error_rate, include_rejections=True):
        success = ((1 - physical_error_rate) ** self.rejection_exponent
                   if include_rejections else 1.0)
        return self.batch_steps / (self.output_states * success)

    def storage_tiles(self, data_protocol, factory_count):
        # Fig. 21a/22a: 15-to-1 directly feeds compact/intermediate data.
        # Fig. 23a: each 15-to-1 factory has one additional storage tile.
        # For 116-to-12 retain 13 buffer tiles/factory (Fig. 21b). More
        # elaborate fast layouts can share storage and require extra routing.
        per_factory = self.buffer_tiles
        if self.name == "15-1" and data_protocol.name == "Fast":
            per_factory = 1
        return per_factory * factory_count


COMPACT = DataProtocol("Compact", 9)
INTERMEDIATE = DataProtocol("Intermediate", 5)
FAST = DataProtocol("Fast", 1)
DATA_PROTOCOLS = (COMPACT, INTERMEDIATE, FAST)

DISTILLATION_15_1 = DistillationProtocol("15-1", 11, 11, 1, 35, 3, 15, 0)
DISTILLATION_116_12 = DistillationProtocol(
    "116-12", 44, 99, 12, 41.25, 4, 116, 13)
# Sec. 3.5: 35*(35*p**3)**3, NOT 1.5*p**7; 176 tiles for 15 steps.
# The rejection correction approximates level-1 stalls, as in Sec. 3.5;
# it does not simulate the multi-level distillation schedule.
DISTILLATION_225_1 = DistillationProtocol(
    "225-1", 176, 15, 1, 35 ** 4, 9, 15, 1)
DISTILLATION_116_12_FAST = DistillationProtocol(
    "116-12-fast", 81, 50, 12, 41.25, 4, 116, 13)
# Preserve old numerical indices 0/1/2; the 81-tile variant is appended.
DISTILLATION_PROTOCOLS = (
    DISTILLATION_15_1, DISTILLATION_116_12, DISTILLATION_225_1,
    DISTILLATION_116_12_FAST,
)
