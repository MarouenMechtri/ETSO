#  Copyright 2016-2017 Marouane Mechteri
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Created on Dec 10, 2017
# authors: Marouane Mechteri
# contacts: {mechteri.marouane}@gmail.com
# license: Apache License, Version 2.0

#!/bin/sh
apt-get update  # To get the latest package lists
apt-get -y upgrade

apt-get -y install python-pip git openjdk-8-jre -y

pip install -r requirements.txt


# Install the extended tosca parser:
cd SFC-orchestrator/Tosca-parser/
python setup.py install
cd toscaparser
cp sfconf/translator.conf /usr/local/lib/python2.7/dist-packages/toscaparser/sfconf/
cd ../../

# Install heat-translator:
cd NCT-translator/plugins/hot-translator/
python setup.py install
cd ../../../../
