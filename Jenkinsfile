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
    timeout(time: 10, unit: 'MINUTES')
  }

  stages {

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
          script {
            // Sanitize branch name for Docker tag
            def tag = env.BRANCH_NAME.replaceAll('/', '-')

            sh """
              buildctl \
                --addr unix:///run/buildkit/buildkitd.sock \
                build \
                --frontend dockerfile.v0 \
                --local context=. \
                --local dockerfile=. \
                --output type=image,name=simple-flask:${tag},push=false
            """
          }
        }
      }
    }
  }

  post {
    success {
      echo "Build finished successfully for branch: ${env.BRANCH_NAME}"
    }
    failure {
      echo "Build failed for branch: ${env.BRANCH_NAME}"
    }
  }
}
