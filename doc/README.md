## 0. Overview

This guide is intended for setting up an instance of the `stella-app` and the `stella-server` on a **single** machine. Both applications have to be in the same Docker network. Only then, the `stella-app`'s HTTP requests can reach the REST-API of the `stella-server`. These instructions will guide you through the following steps:

1. Clone the repositories (`stella-server`, `stella-app`)
2. Download the datasets (extracting and placing them in the correct directory)
3. Configure the `stella-server` and the `stella-app`
4. Build both Docker applications
5. Sanity checks

By the end, you should have both applications running and can simulate interactions with the stella-app, which in turn sends the feedback to the stella-server. By logging into the stella-server, you should be able to see plots in the dashboard and JSON-formatted downloads of the feedback data should be possible.

#### Prerequisites:

:warning: Make sure **`docker`**, **`docker-compose`** and the **`docker-sdk`** [1] are installed and executable! :warning:

[1] The **`docker-sdk`** is actually only required for developing micro-services with experimental systems.

**Start with fresh copies of the repositories and make sure previous builds of the Docker images are removed.** It may not be enough to stop the containers. In some cases, previous image builds (which are not up-to-date) might be re-used.

### 1. Clone the repositories

Clone the repository of the stella-server:

```
git clone https://github.com/stella-project/stella-server
``` 

Clone the repository of the stella-app:

```
git clone https://github.com/stella-project/stella-app
``` 

### 2. Download the datasets 

Download the datasets that are provided by LIVIVO and GESIS from the publicly shared [Sciebo folder](https://th-koeln.sciebo.de/s/OBm0NLEwz1RYl9N). More specifically, you should download the two folders `gesis-search/` and `livivo/` and place the uncompressed folders in the [`data/`](https://github.com/stella-project/stella-app/tree/master/data) directory of the stella-app.

### 3. Configure the `stella-server` and the `stella-app`

Both applications have a `config.py` file. Leaving the configurations untouched after the repositories have been cloned is fine - there is actually no need to change anything here. Those who want to directly dive in, can skip the following lines and can continue with the Docker builds.

For the curious minds, there are seperate pages for the `stella-server`'s [`config.py`](https://github.com/stella-project/stella-documentation/wiki/stella-server-config) and the `stella-app`'s [`config.py`](https://github.com/stella-project/stella-documentation/wiki/stella-app-config). There you will find detailed descriptions of each configuration. For now, it is interesting to have a look at the following fields of `stella-app`'s [`config.py`](https://github.com/stella-project/stella-documentation/wiki/stella-app-config).

1. Check if `conf['app']['DEBUG'] = False`.
2. Check if `conf['app']['BULK_INDEX'] = True`. When starting the `stella-app` all experimental will start to index the data in parallel. There is no need to trigger any indexing process "manually".
3. Check if `conf["app"]["STELLA_SERVER_API"] = "http://nginx/stella/api/v1"`. This is the address of the `stella-server` in the Docker network. Only if both applications are in the same Docker network, they can communicate.
4. Check the credentials that are used by the `stella-app`:

```
conf["app"]["STELLA_SERVER_USER"] = "gesis@stella.org"
conf["app"]["STELLA_SERVER_PASS"] = "pass"
conf["app"]["STELLA_SERVER_USERNAME"] = "GESIS"
```

Per default, GESIS is set as the user of the `stella-app`, but you can change them to LIVIVO's with the help of the credentials given below.

### 4. Build both Docker applications

**The `stella-server` has to be built first!** Its default network will be used as our Docker network. Build the `stella-server` with:
```
cd stella-server/
docker-compose up -d
```

Afterwards, the `stella-app` can be built. In the repository you will find two `.yml`-files. As part of this guide, you have to use the [`docker-compose.yml` file](https://github.com/stella-project/stella-app/blob/master/docker-compose.yml). It will add the `stella-app` to the Docker network of the `stella-server`. You can ignore the `local.yml` - this one is intended for a setup independent of the `stella-server`. Build the `stella-app` with:

```
cd stella-app/
docker-compose up -d
```

If you feel thirsty, this would be the right moment to get a beer :beer:, a cup of coffee :coffee:, tea :tea:, or any other beverage of your choice. It takes a while to build all the Docker images (all dependencies have to be retrieved from the web) and once the images are running in containers, the indexing will take some time.

Please note that at the current stage, the `stella-app` has already too many experimental systems, so not all systems can start the indexing in parallel when starting the app on my laptop (16GB RAM, i7 4Cores@1.9GHz). Even though the `stella-app` forces all systems to build the index at once, some experimental systems will probably remain without an index, after the app has been started on lower-end devices. A current workaround for this problem is to trigger the indexing for specific experimental systems that do not have an index. This can either be done by the corresponding REST-endpoint (`/stella/api/v1/index/<string:container_name>`) or by visiting the dashboard of the `stella-app` and using the index button.

### 5. Sanity checks

Once everything has been set up. We can check a few things first.

#### 1st sanity check: visiting the dashboard

If you did not change anything in the configurations, the `stella-server` should be visitable at [http://0.0.0.0:80](http://0.0.0.0:80). Log in with one of the provided credentials below. You should able to see a list with pre-registered system at [http://0.0.0.0:80/systems](http://0.0.0.0:80/systems) and can visit an "empty" dashboard at [http://0.0.0.0:80/dashboard](http://0.0.0.0:80/dashboard). In the following, we will fill up the database of the `stella-server` with some feedback data.

#### 2nd sanity check: Simulating feedback data and posting it via the REST endpoints of the `stella-server`

In this step, we will simulate interactions and use the [REST endpoints](https://github.com/stella-project/stella-documentation/wiki/REST-API:-STELLA-app---STELLA-server) that are actually used by the stella-app later on. It can be seen as a pre-assessment, if the `stella-server` behaves as intended. Use the [`simulate.py`](https://github.com/stella-project/stella-server/blob/master/util/simulate.py) script and make sure, the address of the stella-server is set correctly in the script. Once executed, you can revisit the dashboard and should be provided with some visualizations. Likewise, JSON-formatted feedback data should be exportable from the systems' overview.

#### 3rd sanity check: Simulating feedback data and posting it via the REST endpoints of the `stella-app`

In the previous step, we were using the REST endpoints that are intended to be used by the `stella-app`. In this step, we will also simulate data and send it to the `stella-app`, which in turn, will send it to the `stella-server`. Use the [`simulate.py`](https://github.com/stella-project/stella-app/blob/master/util/simulate.py) script in the repository of the `stella-app` (make sure the address of the `stella-app` is correct). Revisit the `stella-server` and have a look at the dashboard.

---

## Pre-registered users of the `stella-server` 

##### Participants

| username | email | password |
| --- | --- | --- |
| participant_a | participant_a@stella.org | pass |
| participant_b | participant_b@stella.org | pass |

##### Sites

| username | email | password |
| --- | --- | --- |
| GESIS | gesis@stella.org | pass |
| LIVIVO | livivo@stella.org | pass |


##### Administrators

| username | email | password |
| --- | --- | --- |
| stella-admin | admin@stella.org | pass |

