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
}
print ("Content-Type: text/html\n\n");
open(Farch,"postales.bd");
while(<Farch>){
$linea=$_;
chop($linea);
print "$linea-";
}
close(Farch);
