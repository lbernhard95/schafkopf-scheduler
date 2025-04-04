resource "aws_ecr_repository" "api" {
  name = "schafkopf-api-lambda"
}

resource "aws_ecr_lifecycle_policy" "api" {
  repository = aws_ecr_repository.api.name

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


data "aws_ecr_image" "api" {
  repository_name = aws_ecr_repository.api.name
  image_tag       = "latest"
}
