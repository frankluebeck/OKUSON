all:	postera4.pdf poster.pdf

postera4.pdf:	postera4.ps
	ps2pdf postera4.ps

postera4.ps:	poster.ps psa0toa4
	./psa0toa4 poster.ps postera4.ps

poster.pdf:	poster.ps
	ps2pdf poster.ps

poster.ps:	poster.dvi config.a0
	dvips -P a0 -P cmz -P amz poster.dvi -o poster.ps

poster.dvi:	poster.tex a0poster.cls a0size.sty
	latex poster

clean:
	rm -f poster.pdf postera4.pdf poster.ps postera4.ps poster.log \
	      poster.out poster.aux poster.dvi a0header.ps
