FROM python:3.6-alpine

# Install Pillow
RUN apk add --no-cache jpeg-dev zlib-dev && \
    apk add --no-cache --virtual .build-deps build-base linux-headers && \
    pip install pip --upgrade && \
    pip install Pillow && \
    apk del .build-deps && \
    rm -rf /root/.cache

# Install Numpy
RUN apk --no-cache add --virtual .builddeps gcc gfortran musl-dev && \
    pip install numpy==1.14.0 && \
    apk del .builddeps && \
    rm -rf /root/.cache

# Install Scipy
RUN apk update \
    && apk add \
    ca-certificates \
    libstdc++ \
    libgfortran \
    && apk add --virtual=build_dependencies \
    gfortran \
    g++ \
    make \
    python3-dev \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && mkdir -p /tmp/build \
    && cd /tmp/build/ \
    && wget http://www.netlib.org/blas/blas-3.6.0.tgz \
    && wget http://www.netlib.org/lapack/lapack-3.6.1.tgz \
    && tar xzf blas-3.6.0.tgz \
    && tar xzf lapack-3.6.1.tgz \
    && cd /tmp/build/BLAS-3.6.0/ \
    && gfortran -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f \
    && ar r libfblas.a *.o \
    && ranlib libfblas.a \
    && mv libfblas.a /tmp/build/. \
    && cd /tmp/build/lapack-3.6.1/ \
    && sed -e "s/frecursive/fPIC/g" -e "s/ \.\.\// /g" -e "s/^CBLASLIB/\#CBLASLIB/g" make.inc.example > make.inc \
    && make lapacklib \
    && make clean \
    && mv liblapack.a /tmp/build/. \
    && cd / \
    && export BLAS=/tmp/build/libfblas.a \
    && export LAPACK=/tmp/build/liblapack.a \
    && pip install scipy \
    && apk del --purge -r build_dependencies \
    && rm -rf /tmp/build \
    && rm -rf /var/cache/apk/*

# Install NoteShrinker
RUN pip install NoteShrinker && mkdir /imgs
WORKDIR /imgs

ENTRYPOINT ["note-shrinker"]
