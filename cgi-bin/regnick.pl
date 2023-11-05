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
	if ($name eq "nombres") {$_ = $value;s/\+/ /g;$nombres = $_;}
	if ($name eq "email") {$_ = $value;s/\+/ /g;$email = $_;}
	if ($name eq "tel") {$_ = $value;s/\+/ /g;$tel = $_;}
	if ($name eq "ciudad") {$_ = $value;s/\+/ /g;$ciudad = $_;}
	if ($name eq "pais") {$_ = $value;s/\+/ /g;$pais = $_;}
	if ($name eq "paswd") {$_ = $value;s/\+/ /g;$paswd = $_;}
	if ($name eq "oculto") {$_ = $value;s/\+/ /g;$oculto = $_;}
}
print ("Content-Type: text/html\n\n");
open(Farch,"registrados.bd");
while(<Farch>){
$linea=$_;
@lista=split(/:/,$linea);
if(@lista[0] eq $nick){ 
 $enc="si";
 last;
}
}
close(Farch);
if($enc eq "si") {
 print "Error";
}
else {
open(Farch,">>registrados.bd");
print Farch "$nick:$nombres:$email:$tel:$ciudad:$pais:$paswd:$oculto:\n";
close(Farch);
}
