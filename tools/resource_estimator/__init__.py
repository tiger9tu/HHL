"""Surface-code space, time, and energy estimation using Litinski's tile model."""

from .evaluate import evaluate_configuration
from .hhl import HHL, Task
from .models import ErrorBudget, Estimate, Hardware, InfeasibleConfiguration, PowerModel, Workload
from .optimize import optimize
from .protocols import (
    COMPACT, INTERMEDIATE, FAST, DATA_PROTOCOLS, DISTILLATION_PROTOCOLS,
    DISTILLATION_15_1, DISTILLATION_116_12, DISTILLATION_116_12_FAST,
    DISTILLATION_225_1,
)
