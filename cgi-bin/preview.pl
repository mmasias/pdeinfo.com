#!/usr/local/bin/perl
#---------------------------------------------------
#--->>>Revisado por Manolo 10:04 p.m. 23/12/99<<<---
#---------------------------------------------------
print("Content-Type: text/html\n\n");
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
    $fields{$name}=$value;
#Tratamiento de los datos
#------------------------
	if ($name eq "apellidos_y_nombres") {$_ = $value;s/\+/ /g;$apellidos_y_nombres = $_;}
	if ($name eq "login") {$_ = $value;s/\+/ /g;$login = $_;}
	if ($name eq "paswd") {$_ = $value;s/\+/ /g;$paswd = $_;}
	if ($name eq "situacion") {$_ = $value;s/\+/ /g;$situacion = $_;}
	if ($name eq "direccion_actual") {$_ = $value;s/\+/ /g;$direccion_actual = $_;}
	if ($name eq "telefono") {$_ = $value;s/\+/ /g;$telefono = $_;}
	if ($name eq "correo_electronico") {$_ = $value;s/\+/ /g;$correo_electronico = $_;}
	if ($name eq "lugar_y_fecha_de_nacimiento") {$_ = $value;s/\+/ /g;$lugar_y_fecha_de_nacimiento = $_;}
	if ($name eq "documento_de_identidad") {$_ = $value;s/\+/ /g;$documento_de_identidad = $_;}
	if ($name eq "primaria") {$_ = $value;s/\+/ /g;$primaria = $_;}
	if ($name eq "secundaria") {$_ = $value;s/\+/ /g;$secundaria = $_;}
	if ($name eq "superior") {$_ = $value;s/\+/ /g;$superior = $_;}
	if ($name eq "otros_estudios") 
		{@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$otros_estudios=$otros_estudios.$_."<br>";
		}}

	if ($name eq "lengua_nativa") {$_ = $value;s/\+/ /g;$lengua_nativa = $_;}
	if ($name eq "idioma_1") {$_ = $value;s/\+/ /g;$idioma_1 = $_;}	
	if ($name eq "idioma_2") {$_ = $value;s/\+/ /g;$idioma_2 = $_;}	
	if ($name eq "otro_idioma") {$_ = $value;s/\+/ /g;$otro_idioma = $_;}	

	if ($name eq "cursos_y_seminarios") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$cursos_y_seminarios=$cursos_y_seminarios.$_."<br>";
		}}

	if ($name eq "experiencia_laboral") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$experiencia_laboral=$experiencia_laboral.$_."<br>";
		}}

	if ($name eq "software_que_maneja") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$software_que_maneja=$software_que_maneja.$_."<br>";
		}}

	if ($name eq "hobbies") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$hobbies=$hobbies.$_."<br>";
		}}
	
	if ($name eq "intereses_profesionales") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$intereses_profesionales=$intereses_profesionales.$_."<br>";
		}}	
}

$directorio="/www/pdeinfo/curriculos";
$basedatos="curri.bd";


