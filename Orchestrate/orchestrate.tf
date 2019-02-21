# Terraform Infrastructure File For Snic Science Cloud (OpenStack)
# Author: Sudarsan Bhargavan

variable "master_count" {}
variable "slaves_count" {}
variable "compute_image_id" {}
variable "compute_flavor_name" {}
variable "compute_key_pair_name" {}

variable "security_group_names" {
  type = "list"
}

variable "private_network_id" {}
variable "floatingip_pool_name" {}

resource "openstack_compute_instance_v2" "Spark-Master" {
  count           = "${var.master_count}"
  name            = "Spark-Master"
  image_id        = "${var.compute_image_id}"
  flavor_name     = "${var.compute_flavor_name}"
  key_pair        = "${var.compute_key_pair_name}"
  security_groups = "${var.security_group_names}"

  network {
    uuid = "${var.private_network_id}"
  }

  block_device {
    uuid                  = "${var.compute_image_id}"
    source_type           = "image"
    destination_type      = "local"
    boot_index            = 0
    delete_on_termination = true
  }
}

resource "openstack_networking_floatingip_v2" "Master-FloatingIP-Pool" {
  pool = "${var.floatingip_pool_name}"
}

resource "openstack_compute_floatingip_associate_v2" "Master-FIP" {
  floating_ip = "${openstack_networking_floatingip_v2.Master-FloatingIP-Pool.address}"
  instance_id = "${openstack_compute_instance_v2.Spark-Master.id}"
}

resource "openstack_compute_instance_v2" "Spark-Slaves" {
  count           = "${var.slaves_count}"
  name            = "${format("Spark-Slave-%d", count.index+1)}"
  image_id        = "${var.compute_image_id}"
  flavor_name     = "${var.compute_flavor_name}"
  key_pair        = "${var.compute_key_pair_name}"
  security_groups = "${var.security_group_names}"

  network {
    uuid = "${var.private_network_id}"
  }

  block_device {
    uuid                  = "${var.compute_image_id}"
    source_type           = "image"
    destination_type      = "local"
    boot_index            = 0
    delete_on_termination = true
  }
}
