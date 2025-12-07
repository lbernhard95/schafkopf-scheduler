resource "aws_ecr_repository" "ebg_scanner" {
  name = "ebg_scanner-lambda"
}

resource "aws_ecr_lifecycle_policy" "ebg_scanner" {
  repository = aws_ecr_repository.ebg_scanner.name

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


data "aws_ecr_image" "ebg_scanner" {
  repository_name = aws_ecr_repository.ebg_scanner.name
  image_tag       = "latest"
}
