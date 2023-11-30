# SERVICE CORE
FROM momoware/service_core_nodejs:latest 


#    # SERVICE CORE
#    # see: https://askubuntu.com/questions/909277/avoiding-user-interaction-with-tzdata-when-installing-certbot-in-a-docker-contai
#    # ACHTUNG: recommended npm dependents are required to avoid SSL/certifcate errors
#    # ACHTUNG: try to keep this part identical among all microservices to optimize cache usage
#    FROM ubuntu:latest 
#    
#    ENV DEBIAN_FRONTEND=noninteractive 
#    RUN apt update
#    RUN apt --no-install-recommends install -y curl
#    
#    #install curl
#    RUN apt update
#    RUN apt --no-install-recommends install -y wget
#    WORKDIR /usr/local
#    RUN apt-get --no-install-recommends install -y ca-certificates
#    RUN update-ca-certificates
#    RUN wget https://nodejs.org/dist/v16.13.0/node-v16.13.0-linux-x64.tar.xz
#    RUN apt install xz-utils
#    RUN tar -xJf node-v16.13.0-linux-x64.tar.xz 
#    WORKDIR /usr/local/bin
#    RUN ln -s /usr/local/node-v16.13.0-linux-x64/bin/node
#    RUN ln -s /usr/local/node-v16.13.0-linux-x64/bin/npm
#    

# copy routing sourcefiles, docker build is called from the parentdir
# of services, libraries, apps, node_modules
WORKDIR /eopti
COPY ./services/helloworld/nodejs/*.js ./
COPY ./services/helloworld/nodejs/package.json ./

# run npm to install dependenciesn start with node
# RUN npm install

# copy momo/eopti libraries, dont know how to include these in package.json
# which means they are deleted upon npm install
#COPY ./node_modules/eopti/ ./node_modules/eopti/
#COPY ./node_modules/momo/ ./node_modules/momo/
# copy eopti libraries, dont know how to include these in package.json
# which means they are deleted upon npm install
COPY ./libraries/eopti/ms/ ./node_modules/eopti/ms/
COPY ./libraries/eopti/*.js ./node_modules/eopti/
COPY ./libraries/momo/http/ ./node_modules/momo/http/
COPY ./libraries/momo/tools/ ./node_modules/momo/tools/
COPY ./libraries/momo/setEnvironment.js ./node_modules/momo
#
# CMD ["/bin/bash"]
CMD ["node", "./helloworld.js"]


