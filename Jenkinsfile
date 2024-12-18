pipeline {
    agent {
        docker {
            alwaysPull true
            image "images/agent:1.0"
            args "--privileged -u 0:0 -v /var/run/docker.sock:/var/run/docker.sock"
        }
    }
    environment {
        FLASK_IMAGE_NAME = "flask"
        INNER_VERSION = "${env.BRANCH_NAME}-${env.BUILD_ID}-${env.GIT_COMMIT}"
        AWS_REGION = "eu-north-1"
        AWS_ACCOUNT_ID = "831926627653"
        PRODUCTION_CLUSTER = 'eks-cluster'
    }

    stages {
        stage('Static Analysis') {
            steps {
               script {
                    def scannerHome = tool 'sonarQube scanner'
                    withSonarQubeEnv('sonarqube') {
                        sh "sonar-scanner -Dsonar.projectKey=my-weather-app -Dsonar.sources=."
                    }

                    timeout(time: 1, unit: 'MINUTES') { 
                        def qg = waitForQualityGate() 
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate failure!: ${qg.status}"
                        }
                    }
               }     
            }            
        }
        stage('Build') {
            steps {
                sh "docker compose build"
            }
        }
        stage('Test') {
            steps {
                sh "docker compose up -d"
                sh "pytest ./Tests/testSiteReachability.py"
                sh "docker compose down"
            }
        }
        stage('Publish') {
            steps {
                withCredentials([aws(credentialsId: 'ItayIAM')]) {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    docker tag flask:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/images/weatherapp:${INNER_VERSION}
                    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/images/weatherapp:${INNER_VERSION}
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                sh "echo 'about to deploy to production..'"
                withCredentials([aws(credentialsId: 'ItayIAM')]) {
                    sh """
                    aws eks update-kubeconfig --name $PRODUCTION_CLUSTER --region $AWS_REGION
                    kubectl apply -f ./Production/weatherSecret.yaml
                    kubectl apply -f ./Production/weatherDeployment.yaml
                    kubectl apply -f ./Production/weatherService.yaml
                    """
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker system prune -af"
        }
        success {
            slackSend (
                channel: 'succeeded-builds',
                color: 'good',
                message: "Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} succeeded."
            )
        }
        failure {
            slackSend (
                channel: 'devops-alerts',
                color: 'danger',
                message: "Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} failed."
            )
        }
    }
}
