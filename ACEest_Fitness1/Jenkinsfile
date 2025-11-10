pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // configure in Jenkins
    SONARQUBE = 'SonarQube' // the SonarQube server configured in Jenkins global config
    IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/aceest-fitness1"
    GIT_COMMIT_SHORT = "${env.GIT_COMMIT?.substring(0,7)}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r app/aceest_fitness1/requirements.txt'
        sh 'pytest -q --junitxml=reports/junit.xml'
        junit 'reports/junit.xml'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv("${SONARQUBE}") {
          sh 'pip install sonar-scanner'
          sh 'sonar-scanner -Dsonar.projectKey=ACEest_Fitness -Dsonar.sources=app/aceest_fitness1 -Dsonar.python.version=3.11'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def tag = "${env.BUILD_NUMBER}"
          sh "docker build -t ${IMAGE}:${tag} -f docker/Dockerfile ."
          sh "docker tag ${IMAGE}:${tag} ${IMAGE}:latest"
        }
      }
    }

    stage('Push Image') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
            sh "docker push ${IMAGE}:${env.BUILD_NUMBER}"
            sh "docker push ${IMAGE}:latest"
          }
        }
      }
    }

    stage('Deploy to Kubernetes (Minikube / cluster)') {
      steps {
        // Configure kubeconfig in Jenkins credentials, or use kubectl installed on agent
        sh 'kubectl apply -f k8s/service.yaml'
        sh 'kubectl apply -f k8s/deployment-rolling.yaml'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
    failure {
      mail to: 'your-email@example.com',
           subject: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
           body: "Check Jenkins console output"
    }
  }
}
