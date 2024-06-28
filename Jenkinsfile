pipeline {
    agent any
    
    environment {
        AWS_ECR_REPO = '471112869272.dkr.ecr.ap-northeast-2.amazonaws.com/backend'
        GIT_CREDENTIALS_ID = 'Jenkins_backend_credential'
        ECR_REGION = 'ap-northeast-2'
        IMAGE_TAG = "${env.BUILD_NUMBER}" // 빌드 번호를 태그로 사용
        MANIFEST_REPO = 'github.com/Mozo119/Jenkins_backend_manifast.git'
        MANIFEST_REPO_CREDENTIALS_ID = 'Jenkins_backend_manifast_credential'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main',
                        credentialsId: "${GIT_CREDENTIALS_ID}",
                        url: 'https://github.com/Mozo119/Jenkins_backend.git'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // AWS ECR 로그인
                    sh '''
                    aws ecr get-login-password --region ${ECR_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_REPO}
                    '''
                    
                    // Docker 이미지 빌드
                    sh 'docker build -t backend:${IMAGE_TAG} .'
                    
                    // Docker 이미지 태그
                    sh 'docker tag backend:${IMAGE_TAG} ${AWS_ECR_REPO}:${IMAGE_TAG}'
                    sh 'docker tag backend:${IMAGE_TAG} ${AWS_ECR_REPO}:latest'
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                script {
                    // Docker 이미지 푸시
                    sh 'docker push ${AWS_ECR_REPO}:${IMAGE_TAG}'
                    sh 'docker push ${AWS_ECR_REPO}:latest'
                }
            }
        }
        
        stage('Update Manifest Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${MANIFEST_REPO_CREDENTIALS_ID}", usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        // 매니페스트 레포지토리 업데이트
                        sh '''
                        rm -rf Jenkins_backend_manifast
                        git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFEST_REPO}
                        cd Jenkins_backend_manifast
                        sed -i 's|{{AWS_ECR_REPO}}|'${AWS_ECR_REPO}'|g' deployment.yaml
                        sed -i 's|{{IMAGE_TAG}}|'${IMAGE_TAG}'|g' deployment.yaml
                        git config --global user.email "rlaalstjr0502@gmail.com"
                        git config --global user.name "Mozo119"
                        git add deployment.yaml
                        git commit -m "Update image to ${IMAGE_TAG}" || echo "Nothing to commit"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFEST_REPO}
                        '''
                    }
                }
            }
        }
        
        stage('Clean Up Old Docker Images') {
            steps {
                script {
                    // Docker 이미지를 정리
                    sh '''
                    docker images --filter "reference=${AWS_ECR_REPO}" --format "{{.ID}} {{.Tag}}" | while read -r id tag; do
                        if [ "$tag" != "latest" ] && [ "$tag" != "${IMAGE_TAG}" ]; then
                            docker rmi "$id"
                        fi
                    done
                    '''
                }
            }
        }
    }
    
    post {
        success {
            script {
                // 성공 시 추가 작업 (옵션)
                echo '파이프라인이 성공적으로 완료되었습니다.'
            }
        }
        failure {
            script {
                // 실패 시 추가 작업 (옵션)
                echo '파이프라인이 실패했습니다.'
            }
        }
    }
}
