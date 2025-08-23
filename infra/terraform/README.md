# AWS Terraform Scaffold (FAPAG Collecte)

This is a minimal starting point. It creates a VPC with public/private subnets and leaves placeholders for ALB, ECS Fargate, and RDS.

## Prerequisites
- Terraform >= 1.5
- AWS credentials configured (AWS SSO or access keys)

## Files
- `versions.tf`: required versions
- `providers.tf`: AWS provider
- `variables.tf`: common variables (region, CIDR, DB, ECS sizing)
- `main.tf`: VPC module and placeholders for ALB/ECS/RDS

## Usage
```bash
cd infra/terraform
terraform init
terraform plan -out plan.tfplan 
# optionally override defaults
# terraform plan -var aws_region=eu-west-3 -var project=fapag-collecte -out plan.tfplan
terraform apply plan.tfplan
```

## Next steps
1. Add ALB module (public) and security groups.
2. Add ECS Fargate cluster + service for Django API, connect to ALB target group.
3. Add RDS PostgreSQL in private subnets (no public access). Secrets in Secrets Manager.
4. Add WAFv2 WebACL and associate to ALB.
5. Configure ACM certificate for your domain and HTTPS listener on ALB.
6. Export outputs for CI/CD to feed environment variables (DB host/secret ARNs, ALB URL).

## Mapping to Django env
- DB host/port/user/password -> `POSTGRES_*`
- ALB/Domain -> `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
- Secrets Manager -> populate `.env` at deploy time or load at runtime

## Notes
- Default CIDR/subnets are placeholders; adjust for your org.
- Consider remote state (S3 + DynamoDB) before team use.
