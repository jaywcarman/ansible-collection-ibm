# IBM Power Virtual Server in IBM Cloud

This example creates a Power Systems Virtual Server running AIX or IBMi. The
server is configured to allow incoming SSH connections through a publicly
accessible IP address and authenticated using the provided SSH key.

## Power Systems Virtual Server Resources

The following infrastructure resources will be created (Ansible modules in
parentheses):

* SSH Key (ibm_pi_key)
* Network (ibm_pi_network)
* Virtual Server Instance (ibm_pi_instance)

## Running

### Set Configuration Parameters

1. The following `vars.yml` parameters can be set by the user:

* `service:`
  * `pi_cloud_instance_id:` Power Systems Virtual Server service GUID
  * `ibmcloud_api_key:` IAM Cloud IAM API key
  * `region:` PowerVS service region (e.g. `mon`)
  * `zone:` PowerVS service zone (e.g. `mon01`)
* `ssh_key:`
  * `name:` Name of the SSH Key resource created
  * `public:` Local path to SSH public key
  * `private:` Local path to SSH private key (required to connect to VM after
    provisioning)
* `instance:`
  * `name:` Name assigned to Virtual Server Instance
  * `sys_type:` The type of system on which to create the VM (s922/e880/etc.)
  * `image:` VM image name ([retrieve available images])
  * `proc_type:` The type of processor mode in which the VM will run
    (shared/dedicated)
  * `processors:` The number of entitled CPUs to assign to the VM
  * `memory:` The amount of memory (GB) to assign to the VM
* `network:`
  * `name:`
* `storage_volume:`
  * `type:` Type of additional storage volume
  * `name:` Name of additional storage volume
  * `size:` Size of additional storage volume in GB
  * `shareable:` Make additional storage volume shareable (true/false)

### Create

1. To create all resources and test public SSH connection to the VM, run the
   'create' playbook:

    ```
    ansible-playbook create.yml
    ```

### List Available PI VM Images

1. To list available images run the 'list_pi_images' playbook. *note: Images
   are specific to a PI instance, and thus the 'pi_cloud_instance_id' var
   must be set before running this playbook.:

    ```
    ansible-playbook list_pi_images.yml
    ```

[retrieve available images]: #list-available-pi-images
[Ansible search path]: https://docs.ansible.com/ansible/latest/dev_guide/overview_architecture.html#ansible-search-path
