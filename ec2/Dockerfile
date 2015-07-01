FROM ubuntu

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install wget
RUN apt-get -y install unzip

RUN git clone https://github.com/NYPDVisionZeroAccountability/compstat-vs-moving-violation-enforcement.git

RUN useradd -m devuser

ENV SOLR_VERSION 5.2.1
ENV SOLR solr-$SOLR_VERSION
ENV SOLR_USER devuser

RUN apt-get -y install lsof procps
RUN mkdir -p /opt
RUN wget -nv --output-document=/opt/$SOLR.tgz http://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/$SOLR.tgz
RUN tar -C /opt --extract --file /opt/$SOLR.tgz
RUN rm /opt/$SOLR.tgz
RUN ln -s /opt/$SOLR /opt/solr
RUN chown -R $SOLR_USER:$SOLR_USER /opt/solr /opt/$SOLR

RUN apt-get -y install openjdk-7-jre-headless

EXPOSE 8983
WORKDIR /opt/solr
USER $SOLR_USER
CMD ["/bin/bash", "-c", "/opt/solr/bin/solr -f"]
