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
variable "port_count" {}

variable "ports" {
  type = "list"
}

resource "openstack_networking_secgroup_v2" "Spark-Cluster-Security-Group" {
  name = "Spark-Cluster-Security-Group"
}

resource "openstack_networking_secgroup_v2" "Default" {
  name = "default"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Jupyter" {
  count             = "${var.port_count}"
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${element(var.ports, count.index)}"
  port_range_max    = "${element(var.ports, count.index)}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Master-UI" {
  count             = "${var.port_count}"
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${element(var.ports, count.index)}"
  port_range_max    = "${element(var.ports, count.index)}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Application-UI" {
  count             = "${var.port_count}"
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${element(var.ports, count.index)}"
  port_range_max    = "${element(var.ports, count.index)}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

output "Spark-Cluster-Security-Group-Id" {
  value = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

output "Default-Security-Group-Id" {
  value = "${openstack_networking_secgroup_v2.Default.id}"
}

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
