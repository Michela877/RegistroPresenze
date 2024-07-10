pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Michela877/registropresenze.git'
            }
        }
        
        stage('Install dependencies') {
            steps {
                script {
                    powershell '''
                        $env:Path += "C:/Users/leona/AppData/Local/Programs/Python/Python311"
                        python -m venv venv
                        .\\venv\\Scripts\\Activate.ps1
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    powershell '''
                        if (docker images -q registropresenze) {
                            docker rm test
                        }
                        docker build -t registropresenze:latest .
                    '''
                    
                }
            }
        }

        stage('Run Docker container') {
            steps {
                script {
                    powershell '''
                        if (docker ps -q --filter "name=registropresenze_container") {
                            docker stop registropresenze_container
                        }
                        if (docker ps -aq --filter "name=registropresenze_container") {
                            docker rm registropresenze_container
                        }
                        docker run -d -p 6001:6001 --name registropresenze_container registropresenze:latest
                    '''
                }
            }
        }
        
        stage('Remove Docker images') {
            steps {
                script {
                    powershell '''
                        if (docker images -f "dangling=true" -q) {
                            docker image prune -f
                        }
                    ''' 
                }                
            }
        }
    }
}
