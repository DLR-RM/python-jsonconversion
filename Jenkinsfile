pipeline {
    agent {
        label "rmc-vosl423-x8664-build01"
    }

    parameters {
        string(name: 'tox_args', defaultValue: '-v', description: 'Arguments passed to tox besides the environment name')
        string(name: 'pytest_args', defaultValue: '-vx', description: 'Arguments passed to pytest')
    }

    environment {
        TOX_LIMITED_SHEBANG = 1
        // Allows 1st build of a project to succeed, workaround for https://issues.jenkins-ci.org/browse/JENKINS-41929
        tox_args = "${params.tox_args}"
        pytest_args = "${params.pytest_args}"
    }

    options {
        timestamps()
    }

    stages {

        stage('Prepare tox') {
            steps {
                sh 'pip3 install -q --user --ignore-installed tox==3.8'
            }
        }

        stage('Test Python 2.7') {
            steps {
                // Run test
                // * specify tox environment
                // * collect pytest results in XML file
                // * set absolute cache_dir
                sh "~/.local/bin/tox -e py27 $tox_args -- $pytest_args --junitxml $WORKSPACE/pytest_py27_results.xml -o cache_dir=$WORKSPACE |& tee pytestout.txt"
            }
        }

        stage('Test Python 3.4') {
            steps {
                sh "~/.local/bin/tox -e py34 $tox_args -- $pytest_args --junitxml $WORKSPACE/pytest_py34_results.xml -o cache_dir=$WORKSPACE |& tee pytestout.txt"
            }
        }

        stage('Test Python 3.6') {
            environment {
                PATH = "/opt/python/osl42-x86_64/python3/stable/1.0.2/bin:$PATH"
                LD_LIBRARY_PATH = "/opt/python/osl42-x86_64/python3/stable/1.0.2/lib:$LD_LIBRARY_PATH"
            }
            steps {
                sh "~/.local/bin/tox -e py36 $tox_args -- $pytest_args --junitxml $WORKSPACE/pytest_py36_results.xml -o cache_dir=$WORKSPACE |& tee pytestout.txt"
            }
        }

    }
    post {
        failure {
            rocketSend channel: 'jsonconversion-jenkins', avatar: 'https://rmc-jenkins.robotic.dlr.de/jenkins/static/ff676c77/images/headshot.png', message: ":sob: <$BUILD_URL|Build $BUILD_NUMBER> on branch '$BRANCH_NAME' *failed*! Commit: <https://rmc-github.robotic.dlr.de/common/python-jsonconversion/commit/$GIT_COMMIT|$GIT_COMMIT> :sob:", rawMessage: true
        }
        unstable {
            junit '**/pytest_*_results.xml'
            rocketSend channel: 'jsonconversion-jenkins', avatar: 'https://rmc-jenkins.robotic.dlr.de/jenkins/static/ff676c77/images/headshot.png', message: ":sob: <$BUILD_URL|Build $BUILD_NUMBER> on branch '$BRANCH_NAME' *failed* (unstable)! Commit: <https://rmc-github.robotic.dlr.de/common/python-jsonconversion/commit/$GIT_COMMIT|$GIT_COMMIT> :sob:", rawMessage: true
        }
        success {
            junit '**/pytest_*_results.xml'
            rocketSend channel: 'jsonconversion-jenkins', avatar: 'https://rmc-jenkins.robotic.dlr.de/jenkins/static/ff676c77/images/headshot.png', message: ":tada: <$BUILD_URL|Build $BUILD_NUMBER> on branch '$BRANCH_NAME' *succeeded*! Commit: <https://rmc-github.robotic.dlr.de/common/python-jsonconversion/commit/$GIT_COMMIT|$GIT_COMMIT> :tada:", rawMessage: true
            archiveArtifacts artifacts: '.tox/dist/*', fingerprint: true
        }
    }
}
