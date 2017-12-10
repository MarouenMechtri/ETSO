#### 
ETSO-End-To-End-SFC-Orchestration-Framework
####

In this installation guide, we cover the step-by-step process of installing the ETSO famework on Ubuntu 16.04. We need to have an Opendayligh node that manages the service function chains.
Next we will show how to install on Ubuntu 16.04 an Opendaylight who will play the role of an SFC controller. Then we will provide a description of the steps followed to install the ETSO and to create an SFC on OpenStack and OpenDaylight.


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


Installation and Configuration of the ETSO framework
====================================================

* To build the ETSO framework you need to install the following additional libraries and tools::

   sudo apt-get update 
   sudo apt-get -y upgrade
   sudo apt-get -y install python-setuptools python-dateutil python-pip git openjdk-8-jre python-packaging


* Installation of python clients of OpenStack services::

    sudo apt-get -y install python-openstackclient python-ceilometerclient python-heatclient 

* Clone this git repository in your ETSO VM::

    git clone https://github.com/MarouenMechtri/ETSO.git -b ETSO_v2

* Adding trusted root certificates to the ETSO VM::

    
    # Copy your CA to dir /usr/local/share/ca-certificates/:
    sudo cp openstack_https.crt /usr/local/share/ca-certificates/openstack_https.crt

    # Update the CA store: 
    sudo update-ca-certificates

* Install ETSO services::

   cd ETSO 
   sudo ./install.sh

* Update ODL plugin with the OpenDaylight address, port, username and password::

   vi SFC-manager/plugins/config.json

   {
   "ODL" : "192.168.111.36",
   "ODL_PORT" : 8181,
   "ODL_USERNAME" : "admin",
   "ODL_PASSWORD" : "admin"
   }


* Update credentials.py file with credentials of the OpenStack selected to host the requested SFC, VMs, and stacks::

   vi SFC-orchestrator/credentials.py

   USERNAME="username"
   PASSWORD="password"
   TENANT_NAME="tenant_name"
   TENANT_ID="tenant_uuid"
   ENDPOINT="https://OPENSTACK_ADDRESS:5000/v2.0"
   SERVICE="compute"
   REGION="RegionOne"
   VERSION=2
   HEAT_URL="https://OPENSTACK_ADDRESS:8004/v1/tenant_id"
   OS_CACERT="/etc/ssl/certs/openstack_https.pem" 


Create an SFC
=============

Before creating your first SFC, you need to start the ETSO services:

* Starting the ETSO services::
    ./start.py
   

