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
open(Farch,"$fec");
$enc="no";
while(<Farch>){
$linea=$_;
@lista=split(/:/,$linea);
chop(@lista[1]);
if(@lista[1] eq $nick){
 chop(@lista[1]);
 push(@todos,@lista[0]);
 $enc="si";
}
}
if($enc eq "si"){
 $i=0;
 foreach(@todos){
  $i++;
 }
 if( $i>1) {
  print "$i:@todos[$i-1]"; 
 }
 else {
  print "$i:@todos[0]";
 }
}
close(Farch);
