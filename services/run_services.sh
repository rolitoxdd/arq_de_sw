trap 'kill %1; kill %2; kill %3; kill %4; kill %5' SIGINT
python3 services/serv1.py & \
python3 services/serv2.py & \
python3 services/serv3.py & \
python3 services/serv4.py & \
python3 services/serv5.py & \
python3 services/serv6.py & \
python3 services/serv7.py 