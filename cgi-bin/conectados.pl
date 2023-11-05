#!/usr/local/bin/perl
print ("Content-Type: text/html\n\n");
print ("<HTML><HEAD><TITLE></TITLE></HEAD><BODY>");
print ("<H1>Usuarios del InfoChat</H1>");
print ("<FONT FACE=Tahoma SIZE=3>El sistema ha determinado que los siguientes usuarios han estado conectados al infochat ");
print ("las ultimas 6 horas (Se indica su Ifc)<P> ");
open(Farch,"11012000.txt");
while(<Farch>){
$linea=$_;
@lista=split(/:/,$linea);
print "><SMALL><B> $lista[0]</SMALL></B><BR>";
}
close(Farch);
print "<HR>";

