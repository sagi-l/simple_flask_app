pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      inheritFrom 'buildkit-agent'
      namespace 'jenkins-agents'
      defaultContainer 'jnlp'
    }
  }
  
  environment {
    DOCKERHUB_USER = 'sabichon'
    IMAGE_NAME = 'simple-flask'
    IMAGE_TAG = "${BUILD_NUMBER}"
  }
  
  options {
    timeout(time: 30, unit: 'MINUTES')
  }
  
  stages {
    stage('Check Trigger') {
      steps {
        script {
          def lastCommit = sh(script: 'git log -1 --pretty=%an', returnStdout: true).trim()
          echo "Last commit by: ${lastCommit}"
          if (lastCommit == 'Jenkins CI') {
            currentBuild.result = 'ABORTED'
            error('Skipping build triggered by Jenkins commit')
          }
        }
      }
    }
    
    stage('Verify BuildKit') {
      steps {
        container('buildctl') {
          sh 'buildctl --addr unix:///run/buildkit/buildkitd.sock debug workers'
        }
      }
    }
    
    stage('Build and Push') {
      steps {
        container('buildctl') {
          withCredentials([usernamePassword(
            credentialsId: 'dockerhub-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
              buildctl --addr unix:///run/buildkit/buildkitd.sock build \
                --frontend dockerfile.v0 \
                --local context=. \
                --local dockerfile=. \
                --output type=docker,dest=/tmp/image.tar
              
              wget -qO- https://github.com/google/go-containerregistry/releases/download/v0.20.0/go-containerregistry_Linux_x86_64.tar.gz | tar xz -C /tmp crane
              
              echo "$DOCKER_PASS" | /tmp/crane auth login index.docker.io -u "$DOCKER_USER" --password-stdin
              /tmp/crane push /tmp/image.tar docker.io/${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
            '''
          }
        }
      }
    }
    
    stage('Update K8s Manifest') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'github-creds',
          usernameVariable: 'GIT_USER',
          passwordVariable: 'GIT_TOKEN'
        )]) {
          sh '''
            git config user.email "jenkins@ci.local"
            git config user.name "Jenkins CI"
            
            sed -i "s|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|" k8s/web-app-deployment.yaml
            
            sed -i "s|value: \\".*\\"  # Jenkins will update this|value: \\"${IMAGE_TAG}\\"  # Jenkins will update this|" k8s/web-app-deployment.yaml
            
            git add k8s/web-app-deployment.yaml
            git commit -m "[skip ci] Deploy ${IMAGE_NAME}:${IMAGE_TAG}"
            
            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/sagi-l/simple_flask_app.git HEAD:main
          '''
        }
      }
    }
  }
  
  post {
    success {
      echo "Pushed ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} and updated k8s manifest"
    }
    failure {
      echo 'Build or push failed'
    }
  }
}
