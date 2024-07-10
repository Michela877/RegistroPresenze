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
                        if (docker images -q mysql) {
                            docker rm test
                        }
                        docker-compose up --build -d
                    '''
                    
                }
            }
        }

        stage('Run Docker container') {
            steps {
                script {
                    powershell '''
                        if (docker ps -q --filter "name=registropresenze") {
                            docker stop registropresenze
                        }
                        if (docker ps -aq --filter "name=registropresenze") {
                            docker rm registropresenze
                        }
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

                stage('create database') {
            steps {
                script {
                    powershell '''
                        docker exec -it mysql-container bash -c "mysql -h db -u root -prootpassword -e "CREATE DATABASE IF NOT EXISTS presenze_db""
                          
                    ''' 
                }                
            }
        }

                stage('create table database') {
            steps {
                script {
                    powershell '''
                        docker exec -it mysql-container bash -c "mysql -h db -u root -prootpassword -e "USE presenze_db; CREATE TABLE presenze ( id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL, data_presenza DATE NOT NULL, orario_entrata TIME, orario_uscita TIME ); CREATE TABLE utenti ( id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL );""
                          
                    ''' 
                }                
            }
        }

        
    }
}
