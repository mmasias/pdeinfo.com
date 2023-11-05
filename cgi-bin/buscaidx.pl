#!/usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
#Tratamiento de los datos
#------------------------
	if ($name eq "txtbusca") {$_ = $value;s/\+/ /g;$txtbusca = $_;}
}
print "<table>";
open(Farch,"pdeinfo.idx");
$enc="no";
while(<Farch>){
$linea=$_;
@lista=split(/\^/,$linea);
$pos = rindex($linea,$txtbusca);
if($pos >0){
 print "<tr><td>@lista[1]</td><td><A href=@lista[2]>@lista[2]</a></td></tr>";
 $enc="si";
}
}
if($enc eq "no"){
	print "<tr><td>Lo siento no se encontraron coicidencias</td></tr>";
	}
print("</table>");
close(Farch);