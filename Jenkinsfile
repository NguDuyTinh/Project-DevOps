pipeline {
    agent any
    tools {
        nodejs 'nodejs'
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                // sh 'npm run build'
                echo 'Build'
            }
        }
        
        stage('Test') {
            steps {
                // sh 'npm install'
                // sh 'npm run build'
                echo 'Test1'
            }
        }
    }
}
