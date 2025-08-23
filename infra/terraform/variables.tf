variable "project" {
  description = "Project name prefix"
  type        = string
  default     = "fapag-collecte"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.20.0.0/16"
}

variable "azs" {
  description = "Availability zones to use"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]
}

# Database
variable "db_name" {
  type        = string
  default     = "fapag_collecte"
}

variable "db_username" {
  type        = string
  default     = "fapag_user"
}

variable "db_allocated_storage" {
  type        = number
  default     = 20
}

# Instance sizes (adjust later)
variable "ecs_task_cpu" {
  type    = number
  default = 512
}

variable "ecs_task_memory" {
  type    = number
  default = 1024
}

variable "container_image" {
  description = "Container image for the API (temporary: nginx for smoke test)"
  type        = string
  default     = "nginx:alpine"
}

variable "container_port" {
  description = "Container port exposed by the task"
  type        = number
  default     = 80
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 1
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for HTTPS on ALB (leave empty to keep HTTP only)"
  type        = string
  default     = ""
}

variable "enable_waf" {
  description = "Enable WAFv2 WebACL with AWS Managed Rules"
  type        = bool
  default     = false
}

variable "enable_alb_logging" {
  description = "Enable ALB access logging to S3"
  type        = bool
  default     = false
}

variable "alb_logs_bucket_name" {
  description = "S3 bucket name for ALB access logs (required if enable_alb_logging=true)"
  type        = string
  default     = ""
}
