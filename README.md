# STELLA Server

[![Python application](https://github.com/stella-project/stella-server/actions/workflows/push.yml/badge.svg?branch=master)](https://github.com/stella-project/stella-server/actions/workflows/push.yml)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
![Uptime Robot status](https://img.shields.io/uptimerobot/status/m787965418-9316cd5dcf2729ae45301889)
![Uptime Robot ratio (7 days)](https://img.shields.io/uptimerobot/ratio/7/m787965418-9316cd5dcf2729ae45301889)



The `stella-server` provides the following services:

:busts_in_silhouette: User administration  
:bar_chart: Dashboard  
:robot: Automated generation of the STELLA app &rarr; `docker-compose.yml`  
:floppy_disk: Data storage (user feedback) for data analysis, training, etc.

## Setup

1. Build app with Docker:  `docker-compose up -d`
2. Add toy data with the help of `util/simulate.py`

**A setup guide for the entire infrastructure can be found [here](./doc/README.md).**

## Citation

We provide citation information via the [CITATION file](./CITATION.cff). If you use `stella-server` in your work, please cite our repository as follows:

> Schaer P, Schaible J, Garcia Castro LJ, Breuer T, Tavakolpoursaleh N, Wolff B. STELLA Server. Available at https://github.com/stella-project/stella-server/

We recommend you include the retrieval date.

## License

`stella-server` is licensed under the [GNU GPLv3 license](https://github.com/stella-project/stella-server/blob/master/LICENSE). If you modify `stella-server` in any way, please link back to this repository.

