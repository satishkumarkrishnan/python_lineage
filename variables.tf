variable "region" {
  description = "AWS region"
  default     = "ap-northeast-1"
}

variable "name" {
  description = "The name of the Glue catalogue database"
  type        = string
  default     = "tokyo_glue_catalogue"
  }

variable "description" {
  description = "DB description"
  type        = string
  default     = "Demo DB"
}

variable "catalogue_id" {
  description = "ID of the Glue catalogue to create the database"
  type        = string
  default     = ""
}

variable "location_uri" {
  description = "The location of the db"
  type        = string  
  default     = "null" 
}

variable "parameters" {
  description = "A map of key-value pairs that define parameters and properties of the database"
  type        = map(string)
  default     = {}
}

variable "target_database" {
  description = "Configuration block for a target db"
  default     = []
  type = list(object({
    catalogue_id = string,
    database_name = string
  }))
}

variable "database_name" {
  description = "Glue db for results updation"
  type        = string
  default     = "null" 
}

variable "glue_crawler_description" {
  description = "Description of the crawler"
  type        = string
  default     = "Tokyo Glue Crawler"
}

variable "role" {
  description = "IAM role for the crawler"
  type        = string   
  default     = "null" 
}
variable "ami" {
  description = "The AMI to run in the cluster"
  type        = string
  default     = "ami-0b657832102c1e96b"  
}

variable "instance_type" {
  description = "The type of EC2 Instances to run (e.g. t2.micro)"
  type        = string
  default     = "t2.micro"
  
  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.instance_type)
    error_message = "Only free tier is allowed: t2.micro | t3.micro."
  }
}
variable "desired_capacity" {
  description = "The desired number of EC2 Instances in the ASG"
  type        = number
  default     = 2
}
variable "min_size" {
  description = "The minimum number of EC2 Instances in the ASG"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "The maximum number of EC2 Instances in the ASG"
  type        = number
  default     = 2
}

variable "enable_autoscaling" {
  description = "If set to true, enable auto scaling"
  type        = bool
  default     = true
}