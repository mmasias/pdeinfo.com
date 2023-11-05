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
	if ($name eq "ip") {$_ = $value;s/\+/ /g;$ip = $_;}
	if ($name eq "fec") {$_ = $value;s/\+/ /g;$fec = $_;}
}
$ip=$ENV{'REMOTE_ADDR'};
print ("Content-Type: text/html\n\n");
print "$nick $ip $fec";
open(Ftmp,">tmp.000");

if (-e $fec) {
 open(Farch,"$fec");
 $enc="no";
 while(<Farch>){
 $linea=$_;
 @lista=split(/:/,$linea);
 if(@lista[0] eq $nick) {	
 }
 else {
 	print Ftmp "$linea";
 }
}
close(Farch);
}

print Ftmp "$nick:$ip\n";
close(Ftmp);
if (-e $fec) {unlink("$fec");}
rename("tmp.000","$fec");