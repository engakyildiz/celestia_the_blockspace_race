# celestia_the_blockspace_race
Celestia Light Node Tasks

In the study, a simple example was created using the Python programming language "pywebio" library and "Flask".

As a prerequisite, Docker application must be installed on your computer.

To run the application, clone this repository to your local machine and navigate to the project directory. Then, start the application using docker.


git clone https://github.com/engakyildiz/celestia_the_blockspace_race.git
cd celestia_the_blockspace_race/
cd pfb/
docker build -t flask-app .
docker run -p 5000:5000 flask-app
