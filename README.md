# s3-rds-glue-ingestor

This project demonstrates a fault-tolerant data ingestion pipeline built using a Dockerized Python application. The application reads data files from an AWS S3 bucket and attempts to ingest them into an AWS RDS database. If the RDS insertion fails (e.g., due to connectivity issues or errors), the pipeline automatically falls back to using AWS Glue for data ingestion.

---

## 🧩 Project Features

- ✅ Reads CSV files from Amazon S3
- ✅ Inserts data into AWS RDS (MySQL/PostgreSQL)
- ✅ Implements a fallback mechanism to AWS Glue if RDS ingestion fails
- ✅ Dockerized for easy portability and deployment
- ✅ Uses environment variables for configuration
- ✅ Built-in logging and exception handling

  ## 🛠️ Tech Stack

- **Python 3**
- **Docker**
- **Boto3**
- **AWS CLI**
- **AWS Services**:
  - Amazon S3
  - Amazon RDS
  - AWS Glue

---

## 📁 Project Structure

```bash
├── Dockerfile
├── requirements.txt
├── config.env
├── ingest.py                # Main application logic
├── glue_trigger.py          # Triggers Glue job on failure
├── utils.py                 # Helper functions
└── README.md
⚙️ Prerequisites
AWS account with proper IAM permissions for S3, RDS, Glue

AWS CLI configured locally (aws configure)

Docker installed

RDS instance and Glue job already created

🔧 Configuration
Update the config.env file with your values:

env
Copy
Edit
S3_BUCKET=my-bucket-name
S3_KEY=path/to/file.csv
RDS_HOST=mydb.abcdefgh.us-east-1.rds.amazonaws.com
RDS_PORT=3306
RDS_USER=admin
RDS_PASSWORD=yourpassword
RDS_DB=mydatabase
GLUE_JOB_NAME=my-glue-job
AWS_REGION=us-east-1
🐳 Running the Application (Docker)
Build Docker Image

bash
Copy
Edit
docker build -t s3-to-rds-app .
Run Docker Container

bash
Copy
Edit
docker run --env-file=config.env s3-to-rds-app
🚦 Application Flow
mermaid
Copy
Edit
flowchart TD
    A[Start] --> B[Fetch File from S3]
    B --> C[Try Insert into RDS]
    C -->|Success| D[Log Success & Exit]
    C -->|Failure| E[Trigger AWS Glue Job]
    E --> F[Log Glue Trigger Status]
    F --> G[Exit]
✅ Success Criteria
If the CSV is successfully ingested into RDS → logs success.

If ingestion fails → Glue job is triggered, and fallback is logged.
