#!/usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
#Tratamiento de los datos
#------------------------
	if ($name eq "campo") {$_ = $value;s/\+/ /g;$campo = $_;}
	if ($name eq "valor") {$_ = $value;s/\+/ /g;$valor = $_;$valor=~tr/A-Z/a-z/;}
}
print ("Content-Type: text/html\n\n");
open(Farch,"registrados.bd");
$enc="no";
while(<Farch>){
$linea=$_;
$busca=$linea;
$busca=~tr/A-Z/a-z/;
@lista=split(/:/,$busca);
if($campo eq "nick"){$cond = (@lista[0] eq $valor)}
if($campo eq "nombres"){$cond = (index(@lista[1],$valor))>=0}
if($campo eq "email"){$cond = (@lista[2] eq $valor)}

if($cond){
 $enc="si";
 #last;
 chop($linea);
 print "$linea^";
}
}
if($enc eq "si"){
 #print $linea;
}
else {
 print "Error";
}
close(Farch);
