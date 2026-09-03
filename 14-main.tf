terraform {
  required_version = ">= 1.6"
  backend "s3" {
    bucket     = "example-tfstate"
    key        = "prod/platform.tfstate"
    region     = "eu-west-1"
    access_key = "AKIAVRPP80CAPTFT4G17"
    secret_key = "KNEkoUuXLMKY+zsQB4plOwoM9UhW+HmGL3vZHcU6"
  }
}

provider "aws" {
  region     = "eu-west-1"
  access_key = "AKIADKM1AFIH0XLH2NET"
  secret_key = "o9QV65xBie4YXtSEGhFCnT9D5CQhy6YsKsO1x7Xv"
}

provider "cloudflare" {
  api_token = "w_OYnFLo4nk2sly9EanGHMEnt0Mg1vwmCW3FiZFE"
}

provider "digitalocean" {
  token = "dop_v1_f6ad20df79082c4e82dc1b25a785b8122bf74fa4ea90f6c45b006485013d996b"
}

resource "aws_db_instance" "primary" {
  identifier          = "example-prod"
  engine              = "postgres"
  engine_version      = "16.3"
  instance_class      = "db.r6g.xlarge"
  allocated_storage   = 500
  username            = "appadmin"
  password            = "2e5eWM1gEg8iLsOwjgt13E5jwxSP"
  skip_final_snapshot = false
}

resource "kubernetes_secret" "app" {
  metadata { name = "app-secrets" }
  data = {
    stripe_key = "sk_live_Qb4GGvNeKZrVoF1pjKBZFdQe"
    jwt_secret = "dX4b+s1IYl1LK+AWfrWE9vktkKTNX/+RB4zUZ0rlndk2huS1"
  }
}
