import numpy as np


HADAMARD = 1j * np.array(
    [
        [1, 1],
        [1, -1]
    ]
) / np.sqrt(2)

ID = np.array(
    [
        [1, 0],
        [0, 1]
    ]
)

NOT = np.array(
    [
        [0, 1],
        [1, 0]
    ]
)

CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0 ,0, 1j],
        [0, 0, 1j, 0]
    ]
)