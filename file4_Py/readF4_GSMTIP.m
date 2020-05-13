clear all;
%-------------------------------------------------------------------------------
ldor0=1024;
fid = fopen('f4','r');  pole = fread(fid,[ldor0],'float');

if (or(pole(51)~=19,pole(52)~=14) )
  msgbox ("Incorrect kpars or ints in file."); 
endif 
%-------------------------------------------------------------------------------
kpars = floor(pole(51)); nh = floor(pole(60)); 
ddolgs=pole(56);  dtets =pole(57); 
ids=floor(360.1/ddolgs);  its=floor(180.1/dtets+1);

ntr = floor(pole(58)); ddolgt=pole(54); idt = floor(360.1/ddolgt); 
nl=floor(pole(61)); 	nl2=nl+nl+3
%-------------------------------------------------------------------------------
size_zap = ntr*idt*nl2
potef= fread(fid,[size_zap+1],'float');
 
size_zap = kpars*nh*its*ids;
pgl0 = fread(fid,[size_zap],'float');
fclose(fid); 
%-------------------------------------------------------------------------------
pgl = reshape(pgl0,kpars,nh,its,ids);
pgl_ris(:,:) = pgl(1,7,:,:); 
%[X,Y]=meshgrid(its,ids);
hold on; grid on; box on;
pcolor(pgl_ris ); shading interp; colorbar;
%-------------------------------------------------------------------------------