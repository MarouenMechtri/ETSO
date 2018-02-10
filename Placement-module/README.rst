#### 
Placement module of the ETSO Framework
####


In this guide, we show how to customize the placement module `"placement.py" <placement.py>`_ to deal with a specific resource placement algorithm available in the placement package `"placementAlgo.jar" <placementAlgo.jar>`_. 
Then we describe the inputs and output of the placement algorithms and show how we can add and package a new one. A dummy algorithm was developed to easily integrate a new algorithm in the ETSO framework.


===============================

**Authors:**

Copyright (C) `Marouane Mechteri <https://www.linkedin.com/in/mechtri>`_


================================

.. contents::


Configuration of the placement module and selection of the placement algorithm
==============================================================================

sudo apt-get install libgfortran3

The placement module embeds a family of optimization algorithms to intelligently place VMs or VNFs in underlying NFVIs and to steer traffic flows across the VNFs while using efficiently the infrastructure resources. A set of algorithms are already integrated in the placement package `"placementAlgo.jar" <placementAlgo.jar>`_, and can be selected, invoked, and activated.
The available algorithms are: 

1. An Eigendecomposition-based algorithm: `A Scalable Algorithm for the Placement of Service Function Chains <https://www.researchgate.net/publication/305821223_A_Scalable_Algorithm_for_the_Placement_of_Service_Function_Chains>`_
2. A Dynamic Programming algorithm: `A Dynamic Programming Algorithm for Joint VNF Placement and Chaining <https://www.researchgate.net/publication/311313588_A_Dynamic_Programming_Algorithm_for_Joint_VNF_Placement_and_Chaining>`_
3. A Greedy algorithm: `VNF Placement and Chaining in Distributed Cloud <https://www.researchgate.net/publication/312570696_VNF_Placement_and_Chaining_in_Distributed_Cloud>`_
4. An algorithm based on the Monte Carlo Tree Search (MCTS): `An Efficient Algorithm for Virtual Network Function Placement and Chaining <https://www.researchgate.net/publication/318579373_An_efficient_algorithm_for_virtual_network_function_placement_and_chaining>`_

