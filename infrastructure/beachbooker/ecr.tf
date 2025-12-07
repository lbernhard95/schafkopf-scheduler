resource "aws_ecr_repository" "beachbooker" {
  name         = "beachbooker-lambda"
  force_delete = true
}

resource "aws_ecr_lifecycle_policy" "beachbooker" {
  repository = aws_ecr_repository.beachbooker.name

  policy = jsonencode(
    {
      "rules" : [
        {
          "rulePriority" : 1,
          "description" : "Keep last 1 untagged images",
          "selection" : {
            "tagStatus" : "untagged",
            "countType" : "imageCountMoreThan",
            "countNumber" : 1
          },
          "action" : {
            "type" : "expire"
          }
        }
      ]
  })
}


data "aws_ecr_image" "beachbooker" {
  repository_name = aws_ecr_repository.beachbooker.name
  image_tag       = "latest"
}
