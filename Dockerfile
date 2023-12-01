# NOTE: in order to have libraries in scope, we call docker build from the parentdir
#       of services, libraries and apps. All COPY commands must be written accordingly.

# -1- BUILD IMAGE THAT WOULD BE ABLE TO RUN proxy.js
#     and name it BUILD_PROXY to be used in step 3
FROM momoware/service_core_nodejs:latest AS BUILD_PROXY
 
# copy sourcefiles and install (npm) dependencies
WORKDIR /eopti
COPY ./services/text_service/ ./
# RUN npm install

# copy momo/eopti libraries, dont know (yet) how to include these in package.json
COPY ./libraries/eopti/ms/ ./node_modules/eopti/ms/
COPY ./libraries/eopti/*.js ./node_modules/eopti/
COPY ./libraries/momo/http/ ./node_modules/momo/http/
COPY ./libraries/momo/tools/ ./node_modules/momo/tools/
COPY ./libraries/momo/setEnvironment.js ./node_modules/momo


# -2- start the FINAL BUILD, here it is based on python 3.8
FROM python:3.8

# -2.1- copy from BUILD_PROXY the files that are required to run proxy.js
#       but not proxy.js itself yet, we copy this further below because it is more volatile
WORKDIR /eopti/
COPY --from=BUILD_PROXY /eopti/node_modules/ ./node_modules/
COPY --from=BUILD_PROXY /usr/local/bin/node /usr/local/bin/node


# -2.2- then we copy the text-semantic components, this is basically
#       the code in the Dockerfile of the icd10 project
WORKDIR /code
COPY ./services/text_service/pyproject.toml ./
COPY ./services/text_service/poetry.lock ./
RUN pip install poetry==1.6.0
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

# COPY ./services/text_service/embedder ./embedder
# COPY ./services/text_service/classifiers ./classifiers
COPY ./services/text_service/required_classes.py ./required_classes.py
# we dont need the app, its functionality shall be moved to server.py
# COPY ./app.py ./app.py


# -2.3- copy server.py (and its dependencies in momotools),
# which is based on the helloworld server.py and shall implement
# the rest-service connecting the text-semantic implementation
WORKDIR /code
RUN pip install requests
COPY ./services/text_service/momotools/ ./momotools/
COPY ./services/text_service/server.py ./


# -2.4- copy proxy.js
WORKDIR /eopti
COPY --from=BUILD_PROXY /eopti/proxy.js ./

# -4- Calculate build-hash and include via dockerStart.sh the
#     commands to start (at least) proxy.js and server.py 
WORKDIR /eopti
COPY ./services/text_service/dockerStart.sh ./
RUN find . ../code  -exec sha1sum '{}' \; | sort - &> ./file_hashes
RUN cat ./file_hashes | sha1sum - > ./build_hash
CMD ["./dockerStart.sh"]