#------------------
# Rutina principal
#------------------
if ($situacion eq "nuevo_curriculo"){
	#Grabar la base de datos.
	open(Farch,"$login");
	$paswd=<Farch>;
	close(Farch);
#	chop($paswd);
	unlink $login;
	open(Farch,">>$basedatos");
	print Farch "$login^$paswd^$apellidos_y_nombres^$direccion_actual^$telefono^$correo_electronico^$lugar_y_fecha_de_nacimiento^$documento_de_identidad^$primaria^$secundaria^$superior^$otros_estudios^$lengua_nativa^$idioma_1^$idioma_2^$otro_idioma^$experiencia_laboral^$cursos_y_seminarios^$software_que_maneja^$hobbies^$intereses_profesionales\n";
	close(Farch);
	#Generar el HTML de redireccion.
	open(Farch,">>$directorio/$login.htm");
	print Farch "<HTML><HEAD>\n";
	print Farch "<META HTTP-EQUIV='Refresh' CONTENT='3; URL=/cgi-bin/revisa.pl?$login'>\n";
	print Farch "<TITLE>Espere un momento...</TITLE></HEAD>\n";
	print Farch "<BODY>\n";
	print Farch "<FONT FACE='Ms Sans Serif' SIZE='3'>\n";
	print Farch "<BIG>Generando currículo...</BIG><BR><BR>\n";
	print Farch "Espere un momento mientras el sistema genera el currículo de <B>$apellidos_y_nombres</B><BR><BR>";
	print Farch "Si su navegador no lo lleva a la página requerida en 10 segundos,"; 
	print Farch "por favor pulse <A HREF='/cgi-bin/revisa.pl?$login'>aquí</A>\n";
	print Farch "<HR></FONT></BODY></HTML>\n";
	close(Farch);
	#Imprimir la pagina de respuesta.
	print("Content-Type: text/html\n\n");
	print("<HEAD><TITLE>Resultados</TITLE>");
	print("<META HTTP-EQUIV='Refresh' CONTENT='5; URL=/curriculos'></HEAD>\n");
	print("<body background='/curriculos/_themes/sumipntg/sumtextb.jpg' bgcolor='#FFFFCC' text='#000066' link='#660099' vlink='#993366' alink='#6666CC'><font face='Verdana, Arial, Helvetica'>");
	print("<H1>Datos grabados</H1>");
	print("<p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("<H3>Su información ha sido recibida con éxito.</H3>");
	print("Pulse <A HREF='/curriculos'>aqui</A> para volver a la página principal.");
	print("<SMALL><p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("<p align='center'>Este es un servicio gratuito de <a href='http://pdeinfo.com' target='_blank'>Punto de Información</a></p>");
	print("<blockquote><p><font size='1'>Aunque Punto de Información hace un esfuerzo por validar la información que se");
	print("presenta en estas páginas, no es responsable por errores u omisiones incluidos en estas.</font></p>");
	print("<p><small><br>Todos los derechos reservados - Sistemas PdeInfo - 1999</small></p>");
	print("<p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("</blockquote></body>");
	}

if ($situacion eq "edita_curriculo"){
	open(ESCR,">temp.dat");
	open(Farch,"$basedatos");
	while(<Farch>) {
	 $linea=$_;
	 @lista=split(/\^/,$_);
         if (@lista[0] eq $login ) {
          print ESCR "$login^@lista[1]^$apellidos_y_nombres^$direccion_actual^$telefono^$correo_electronico^$lugar_y_fecha_de_nacimiento^$documento_de_identidad^$primaria^$secundaria^$superior^$otros_estudios^$lengua_nativa^$idioma_1^$idioma_2^$otro_idioma^$experiencia_laboral^$cursos_y_seminarios^$software_que_maneja^$hobbies^$intereses_profesionales\n";
	}
	else {
         print ESCR $linea;
        } 
 
 }
	close(Farch);
	close(ESCR);
	unlink "curri.bd";
	rename("temp.dat","curri.bd");
	print("<HEAD><TITLE>Resultados</TITLE>\n");
	print("<META HTTP-EQUIV='Refresh' CONTENT='3; URL=/curriculos'></HEAD>");
	print("<body background='/curriculos/_themes/sumipntg/sumtextb.jpg' bgcolor='#FFFFCC' text='#000066' link='#660099' vlink='#993366' alink='#6666CC'><font face='Verdana, Arial, Helvetica'>");
	print("<H1>Datos actualizados</H1>");
	print("<p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("<H3>Su información ha sido actualizada con éxito.</H3>");
	print("Por favor espere un momento mientras el sistema finaliza la actualización.");
	print("<SMALL><p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("<p align='center'>Este es un servicio gratuito de <a href='http://pdeinfo.com' target='_blank'>Punto de Información</a></p>");
	print("<blockquote><p><font size='1'>Aunque Punto de Información hace un esfuerzo por validar la información que se");
	print("presenta en estas páginas, no es responsable por errores u omisiones incluidos en estas.</font></p>");
	print("<p><small><br>Todos los derechos reservados - Sistemas PdeInfo - 1999</small></p>");
	print("<p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");
	print("</blockquote></body>");
}