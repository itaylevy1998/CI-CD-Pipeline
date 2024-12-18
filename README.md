## CI/CD Pipeline Project 

### Project Overview
 This project implements a fully automated CI/CD pipeline within an AWS environment. The pipeline automates the entire process, from code commits to deployment.

### Architecture
- **AWS VPC:** The environment is hosted within a Virtual Private Cloud (VPC) that includes public and private subnets.
- **GitLab:** Source code management and version control system.
- **Jenkins:** Continuous Integration server responsible for automating the CI/CD workflow.
- **EKS Cluster:** Production environment running the application in a Kubernetes cluster.
- **Slack:** Provides notifications about the pipeline's status.

### Workflow
1) **Code Commit:** Developers push code changes to the GitLab repository.
2) **Webhook Trigger:** GitLab sends a webhook notification to the Jenkins server.
3) **Pipeline Execution:** Jenkins automates the following steps:
    - **Static Analysis:** Perform code quality checks to ensure adherence to coding standards.
    - **Build:** Compile the source code into a deployable artifact.
    - **Test:** Run unit and integration tests to validate functionality.
    - **Publish:** Upload the build artifact to a repository or storage for deployment.
    - **Deploy:** Update the Kubernetes cluster in the EKS environment with the new application version.
    - **Notification:** Send a Slack message with the pipeline status (success or failure).













