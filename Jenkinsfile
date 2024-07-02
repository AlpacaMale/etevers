pipeline {
    agent any

    environment {
        MANIFEST_REPO = 'https://github.com/Mozo119/Jenkins_backend_manifast.git'
        AWS_ECR_REPO = '471112869272.dkr.ecr.ap-northeast-2.amazonaws.com/backend'
        IMAGE_TAG = '73'
        GIT_USERNAME = 'Mozo119'
        GIT_PASSWORD = 'your_password_or_token' // 이 부분은 Jenkins 자격 증명으로 대체하는 것이 좋습니다.
    }

    stages {
        stage('Update Manifest Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Jenkins_backend_manifest_credential', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        sh '''
                        rm -rf Jenkins_backend_manifast
                        git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFEST_REPO}
                        cd Jenkins_backend_manifast
                        echo "Updating deployment.yaml with AWS_ECR_REPO: ${AWS_ECR_REPO} and IMAGE_TAG: ${IMAGE_TAG}"
                        sed -i 's|{{AWS_ECR_REPO}}|'${AWS_ECR_REPO}'|g' deployment.yaml
                        sed -i 's|{{IMAGE_TAG}}|'${IMAGE_TAG}'|g' deployment.yaml
                        echo "Updated deployment.yaml:"
                        cat deployment.yaml  # 확인을 위해 추가
                        git config --global user.email "rlaalstjr0502@gmail.com"
                        git config --global user.name "Mozo119"
                        git add deployment.yaml
                        git status  # 변경 사항 확인을 위해 추가
                        git commit -m "Update image to ${IMAGE_TAG}" || echo "Nothing to commit"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFEST_REPO}
                        '''
                    }
                }
            }
        }
    }
}
