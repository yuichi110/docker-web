From jenkins/jenkins:2.190.1-centos

USER root
RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
RUN yum install -y yum-utils device-mapper-persistent-data lvm2 docker-ce-cli 
RUN curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN cd ~/.ssh; cat /dev/zero | ssh-keygen -t rsa -m PEM -q -N ""
RUN cp ~/.ssh/id_rsa.pub ~/
Expose 8080
Expose 50000

USER jenkins
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/jenkins.sh"]