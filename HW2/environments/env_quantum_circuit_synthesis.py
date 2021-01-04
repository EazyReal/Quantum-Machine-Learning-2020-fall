# -*- coding: utf-8 -*-
"""
Copyright 2018 Alexey Melnikov and Katja Ried.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

Please acknowledge the authors when re-using this code and maintain this notice intact.
Code written by Alexey Melnikov and Katja Ried, implementing ideas from 

'Projective simulation with generalization'
Alexey A. Melnikov, Adi Makmal, Vedran Dunjko & Hans J. Briegel
Scientific Reports 7, Article number: 14430 (2017) doi:10.1038/s41598-017-14740-y
"""

"""
Copyright 2021 Yan-Tong Lin.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
Please acknowledge the authors when re-using this code and maintain this notice intact.

This is a brand new environment created by Yan-Tong Lin based on the project above.
"""

#This code requires the following packages
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import *
from qiskit import Aer
from qiskit import execute

"""
example of env_config
n_qubit = 2
allowed_gates = [
    (HGate, [0]),
    (HGate, [1]),
    (XGate, [0]),
    (XGate, [1]),
    (ZGate, [0]),
    (ZGate, [1]),
    (CXGate, [0,1]),
]
target_circuit = QuantumCircuit(n_qubit)
target_circuit.h([0,1])
target_circuit.z([0,1])
target_circuit.cz(0,1)
target_circuit.h([0,1])
env_config = (n_qubit, allowed_gates, target_circuit)
"""


class TaskEnvironment(object):
    """
    Quantum Circuit Synthesis Experiment Enviraonment for QML 2020 fall @ Taiwan 
    """
    
    def __init__ (self, config):
        """
        config = (n_qubit, allowed_gates, target_circuit)
        n_qubit: int
        allowed_gates: List[Gate, [bits]]
        target_circuit: QuantumCircuit
        """
        n_qubit, allowed_gates, target_circuit = config
        self.n_qubit = n_qubit
        self.max_steps_per_trial = 10**4
        # self.num_percepts_list = dimensions
        self.current_circuit = QuantumCircuit(self.n_qubit) 
        self.target_circuit = target_circuit
        # Reward is specified by checking equivelance of two circuits --- current and target
        self.act_list = allowed_gates
        #The first entry refers to forbidden x moves, the second to y.
        self.num_actions = len(self.act_list)
    
    def reset(self):
        self.current_circuit = QuantumCircuit(self.n_qubit) 
        return self.current_circuit.qasm(formatted=False)
    
    def move(self,action_index):
        """Given the agent's action index (int 0-3), returns the new position, reward and trial_finished."""
        #test whether the action is permissible   
        action = self.act_list[action_index]
        #Do the Action
        gate, applied = action
        self.current_circuit.append(gate(), applied) # gate() is to instantialize a object from a gate class
        #Test if has reward 
        backend_sim = Aer.get_backend('unitary_simulator')
        job_sim = execute([self.current_circuit, self.target_circuit], backend_sim)
        result_sim = job_sim.result()
        current_unitary = result_sim.get_unitary(self.current_circuit)
        target_unitary = result_sim.get_unitary(self.target_circuit)
        # reward = 1 if (abs(current_unitary-target_unitary) < 1e-5).all() else 0
        reward = np.allclose(current_unitary, target_unitary)
        trial_finished = False
        solution = None
        if reward == 1:  #reset to origin to avoid agent hanging around target all the time
            # solution = self.current_circuit
            self.current_circuit = QuantumCircuit(self.n_qubit) 
            trial_finished = True
        return self.current_circuit.qasm(formatted=False), reward, trial_finished #, solution

    def get_circuit(self):
        return self.current_circuit
        