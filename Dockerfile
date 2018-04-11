FROM odanoburu/gf-deb:3.9

RUN wget -q https://github.com/TALP-UPC/FreeLing/raw/master/data/pt/dictionary/entries/nouns https://github.com/TALP-UPC/FreeLing/raw/master/data/pt/dictionary/entries/verbs

WORKDIR /home/gfer

COPY ./ /home/gfer

CMD ["gf"]
