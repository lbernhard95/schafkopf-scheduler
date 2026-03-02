
resource "aws_ecr_repository" "whatsapp_scheduler" {
  name         = "whatsapp_scheduler-lambda"
  force_delete = true
}

resource "aws_ecr_lifecycle_policy" "whatsapp_scheduler" {
  repository = aws_ecr_repository.whatsapp_scheduler.name

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


data "aws_ecr_image" "whatsapp_scheduler" {
  repository_name = aws_ecr_repository.whatsapp_scheduler.name
  image_tag       = "latest"
}
