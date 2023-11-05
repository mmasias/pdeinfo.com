#!/usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
#Tratamiento de los datos
#------------------------
	if ($name eq "nick") {$_ = $value;s/\+/ /g;$nick = $_;}
	if ($name eq "fec") {$_ = $value;s/\+/ /g;$fec = $_;}
}
print ("Content-Type: text/html\n\n");
open(Farch,"registrados.bd");
$enc="no";
while(<Farch>){
$linea=$_;
@lista=split(/:/,$linea);
if(@lista[0] eq $nick){
 $enc="si";
 last;
}
}
if($enc eq "si"){
 print $linea;
}
close(Farch);
