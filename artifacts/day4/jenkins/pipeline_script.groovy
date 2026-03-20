pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps { sh 'echo Preparation stage' }
        }
        stage('Build') {
            steps { sh 'echo Build stage' }
        }
        stage('Results') {
            steps { sh 'echo Results stage' }
        }
    }
}
