#!/usr/local/bin/perl
require "curriculo_configuracion.pl";

read(STDIN,$input,$ENV{CONTENT_LENGTH});
print("Content-Type: text/html\n\n");
print "<HR>";
@tmp= split("&",$input); 

foreach(@tmp) {
		# ----------------------------------
		# Reemplazar los caracteres extraños
		# ----------------------------------
		s/%0D%0A/<BR>/g; 										# Con esto ponemos <BR> a todos los saltos de linea
																				# Si este va debajo de la correccion general
																				# Entonces si los pone como multiples lineas
																				
		s/\+/ /g;														# Correccion de los espacios
		s/%40/\@/g;													# Corrección de la arroba
		s/%(..)/pack("c",hex($1))/ge;				# Corrección general sugerida por el PERL
    ($nombre,$valor)= split("=", $_);
    print "$nombre \t $valor<br>";
    $datos{$nombre}=$valor;
}
print "<HR>";