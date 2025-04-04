resource "aws_ecr_repository" "schafkopf_scheduler" {
  name = "schafkopf-scheduler-lambda"
}

resource "aws_ecr_lifecycle_policy" "schafkopf_scheduler" {
  repository = aws_ecr_repository.schafkopf_scheduler.name

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


data "aws_ecr_image" "schafkopf_scheduler" {
  repository_name = aws_ecr_repository.schafkopf_scheduler.name
  image_tag       = "latest"
}
