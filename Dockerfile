FROM python:3-alpine AS build

COPY . /pytezos
RUN apk update \
	&& apk --no-cache add --virtual build-deps \
	    build-base \
		libffi-dev \
		libressl-dev \
	&& pip3 install poetry==1.0.5 \
	&& cd /pytezos && poetry build


FROM python:3-alpine

COPY --from=build /pytezos/dist/*.whl /tmp/pytezos/
RUN apk update \
	&& apk --no-cache add --virtual build-deps \
		build-base \
		autoconf \
		automake \
		git \
		gmp-dev \
		isl \
		libatomic \
		libffi-dev \
		libgomp \
		libressl-dev \
		libtool \
		make \
		mpfr4 \
		mpc1 \
		musl-dev \
		openssl \
	&& apk --no-cache add \
		binutils \
		libsodium-dev \
	&& git clone https://github.com/bitcoin-core/secp256k1.git /tmp/secp256k1 && cd /tmp/secp256k1 \
	&& ./autogen.sh \
	&& ./configure \
	&& make install \
	&& cd / && rm -rf /tmp/secp256k1 \
	&& pip3 install --no-cache-dir poetry==1.0.5 \
	&& pip3 install --no-build-isolation --no-cache-dir pendulum==2.1.0 \
    && pip3 install --no-cache-dir /tmp/pytezos/*.whl && rm -rf /tmp/pytezos \
    && pip3 uninstall --yes poetry \
	&& rm -rf ~/.cache/pip && apk del py-pip \
	&& apk del build-deps \
	&& rm -f /sbin/apk && rm -rf /etc/apk && rm -rf /lib/apk && rm -rf /usr/share/apk && rm -rf /var/lib/apk
