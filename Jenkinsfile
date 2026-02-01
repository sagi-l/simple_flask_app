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
              # Build image to docker tarball format
              buildctl --addr unix:///run/buildkit/buildkitd.sock build \
                --frontend dockerfile.v0 \
                --local context=. \
                --local dockerfile=. \
                --output type=docker,dest=/tmp/image.tar
              
              # Install crane
              wget -qO- https://github.com/google/go-containerregistry/releases/download/v0.20.0/go-containerregistry_Linux_x86_64.tar.gz | tar xz -C /tmp crane
              
              # Login and push
              echo "$DOCKER_PASS" | /tmp/crane auth login index.docker.io -u "$DOCKER_USER" --password-stdin
              /tmp/crane push /tmp/image.tar docker.io/${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
            '''
          }
        }
      }
    }
  }
  
  post {
    success {
      echo "Pushed ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
    }
    failure {
      echo 'Build or push failed'
    }
  }
}
