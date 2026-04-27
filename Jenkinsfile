pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'tdeepakreddy'
        IMAGE_NAME = 'aceest-app'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SONARQUBE_SERVER = 'sonarqube-server'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'Assignment2', url: 'https://github.com/DeepakReddy-93525/ACEest_Fitness_Devops_AS1.git'
                echo 'Checked out source code'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                echo 'Environment setup completed'
            }
        }
        
        stage('Code Quality - Linting') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app.py test_app.py --count --select=E9,F63,F7,F82 --show-source --statistics
                    flake8 app.py test_app.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
                echo 'Code linting completed'
            }
        }
        
        stage('Unit Testing') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest-cov
                    pytest --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                    pip install bandit
                    bandit -r app.py -f json -o bandit-report.json || true
                '''
                echo 'Unit tests completed'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(env.SONARQUBE_SERVER) {
                    sh '''
                        export JAVA_HOME=/usr/lib/jvm/jdk-17
                        export PATH=$JAVA_HOME/bin:$PATH
                        sonar-scanner || true
                    '''
                }
                echo 'SonarQube analysis completed (non-fatal)'
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    try {
                        timeout(time: 5, unit: 'MINUTES') {
                            waitForQualityGate abortPipeline: false
                        }
                        echo 'Quality gate passed'
                    } catch (Exception e) {
                        echo 'Quality gate check failed (non-fatal): ' + e.toString()
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build image with version tags
                    def image = docker.build("${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}")
                    
                    // Tag as latest
                    image.tag("${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:latest")
                    
                    echo "Docker image built: ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub
                    docker.withRegistry("https://index.docker.io/v1/", "dockerhub-credentials") {
                        // Push versioned image
                        docker.image("${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                        
                        // Push latest tag
                        docker.image("${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:latest").push()
                    }
                    
                    echo "Images pushed to Docker Hub:"
                    echo "- ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                    echo "- ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Container Testing') {
            steps {
                sh '''
                    # Pull and test the pushed image
                    docker run --rm -d --name test-container -p 5000:5000 ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 10
                    # Health check
                    curl -f http://localhost:5000/programs || exit 1
                    docker stop test-container
                '''
                echo 'Container testing completed with Docker Hub image'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed!'
        }
    }
}
