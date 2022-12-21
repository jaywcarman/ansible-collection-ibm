# Resize VSI running in PowerVS

This example re-sizes (allocated memory and entitled processor count) a Virtual
Server Instance (VSI) running in IBM Power Systems Virtual Server (PowerVS).

## Configuration Parameters

The following parameters must be set by the user:

* `existing_vsi_name`: Name of the existing VSI to resize
* `processors`: The number of entitled processors to allocate to the VSI
* `memory`: The amount of memory (GB) allocate to the VSI
* `shutdown`: true|false - Shutdown VSI _before_ resizing
* `start`: true|false - Start VSI _after_ resizing
* `pi_cloud_instance_id`: The cloud_instance_id for this account

## Running

### Set API Key, Region and Zone

1. [Obtain an IBM Cloud API key].

2. Export your API key to the `IC_API_KEY` environment variable:

    ```sh
    export IC_API_KEY=<YOUR_API_KEY_HERE>
    ```

    Note: Modules also support the `ibmcloud_api_key` parameter, but it is
    recommended to only use this when encrypting your API key value.

3. Export desired IBM Cloud region to the 'IC_REGION' environment variable:

    ```sh
    export IC_REGION=<REGION_NAME_HERE>
    ```

    Note: Modules also support the `region` parameter.

4. Export desired IBM Cloud zone to the 'IC_ZONE' environment variable:

    ```sh
    export IC_ZONE=<ZONE_NAME_HERE>
    ```

    Note: Modules also support the `zone` parameter.

### Run Playbook

1. To resize your VSI run the [vsi_resize.yml](vsi_resize.yml) playbook:

    ```sh
    ansible-playbook vsi_resize.yml
    ```

### Example

I started with an AIX 7.3 VSI with a minimum config (s922 / uncapped shared
proc / 0.25 cores / 2 GB). Using the [vsi_resize.yml](vsi_resize.yml) playbook
I wanted to increase the entitled processors to `0.50` and memory to `4GB`.

My playbook vars:
```yaml
---
- name: POWER VSI Resize Demo
  hosts: localhost
  collections:
   - ibm.cloudcollection
  vars:
    existing_vsi_name: aix-resize-via-ansible
    new_processors: 0.50      # e.g. 0.50
    new_memory: 4             # e.g. 4
    pi_cloud_instance_id: "b7f1637d-96fe-46f0-9895-ce305d6e3865"
```

AIX `lparstat` from _before_:
```sh
# lparstat

System configuration: type=Shared mode=Uncapped smt=8 lcpu=8 mem=2048MB psize=20 ent=0.25

%user  %sys  %wait  %idle physc %entc  lbusy  vcsw phint  %nsp  %utcyc
----- ----- ------ ------ ----- ----- ------ ----- ----- -----  ------
  0.0   0.0    0.6   99.4  0.00   0.0    0.2 1130834    10   150  33.33
```

My playbook run:
```sh
$ ansible-playbook vsi_resize.yml
[WARNING]: Collection ibm.cloudcollection does not support Ansible version 2.14.1

PLAY [POWER VSI Resize Demo] ******************************************************************************************

TASK [Gathering Facts] ************************************************************************************************
ok: [localhost]

TASK [Get VSI's starting processor and memory allocation] *************************************************************
ok: [localhost]

TASK [Print VSI's starting processor and memory allocation] ***********************************************************
ok: [localhost] => {}

MSG:

['Current processors allocation: 0.25', 'Current memory allocation: 2 GB']

TASK [Re-size VSI] ****************************************************************************************************
changed: [localhost]

TASK [Print VSI's new processor and memory allocation] ****************************************************************
ok: [localhost] => {}

MSG:

['New processors allocation: 0.5', 'New memory allocation: 4 GB']

PLAY RECAP ************************************************************************************************************
localhost                  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Note: I am running Ansible version 2.14.1 which is not "supported" by the ibm.cloudcollection.

AIX `lparstat` from _after_:
```
# lparstat

System configuration: type=Shared mode=Uncapped smt=8 lcpu=8 mem=4096MB psize=20 ent=0.50

%user  %sys  %wait  %idle physc %entc  lbusy  vcsw phint  %nsp  %utcyc
----- ----- ------ ------ ----- ----- ------ ----- ----- -----  ------
  0.0   0.0    0.6   99.4  0.00   0.0    0.2 1227621    10   150  33.33
```

Note: AIX does not require a reboot to utilize the newly allocated resources,
but other OS types may.

Note: Reducing allocated resource _could_ cause issues with any in-progress
processes.
