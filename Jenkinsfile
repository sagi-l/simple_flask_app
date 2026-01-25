pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      namespace 'jenkins-agents'
      defaultContainer 'jnlp'

      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: buildctl
    image: moby/buildkit:v0.19.0
    command:
      - sleep
    args:
      - infinity
    volumeMounts:
      - name: buildkit
        mountPath: /run/buildkit
      - name: workspace-volume
        mountPath: /home/jenkins/agent
    workingDir: /home/jenkins/agent

  - name: buildkitd
    image: moby/buildkit:v0.19.0
    args:
      - --addr
      - unix:///run/buildkit/buildkitd.sock
    securityContext:
      privileged: true
    volumeMounts:
      - name: buildkit
        mountPath: /run/buildkit
      - name: workspace-volume
        mountPath: /home/jenkins/agent
    workingDir: /home/jenkins/agent

  volumes:
  - name: buildkit
    emptyDir: {}
  - name: workspace-volume
    emptyDir: {}
"""
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
            def tag = env.BRANCH_NAME?.replaceAll('/', '-') ?: 'local'

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
