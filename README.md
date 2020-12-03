# STELLA Server

The `stella-server` provides the following services:

:busts_in_silhouette: User administration (administration of admins, participants and sites)  
:bar_chart: Dashboard service  
:robot: Automated generation of the STELLA app &rarr; `docker-compose.yml`  
:floppy_disk: Data storage (user feedback) for data analysis, training, etc.

## Setup

1. Build app with Docker:  `docker-compose up -d`
2. Add toy data with the help of `util/simulate.py`

## Citation

We provide citation information via the [CITATION file](./CITATION.cff). If you use `stella-server` in your work, please cite our repository as follows:

> Schaer P, Schaible J, Garcia Castro LJ, Breuer T, Tavakolpoursaleh N, Wolff B. STELLA Search. Available at https://github.com/stella-project/stella-server/

We recommend you include the retrieval date.

## License

`stella-server` is licensed under the [GNU GPLv3 license](https://github.com/stella-project/stella-server/blob/master/LICENSE). If you modify `stella-server` in any way, please link back to this repository.

