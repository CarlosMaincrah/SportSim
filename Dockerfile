FROM alpine:3.12

RUN apk add python3

CMD git clone https://github.com/Pisich/FRIO-MX ; cd FRIO-MX/ ; python3 FRIO.MX ;
