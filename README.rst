# ETSO-End-To-End-SFC-Orchestration-Framework

In this installation guide, we cover the step-by-step process of installing the ETSO famework on Ubuntu 16.04. We need to have an Opendayligh node that manages the service function chains.
Next we will show how to install on Ubuntu 16.04 an Opendaylight who will play the role of an SFC controller. Then we will provide a description of the steps followed to install the ETSO and to create an SFC with OpenStack and OpenDaylight.


===============================

**Authors:**

Copyright (C) `Marouane Mechteri <https://www.linkedin.com/in/mechtri>`_


================================

.. contents::



Installation of OpenDaylight and SFC features
=============================================


* Installation of openjdk 8 and unzip::


    sudo apt-get update
    sudo apt-get install openjdk-8-jre
    sudo apt-get install unzip

* Edit /etc/environment with JAVA_HOME variable::

    sudo vi /etc/environment

    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/


* Download the OpenDaylight Boron release::

    wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.5.1-Boron-SR1/distribution-karaf-0.5.1-Boron-SR1.zip
    unzip distribution-karaf-0.5.1-Boron-SR1.zip



* Load JAVA_HOME variable::

    logout and login again


* Installation of SFC features::

    cd distribution-karaf-0.5.1-Boron-SR1/
    ./bin/karaf
    feature:install  odl-sfc-model odl-sfc-provider odl-sfc-provider-rest odl-sfc-netconf odl-sfc-ovs  odl-sfc-scf-openflow odl-sfc-openflow-renderer  odl-sfclisp odl-sfc-sb-rest odl-sfc-ui


Configuration of the ETSO framework
===================================



Create an SFC
=============
