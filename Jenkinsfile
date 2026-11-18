pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        script {
          def scmVars = checkout([
            $class: 'GitSCM',
            branches: [[name: '*/main']],
            userRemoteConfigs: [[url: 'https://github.com/Shayanahmed99/devops-midterm.git']]
          ])
          env.GIT_COMMIT = scmVars.GIT_COMMIT
        }
      }
    }

    stage('Train') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          python train.py
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          . venv/bin/activate
          pytest -q
        '''
      }
    }

    stage('Build Image') {
      steps {
        sh 'docker build -t midterm-app:latest .'
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          docker rm -f midterm-app || true
          docker run -d --name midterm-app --restart unless-stopped -p 8000:8000 midterm-app:latest
          for i in 1 2 3 4 5 6 7 8 9 10; do
            if curl -sf http://localhost:8000/metrics; then exit 0; fi
            sleep 3
          done
          docker logs midterm-app
          exit 1
        '''
      }
    }
  }

  post {
    always {
      emailext(
        to: 'qasimalik@gmail.com',
        from: 'shayanahmedmalik99@gmail.com',
        subject: "FA23-BDS-037 build ${currentBuild.currentResult} #${env.BUILD_NUMBER}",
        body: """Student Reg No: FA23-BDS-037
Result: ${currentBuild.currentResult}
Commit: ${env.GIT_COMMIT}
Build: ${env.BUILD_URL}"""
      )
    }
  }
}