# testerNloggerWAN
It tests the WAN connection and it logs the status on every change.



# How to create a service
References:
- https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
- https://stackoverflow.com/questions/35984151/how-to-create-new-system-service-by-ansible-playbook

- Criar link simbólico
sudo ln -s /opt/testerNlogger/testernlogger.service /etc/systemd/system/testernlogger.service

- Reload the service files to include the new service.
sudo systemctl daemon-reload

- Start your service
sudo systemctl start testernlogger.service

- To check the status of your service
sudo systemctl status testernlogger.service

- To enable your service on every reboot
sudo systemctl enable testernlogger.service