pipeline {
    agent any
    
    environment {
        AWS_ECR_REPO = '471112869272.dkr.ecr.ap-northeast-2.amazonaws.com/backend'
        GIT_CREDENTIALS_ID = 'Jenkins_backend_credential'
        ECR_REGION = 'ap-northeast-2'
        IMAGE_TAG = "${env.BUILD_NUMBER}" // 빌드 번호를 태그로 사용
        BACKEND_REPO = 'https://github.com/Mozo119/Jenkins_backend.git'
        MANIFEST_REPO = 'https://github.com/Mozo119/Jenkins_backend_manifest.git'
        MANIFEST_REPO_CREDENTIALS_ID = 'Jenkins_backend_manifest_credential'
    }
    
    stages {
        stage('Checkout Backend Repository') {
            steps {
                // 젠킨스 백엔드 레포지토리에서 소스 코드 체크아웃
                script {
                    git branch: 'main',
                        credentialsId: "${GIT_CREDENTIALS_ID}",
                        url: "${BACKEND_REPO}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // AWS ECR 로그인
                script {
                    withCredentials([usernamePassword(credentialsId: 'aws-ecr-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        sh '''
                        aws ecr get-login-password --region ${ECR_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_REPO}
                        '''
                    }
                }
                
                // Docker 이미지 빌드
                sh 'docker build -t ${AWS_ECR_REPO}:${IMAGE_TAG} .'
                
                // Docker 이미지 태그
                sh 'docker tag ${AWS_ECR_REPO}:${IMAGE_TAG} ${AWS_ECR_REPO}:latest'
                
                // Docker 이미지 푸시
                sh 'docker push ${AWS_ECR_REPO}:${IMAGE_TAG}'
                sh 'docker push ${AWS_ECR_REPO}:latest'
            }
        }
        
        stage('Update Manifest Repository') {
            steps {
                // 매니페스트 레포지토리 업데이트
                withCredentials([usernamePassword(credentialsId: "${MANIFEST_REPO_CREDENTIALS_ID}", usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        sh '''
                        sed -i 's|{{AWS_ECR_REPO}}|'${AWS_ECR_REPO}'|g' Jenkins_backend_manifest/deployment.yaml
                        sed -i 's|{{IMAGE_TAG}}|'${IMAGE_TAG}'|g' Jenkins_backend_manifest/deployment.yaml
                        cd Jenkins_backend_manifest
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
                // Docker 이미지를 정리
                script {
                    sh '''
                    docker images --filter "reference=${AWS_ECR_REPO}" --format "{{.ID}} {{.Tag}}" | while read -r id tag; do
                        if [ "$tag" != "latest" ] && [ "$tag" != "${IMAGE_TAG}" ]; then
                            docker rmi -f "$id"
                        fi
                    done
                    '''
                }
            }
        }
    }
}
