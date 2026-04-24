output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "auth_service_ecr" {
  value = aws_ecr_repository.auth_service.repository_url
}

output "ticket_service_ecr" {
  value = aws_ecr_repository.ticket_service.repository_url
}