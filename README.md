# Weathermom
Commands to run the program:
Get into ubuntu: ssh -i "labsuser.pem" ubuntu@ec2-54-87-155-49.compute-1.amazonaws.com
to activate virtual env:  source myenv/bin/activate
navigate to the folder: cd New\ folder
export FLASK_APP=weathermom
flask run --port=8080 --host=0.0.0.0
URL(changes every time): http://ec2-54-87-155-49.compute-1.amazonaws.com:8080/
