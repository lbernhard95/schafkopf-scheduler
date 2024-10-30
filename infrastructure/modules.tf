
module "web" {
  source = "./web"
  providers = {
    aws        = aws
    aws.us-east = aws.us-east
  }
}

module "api" {
  source = "./api"
}