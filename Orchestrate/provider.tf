# Terraform Provider File For Snic Science Cloud (OpenStack)
# Author: Sudarsan Bhargavan

variable "user_name" {}
variable "user_domain_name" {}
variable "user_password" {}
variable "keystone_url" {}
variable "tenant_id" {}
variable "region_name" {}

provider "openstack" {
  user_name        = "${var.user_name}"
  user_domain_name = "${var.user_domain_name}"
  password         = "${var.user_password}"
  auth_url         = "${var.keystone_url}"
  tenant_id        = "${var.tenant_id}"
  region           = "${var.region_name}"
}
