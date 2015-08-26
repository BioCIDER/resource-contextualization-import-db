# resource-contextualization—import-db

DB Abstraction Layer

> Python classes to manage different DBs, their connections and functionality. 

## Getting Started

You need a proper python interpreter for your system. Download it from [Python downloads](https://www.python.org/downloads/)

Version tested with this application is 2.7.

Also, you need to download pysolr library to operate with SolR DB.
You can download it from:
[Pysolr downloads](https://pypi.python.org/pypi/pysolr)

Last version tested is 3.3.2.


## Abstraction layer

In order to avoid depending excessively on one specific DB implementation, we have built some classes to isolate it the rest of the code.

### DBFactory

This class should be the entry point for anyone who wants to use our persistence system.

### AbstractManager

Abstract class that should be implemented by all specific DB manager classes. 
One user of this abstraction layer only should care about methods in this class to manage data, without any knowledge about which specific DB manager is underlying.

One of those classes is our SolrManager class into /solr folder.

## Contributing

Please submit all issues and pull requests to the [elixirhub/resource-contextualization-import-db](https://github.com/elixirhub/resource-contextualization-import-db/) repository!


## Support
If you have any problem or suggestion please open an issue [here](https://github.com/elixirhub/resource-contextualization-import-db/issues).


## License 


This software is licensed under the Apache 2 license, quoted below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
