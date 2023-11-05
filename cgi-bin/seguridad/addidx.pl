#!/usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
#Tratamiento de los datos
#------------------------
	if ($name eq "nombre") {$_ = $value;s/\+/ /g;$nombre = $_;}
	if ($name eq "url") {$_ = $value;s/\+/ /g;$url = $_;}
	if ($name eq "categoria") {$_ = $value;s/\+/ /g;$categoria = $_;}
	if ($name eq "descripcion") {$_ = $value;s/\+/ /g;$descripcion = $_;}
}
open(ARCH,"cnt.dat");
$lin=<ARCH>;
close(ARCH);
if ($lin eq "") {
 $lin=0;
}
$val=$lin+1;
open(ARCH,">cnt.dat");
print ARCH "$val";
close(ARCH);
open(Farch,">>pdeinfo.idx");
print Farch "$val^$nombre^$url^$categoria^$descripcion\n";
close(Farch);