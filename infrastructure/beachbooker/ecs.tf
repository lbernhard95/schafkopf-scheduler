resource "aws_ecs_cluster" "beachbooker" {
  name = "beachbooker"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "beachbooker-ecs-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_assume_role_policy.json
}

data "aws_iam_policy_document" "ecs_task_execution_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy" "beachbooker" {
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogGroup"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogStream"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "logs:PutLogEvents"
        Resource = "*"
    }]
  })
}
resource "aws_iam_role_policy_attachment" "beachbooker" {
  policy_arn = aws_iam_policy.beachbooker.arn
  role       = aws_iam_role.ecs_task_execution_role.name
}

resource "aws_ecs_task_definition" "beachbooker" {
  family                   = "beachbooker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "beachbooker"
    image     = "${aws_ecr_repository.beachbooker.repository_url}:latest"
    essential = true
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.beachbooker_logs.name
        awslogs-region        = "eu-central-1"
        awslogs-stream-prefix = "ecs"
      }
    }
    environment = [
      { name = "LOG_GROUP_NAME", value = aws_cloudwatch_log_group.beachbooker_logs.name },
      { name = "ZHS_USERNAME", value = jsondecode(data.aws_secretsmanager_secret_version.zhs_user_secret.secret_string)["ZHS_USERNAME"] },
      { name = "ZHS_PASSWORD", value = jsondecode(data.aws_secretsmanager_secret_version.zhs_user_secret.secret_string)["ZHS_PASSWORD"] },
      { name = "GMAIL_SENDER_ADDRESS", value = var.gmail_sender_email },
      { name = "GMAIL_SENDER_PASSWORD", value = var.gmail_sender_password },
      { name = "RUNNING_ON_AWS", value = "true" },
    ]
  }])
}

resource "aws_security_group" "ecs_security_group" {
  vpc_id = data.aws_vpc.default.id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_cloudwatch_event_target" "ecs_task" {
  rule     = aws_cloudwatch_event_rule.beachbooker.name
  arn      = aws_ecs_cluster.beachbooker.arn
  role_arn = aws_iam_role.ecs_task_execution_role.arn
  ecs_target {
    launch_type         = "FARGATE"
    task_definition_arn = aws_ecs_task_definition.beachbooker.arn
    network_configuration {
      subnets          = data.aws_subnets.default.ids
      security_groups  = [aws_security_group.ecs_security_group.id]
      assign_public_ip = true
    }
  }
}

resource "aws_iam_role_policy" "allow_events_to_run_tasks" {
  name = "AllowEventsToRunTasks"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = data.aws_iam_policy_document.events_invoke_ecs_task.json
}

data "aws_iam_policy_document" "events_invoke_ecs_task" {
  statement {
    effect = "Allow"

    actions = [
      "ecs:RunTask",
      "iam:PassRole"
    ]

    resources = [
      aws_ecs_task_definition.beachbooker.arn
    ]
  }
}
