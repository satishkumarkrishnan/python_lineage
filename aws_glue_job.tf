#AWS Glue job for a Python script
resource "aws_glue_job" "example" {
  name = "DDSL_Glue_job"
  role_arn = aws_iam_role.gluerole.arn
  #max_capacity = "1.0"
  glue_version = "4.0"
  number_of_workers = "2.0"
  worker_type = "G.1X"
  command {
   # name            = "pythonshell"
    script_location = "s3://${aws_s3_bucket.example1.bucket}/datalineage.py" 
    python_version = "3"
  }
   default_arguments = {    
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.glue_job_log_group.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--enable-metrics"                   = "true"
    "--job-language"                     = "Python 3"
    "--scriptLocation"                   = "s3://${aws_s3_bucket.example1.bucket}/datalineage.py"
    "--extra-jars"                       = "s3://${aws_s3_bucket.example1.bucket}/openlineage-spark_2.12-1.13.1.jar,"
    "--user-jars-first"                  = "true" 
    "--encryption-type"                  = ""
  }
}