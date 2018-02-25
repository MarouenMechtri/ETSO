#### 
Placement module of the ETSO Framework
####


This guide describes how to customize the placement module `"placement.py" <placement.py>`_ to use our placement algorithm available in the placement package `"placementAlgo.jar" <placementAlgo.jar>`_. 
Then we describe the inputs and output of the placement algorithms and show how we can add and package a new one. A dummy algorithm was developed to easily integrate a new algorithm in the ETSO framework.


===============================

**Authors:**

Copyright (C) `Marouane Mechteri <https://www.linkedin.com/in/mechtri>`_


================================

.. contents::


Configuration of the placement module and selection of the placement algorithm
==============================================================================


The placement module embeds a family of optimization algorithms to intelligently place VMs or VNFs in underlying NFVIs and to steer traffic flows across the VNFs while using efficiently the infrastructure resources. A set of algorithms are already integrated in the placement package `"placementAlgo.jar" <placementAlgo.jar>`_, and can be selected, invoked, and activated.
The available algorithms are: 

1. An Eigendecomposition-based algorithm: `A Scalable Algorithm for the Placement of Service Function Chains <https://www.researchgate.net/publication/305821223_A_Scalable_Algorithm_for_the_Placement_of_Service_Function_Chains>`_
2. A Dynamic Programming algorithm: `A Dynamic Programming Algorithm for Joint VNF Placement and Chaining <https://www.researchgate.net/publication/311313588_A_Dynamic_Programming_Algorithm_for_Joint_VNF_Placement_and_Chaining>`_
3. A Greedy algorithm: `VNF Placement and Chaining in Distributed Cloud <https://www.researchgate.net/publication/312570696_VNF_Placement_and_Chaining_in_Distributed_Cloud>`_
4. An algorithm based on the Monte Carlo Tree Search (MCTS): `An Efficient Algorithm for Virtual Network Function Placement and Chaining <https://www.researchgate.net/publication/318579373_An_efficient_algorithm_for_virtual_network_function_placement_and_chaining>`_


To select one of the algorithm available in the placement package, update the `orchestrator.py file <../SFC-orchestrator/sfc-orchestrator.py>`_ and precisely placement_headers['algorithm'] variable with one of these values:

- eigen
- dp
- greedy
- mcts


Install prerequisite package::

   sudo apt-get install libgfortran3

Figure below shows the part of the code that should be changed::

   vi SFC-orchestrator/sfc-orchestrator.py

   placement_headers = {}
   placement_headers['content-type'] = 'application/json'
   placement_headers['algorithm'] = 'algorithm_name'
   placement_headers['version'] = str(credentials.VERSION)
   placement_headers['username'] = credentials.USERNAME



.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/orchestratorpy.png


Inputs and Output of the placement algorithms
=============================================


The inputs of each placement algorithm are:

* The client request is modeled by a graph composed by a set of virtual nodes representing VNF and a set of virtual links connecting them. `instanceIG3-0 <instanceIG3-0>`_ is an example of a request composed by 3 VNFs and 2 links and representing a service chain::

   Number of Servers
   3 1 1
   Nodes
   0 0 2 3 1 0
   1 1 2 3 1 0
   2 2 2 3 1 0
   EDGES
   0 1 100
   1 2 100

* The substrate graph is modeled also by a graph. `instanceRG13-0 <instanceRG13-0>`_ is an example of a substrate infrastructure.

The output of the algorithms is a file containing the mapping result of the client request on the substrate infrastructure. The file name of the algorithm output has this format: SolutionMappingALGO-SUBSTRATE_FILE_NAME-REQUEST_FILE_NAME. For example, when executing the dynamic programming algorithm the output file name is SolutionMappingDP-instanceRG13-0-instanceIG3-0.


The Dummy algorithm
===================


In this section, we show the procedure to add a new algorithm in the ETSO framework:

* The first step of the procedure is to download the `ETSO dummy algorithm <https://github.com/MarouenMechtri/ETSO_dummy_algorithm>`_ package::

   git clone https://github.com/MarouenMechtri/ETSO_dummy_algorithm.git


* The second step is to add the new algorithm in the `dummy_algo.java <https://raw.githubusercontent.com/MarouenMechtri/ETSO_dummy_algorithm/master/src/dummy_algo/dummy_algo.java>`_::

   vi ETSO_dummy_algorithm/src/dummy_algo/dummy_algo.java

.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/dummy_algojava1.png

The call to the new algorithm must be made after reading the input files (request and substrate files) then the result of the algorithm must be saved in the matrix **mappingResult**. In the dummy example, we made a simple resource assignment which consists of assigning the first VM to the first server, the second VM to the second server...


* The third step of the procedure is to make sure that the output file of the algorithm respect the format described earlier (see figure below).

.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/dummy_algojava.png


* The fourth step consists on updating the `PlacementAlgo.java file <https://raw.githubusercontent.com/MarouenMechtri/ETSO_dummy_algorithm/master/src/placementSFC/PlacementAlgo.java>`_ which is the interface between the placement module of the ETSO framework and placement package that will encapsulate the new algorithm::

   vi ETSO_dummy_algorithm/src/placementSFC/PlacementAlgo.java

* The fifth step is to generate and to export a runnable jar file. Figure below show how to generate the jar file via the eclipse

.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/exportjarfile.png


* The final step is to add a new entry in the placement.py file with the new algorithm. See figure below:

.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/placementpy1.png

To integrate the new algorithm in the ETSO framework, update the `orchestrator.py file <../SFC-orchestrator/sfc-orchestrator.py>`_ and set the placement_headers['algorithm'] variable to the *dummy* value.
 
.. image:: https://raw.githubusercontent.com/MarouenMechtri/ETSO/ETSO_v2/images/orchestratorpy1.png

