## after ssh instructions

cd /var/app
source venv/staging-LQM1lest/bin/activate
cd current/
sudo cp /etc/pki/tls/certs/autoave-global-firebase-adminsdk.json ./autoave-global-firebase-adminsdk.json
sudo chown ec2-user ./autoave-global-firebase-adminsdk.json