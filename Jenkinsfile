pipeline {
    environment {
        AWS_ACCOUNT_ID = '471112869272'
        AWS_REGION = 'ap-northeast-2'
        ECR_REPO_NAME = 'eks-project'
        registry = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
        registryCredential = 'ECR-Credentials' // Jenkins에 설정된 AWS 자격 증명 ID
        app = ''
        version = "${env.BUILD_NUMBER}"
    }

    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AlpacaMale/project.git'
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    app = docker.build("${registry}:${version}", "--build-arg ENVIRONMENT=${env} .")
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com'
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    docker.withRegistry("https://${registry}", registryCredential) {
                        app.push("${version}")   // 버전 태그로 푸시
                        app.push("latest")       // latest 태그로 푸시
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                script {
                    sh "docker rmi ${registry}:${version}"
                    sh "docker rmi ${registry}:latest"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
