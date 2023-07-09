#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Created on Thu Aug 27 21:54:22 2020

@author: Abdellah Tounsi

Fibonacci
********
Defines Fibonacci anyonic model (SU(2)_3) by their fusion rules and computes
braiding generators of any possible qudit represented by Fibonacci anyons.

Ex:

    1 1 1 1 1
    \/ / / /
    i\/ / /
     j\/ /
      k\/
       l\
    outcomes of the state |((((1, 1)_i, 1)_j, 1)_k, 1)_l| are [i, j, k, l]

This model is designed to:
    + check fusion rule validity.
    + check ayonic state validity.
    + generates the basis of fusion space in the standard form (left
    to right fusion order).
    + defines F and R matrices.
    + generates B (braiding) matrices.
    + calculates braiding generators (sigma_n).
"""
import numpy as np
from typing import List
from copy import deepcopy
from codes.cplot import cplot


def check_rule(anyon_1, anyon_2, outcome):
    """
    anyons can be either 0 or 1.
    """
    check = False
    if anyon_1 == 1 and anyon_2 == 1:
        check = True

    elif anyon_1 == 1 or anyon_2 == 1:
        if outcome == 1:
            check = True
    else:
        if outcome == 0:
            check = True

    return check


def check_state(outcomes: List):
    r"""checks if a state is valid in Fibonacci models. Ex:
        1 1 1 1
        \/ / /
        i\/ /
         j\/
          k\
        outcomes of the state |((((1, 1)_i, 1)_j, 1)_k, 1)_l| are [i, j, k, l]
    Inputs:
        outcomes: list:
            outcomes of the fusion tree by order (L to R)
    """
    check = True
    previous_outcome = 1
    for outcome in outcomes:
        if check_rule(previous_outcome, 1, outcome):
            previous_outcome = outcome
        else:
            check = False
            break

    return check


def find_basis(n_anyons):
    """
    generates all states that form the basis of Hilbert space of n_anyons.
    Inputs:
        n_anyons: in:
            number of anyons.
    Returns:
        List[List]: list of states with their labeling outcomes.
    """
    n_labels = n_anyons - 1

    # Generate all combinations and check if
    # they verify Fibonacci rules
    # (To do) combinations can be generated with binary methods.

    new_comb = []
    final_comb = []
    for _ in range(n_labels):
        new_comb.append(0)
        final_comb.append(1)
    
    states = []
    if check_state(new_comb):
        new_state = deepcopy(new_comb)
        states.append(new_state)

    while not new_comb == final_comb:
        for i, label in enumerate(new_comb):
            if label == 0:
                new_comb[i] = 1
                break
            else:
                new_comb[i] = 0
        if check_state(new_comb):
            new_state = deepcopy(new_comb)
            states.append(new_state)

    return states


def F(a1, a2, a3, outcome):
    """
    F matrix
    """
    inv_phi = (np.sqrt(5) - 1) / 2  # inverse of golden number
    f_matrix = np.array([[0, 0], [0, 0]])

    # a1 + a2 + a3 + outcome = 4
    if a1 + a2 + a3 + outcome == 4:
        f_matrix = np.array([[inv_phi, np.sqrt(inv_phi)],
                             [np.sqrt(inv_phi), -inv_phi]])

    # a1 + a2 + a3 + outcome = 3
    elif a1 + a2 + a3 + outcome == 3:
        f_matrix = np.array([[0, 0], [0, 1]])

    # a1 + a2 + a3 + outcome = 2
    elif a1 + a2 + a3 + outcome == 2:
        if a1 + a2 == 2:
            f_matrix = np.array([[0, 1], [0, 0]])
        elif a2 + a3 == 2:
            f_matrix = np.array([[0, 0], [1, 0]])
        elif a1 + a3 == 2:
            f_matrix = np.array([[0, 0], [0, 1]])
        elif a3 + outcome == 2:
            f_matrix = np.array([[0, 1], [0, 0]])
        elif a1 + outcome == 2:
            f_matrix = np.array([[0, 0], [1, 0]])
        elif a2 + outcome == 2:
            f_matrix = np.array([[0, 0], [0, 1]])

    # a1 + a2 + a3 + outcome = 1
    # a1 + a2 + a3 + outcome = 0
    elif a1 + a2 + a3 + outcome == 0:
        f_matrix = np.array([[1, 0], [0, 0]])

    return f_matrix


def R(a1, a2):
    """
    R matrix
    """
    if a1 + a2 == 2:
        r_matrix = np.array([[np.exp(-4 * np.pi * 1j / 5), 0],
                             [0, np.exp(3 * np.pi * 1j / 5)]])
    else:
        r_matrix = np.array([[1, 0], [0, 1]])

    return r_matrix


def B(a0, a1, a2, outcome):
    """
    Braiding matrix
    """
    b_matrix = F(a0, a1, a2, outcome)\
        @ R(a1, a2) @ F(a0, a2, a1, outcome).conjugate().T

    return b_matrix


def sigma(index, state_f, state_i):
    """
    Amplitude of getting state_f by applying the braiding operator
    sigma_{index} on state_i.

    Returns:
        the component (state_f, state_i) of the sigma_{index} matrix
    """
    if index <= 0 or index > len(state_i):
        raise ValueError("index value is not valid!")

    stt_f = [1] + state_f
    stt_i = [1] + state_i

    if index - 2 < 0:
        a0 = 0
    elif index - 2 == 0:
        a0 = 1
    else:
        a0 = state_i[index - 3]

    outcome = state_i[index - 1]
    a = stt_i[index - 1]
    b = stt_f[index - 1]

    ket = stt_i
    ket[index - 1] = b
    bra = stt_f
    if ket != bra:
        return 0

    return B(a0, 1, 1, outcome)[a, b]


def braiding_generator(index, n_anyons, show=True):
    """
    calculates the matrix of the braiding generator that exchange
    index'th anyon with the (index + 1)'th anyon.
    Inputs:
        index: int:
        n_anyons: int:
            number of anyons.
    Returns:
        (numpy.array whose dimension equals to the dimension of
        anyons' Hilbert space, basis)
    """

    # basis of Hilbert space
    basis = find_basis(n_anyons)

    # compute components of the braiding matrix
    sig = []
    for f, state_f in enumerate(basis):
        sig.append([])
        for i, state_i in enumerate(basis):
            sig[f].append(sigma(index, state_f, state_i))
    if show:
        cplot(sig)

    return sig, basis
