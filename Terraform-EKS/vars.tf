variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-north-1"
}


variable "vpc_id" {
  description = "Existing VPC ID for the EKS cluster"
  type        = string
  default     = "vpc-0320f59abb2394166"
}


variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "weather-app-cluster"
}

variable "k8s-version" {
    description = "Version for the k8s cluster"
    type = string
    default = "1.31"
}

variable "instance_type" {
  description = "Instance type for the EKS nodes"
  type        = string
  default     = "t3.small"
}
