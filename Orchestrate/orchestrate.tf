# Terraform Infrastructure File For Snic Science Cloud (OpenStack)
# Author: Sudarsan Bhargavan

variable "master_count" {}
variable "slaves_count" {}
variable "compute_image_id" {}
variable "compute_flavor_name" {}
variable "compute_key_pair_name" {}
variable "private_network_id" {}
variable "floatingip_pool_name" {}
variable "ip_type" {}
variable "ip_protocol" {}
variable "ssh_port" {}
variable "jupyter_port" {}
variable "spark_master_port" {}
variable "spark_worker_port" {}
variable "spark_master_ui_port" {}
variable "spark_worker_ui_port" {}
variable "spark_app_ui_port" {}
variable "spark_driver_port" {}
variable "cidr_block" {}
variable "slaves_fip_count" {}

resource "openstack_networking_secgroup_v2" "Spark-Cluster-Security-Group" {
  name = "Spark-Cluster-Security-Group"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-SSH" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.ssh_port}"
  port_range_max    = "${var.ssh_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Jupyter" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.jupyter_port}"
  port_range_max    = "${var.jupyter_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Master-Port" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_master_port}"
  port_range_max    = "${var.spark_master_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Worker-Port" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_worker_port}"
  port_range_max    = "${var.spark_worker_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Master-UI" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_master_ui_port}"
  port_range_max    = "${var.spark_master_ui_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Worker-UI" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_worker_ui_port}"
  port_range_max    = "${var.spark_worker_ui_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Application-UI" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_app_ui_port}"
  port_range_max    = "${var.spark_app_ui_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "Rule-Spark-Driver" {
  direction         = "ingress"
  ethertype         = "${var.ip_type}"
  protocol          = "${var.ip_protocol}"
  port_range_min    = "${var.spark_driver_port}"
  port_range_max    = "${var.spark_driver_port}"
  remote_ip_prefix  = "${var.cidr_block}"
  security_group_id = "${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"
}

resource "openstack_blockstorage_volume_v2" "Email-Data-Volume" {
  name = "Email-Data-Volume"
  size = 30
}

resource "openstack_compute_instance_v2" "Spark-Master" {
  count           = "${var.master_count}"
  name            = "Spark-Master"
  image_id        = "${var.compute_image_id}"
  flavor_name     = "${var.compute_flavor_name}"
  key_pair        = "${var.compute_key_pair_name}"
  security_groups = ["${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"]

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

resource "openstack_compute_volume_attach_v2" "Volume-Attach" {
  instance_id = "${openstack_compute_instance_v2.Spark-Master.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.Email-Data-Volume.id}"
}

resource "openstack_compute_instance_v2" "Spark-Slaves" {
  count           = "${var.slaves_count}"
  name            = "${format("Spark-Slave-%d", count.index + 1)}"
  image_id        = "${var.compute_image_id}"
  flavor_name     = "${var.compute_flavor_name}"
  key_pair        = "${var.compute_key_pair_name}"
  security_groups = ["${openstack_networking_secgroup_v2.Spark-Cluster-Security-Group.id}"]

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

resource "openstack_networking_floatingip_v2" "Slaves-FloatingIP-Pool" {
  count = "${var.slaves_fip_count}"
  pool  = "${var.floatingip_pool_name}"
}

resource "openstack_compute_floatingip_associate_v2" "Slaves-FIP" {
  count       = "${var.slaves_fip_count}"
  floating_ip = "${element(openstack_networking_floatingip_v2.Slaves-FloatingIP-Pool.*.address, count.index)}"
  instance_id = "${element(openstack_compute_instance_v2.Spark-Slaves.*.id, count.index)}"
}

# ==================================================
# Ansible Static Inventory Block

data "template_file" "Ansible_Static_Inventory" {
  template = "${file("${path.module}/ansible_hosts.tpl")}"

  depends_on = [
    "openstack_compute_floatingip_associate_v2.Master-FIP",
    "openstack_compute_floatingip_associate_v2.Slaves-FIP",
  ]

  vars {
    spark_master_public_ip  = "${openstack_compute_floatingip_associate_v2.Master-FIP.floating_ip}"
    spark_slave_1_public_ip = "${openstack_compute_floatingip_associate_v2.Slaves-FIP.*.floating_ip[0]}	hostname_suffix=1"
    spark_slave_2_public_ip = "${openstack_compute_floatingip_associate_v2.Slaves-FIP.*.floating_ip[1]}	hostname_suffix=2"
  }
}

resource "null_resource" "Ansible_Static_Inventory" {
  triggers {
    template_rendered = "${join("", data.template_file.Ansible_Static_Inventory.*.rendered)}"
  }

  provisioner "local-exec" {
    command = "echo '${join("", data.template_file.Ansible_Static_Inventory.*.rendered)}' > Spark_Cluster_Hosts"
  }
}
