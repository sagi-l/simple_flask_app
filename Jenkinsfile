pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      inheritFrom 'buildkit-agent'
      namespace 'jenkins-agents'
      defaultContainer 'jnlp'
    }
  }
  options {
    timeout(time: 30, unit: 'MINUTES')
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Verify BuildKit') {
      steps {
        container('buildctl') {
          sh 'buildctl --addr unix:///run/buildkit/buildkitd.sock debug workers'
        }
      }
    }
    stage('Build image (NO PUSH)') {
      steps {
        container('buildctl') {
          sh '''
            buildctl --addr unix:///run/buildkit/buildkitd.sock build \
              --frontend dockerfile.v0 \
              --local context=. \
              --local dockerfile=. \
              --output type=image,name=simple-flask:${env.BRANCH_NAME},push=false
          '''
        }
      }
    }
  }
}
