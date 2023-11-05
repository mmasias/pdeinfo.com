#!/usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
#Tratamiento de los datos
#------------------------
	if ($name eq "apellidos_y_nombres") {$_ = $value;s/\+/ /g;$apellidos_y_nombres = $_;}
	if ($name eq "direccion_actual") {$_ = $value;s/\+/ /g;$direccion_actual = $_;}
	if ($name eq "login") {$_ = $value;s/\+/ /g;$login = $_;}
	if ($name eq "paswd") {$_ = $value;s/\+/ /g;$paswd = $_;}
	if ($name eq "telefono") {$_ = $value;s/\+/ /g;$telefono = $_;}
	if ($name eq "correo_electronico") {$_ = $value;s/\+/ /g;$correo_electronico = $_;}
	if ($name eq "lugar_y_fecha_de_nacimiento") {$_ = $value;s/\+/ /g;$lugar_y_fecha_de_nacimiento = $_;}
	if ($name eq "documento_de_identidad") {$_ = $value;s/\+/ /g;$documento_de_identidad = $_;}
	if ($name eq "primaria") {$_ = $value;s/\+/ /g;$primaria = $_;}
	if ($name eq "secundaria") {$_ = $value;s/\+/ /g;$secundaria = $_;}
	if ($name eq "superior") {$_ = $value;s/\+/ /g;$superior = $_;}

	if ($name eq "otros_estudios") {
		@t=split(/=/,$_);
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
#--------------------------------
#Validar usuario duplicado
$enc="no";
open(Farch,"curri.bd");
while(<Farch>) {
 $linea=$_;
 @lista=split(/\^/,$linea);
 $lg=@lista[0];
 if ($lg eq $login)  {
    $enc="si";
    last;
 }
}
close(Farch);
if ($enc eq 'si') {
 print "Sorry elige otro login porque $login ya existe";
}
else {
#Presentación de datos
#---------------------
$Web =<<_HTML_;
<html>
<head>
<title>Currículums</title>
<style>
<!--
td { border-bottom: 1px solid rgb(0,128,192) }
-->
</style>
</head>
<body link="#0080C0" vlink="#0080C0" alink="#0080C0">
<font face="Ms Sans Serif" size="2" color="#0080C0">
Por favor verifique que los datos ingresados en el currículum son correctos. 
Luego presione el botón <B>Aceptar datos ingresados</B> para grabarlos en nuestra base de datos. 
En caso contrario, pulse el botón <B>ATRAS</B> de su navegador para regresar y corrija lo que considere necesario.
</font>
<HR>
<h2 align="center"><font color="#0080C0"><big>$login</big></font></h2>
<h1 align="center"><font color="#0080C0"><big>$apellidos_y_nombres</big></font></h1>
<h2 align="center">Currículum vitae</h2>
<div align="center"><center>
<table border="0" width="600" cellspacing="0" cellpadding="5"
style="border-right: 2px none rgb(0,0,0)">
  <tr align="center">
    <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left"
    bgcolor="#0080C0"><font color="#FFFFFF" face="MS Sans Serif"><strong>Datos personales</strong></font></td>
  </tr>
  <tr align="center">
    <td width="100%" bgcolor="#FFFFFF"><div align="center"><center><table border="0"
    cellspacing="0" cellpadding="2" width="500">
      <tr>
        <td align="left" valign="top"><strong><small><font face="MS Sans Serif"><small>Dirección
        actual</small></font></small></strong></td>
        <td align="left"><font face="MS Sans Serif" size="3">$direccion_actual</font></td>
      </tr>
      <tr>
        <td align="left" valign="top"><strong><small><font face="MS Sans Serif"><small>Teléfono</small></font></small></strong></td>
        <td align="left"><font face="MS Sans Serif" size="3">$telefono</font></td>
      </tr>
      <tr>
        <td align="left" valign="top"><strong><small><font face="MS Sans Serif"><small>Correo
        electrónico</small></font></small></strong></td>
        <td align="left"><font face="MS Sans Serif" size="3">$correo_electronico</font></td>
      </tr>
      <tr>
        <td align="left" valign="top"><strong><small><font face="MS Sans Serif"><small>Lugar y
        fecha de nacimiento</small></font></small></strong></td>
        <td align="left"><font face="MS Sans Serif" size="3">$lugar_y_fecha_de_nacimiento</font></td>
      </tr>
      <tr>
        <td align="left" valign="top"><strong><small><font face="MS Sans Serif"><small>Documentos
        de Identidad</small></font></small></strong></td>
        <td align="left"><font face="MS Sans Serif" size="3">$documento_de_identidad</font></td>
      </tr>
    </table>
    </center></div></td>
  </tr>
  <tr align="center">
    <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left"
    bgcolor="#0080C0"><font color="#FFFFFF" face="MS Sans Serif"><strong>Formación</strong></font></td>
  </tr>
  <tr align="center">
    <td width="100%" bgcolor="#FFFFFF"><div align="center"><center><table border="0"
    cellspacing="0" cellpadding="2" width="500">
      <tr>
        <td valign="top" align="left"><small><strong><small><font face="MS Sans Serif">Primaria</font></small></strong></small></td>
        <td align="left" valign="middle"><font face="MS Sans Serif" size="3">$primaria</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><small><font face="MS Sans Serif">Secundaria</font></small></strong></small></td>
        <td align="left" valign="middle"><font face="MS Sans Serif" size="3">$secundaria</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><small><font face="MS Sans Serif">Superior</font></small></strong></small></td>
        <td align="left" valign="middle"><font face="MS Sans Serif" size="3">$superior</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><small><font face="MS Sans Serif">Otros
        estudios</font></small></strong></small></td>
        <td align="left" valign="middle"><font face="MS Sans Serif" size="3">$otros_estudios</font></td>
      </tr>
    </table>
    </center></div></td>
  </tr>
  <tr align="center">
    <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left"
    bgcolor="#0080C0"><font color="#FFFFFF" face="MS Sans Serif"><strong>Idiomas</strong></font></td>
  </tr>
  <tr align="center">
    <td width="100%" bgcolor="#FFFFFF"><div align="center"><center><table border="0"
    cellspacing="0" cellpadding="2" width="500">
      <tr>
        <td valign="top" align="left"><small><small><strong><font face="MS Sans Serif">Lengua
        nativa</font></strong></small></small></td>
        <td align="left"><font face="MS Sans Serif">$lengua_nativa</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><small><strong><font face="MS Sans Serif">Idioma 1</font></strong></small></small></td>
        <td align="left"><font face="MS Sans Serif">$idioma_1</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><small><strong><font face="MS Sans Serif">Idioma 2</font></strong></small></small></td>
        <td align="left"><font face="MS Sans Serif">$idioma_2</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><small><strong><font face="MS Sans Serif">Otros</font></strong></small></small></td>
        <td align="left"><font face="MS Sans Serif">$otro_idioma</font></td>
      </tr>
    </table>
    </center></div></td>
  </tr>
  <tr align="center">
    <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left"
    bgcolor="#0080C0"><font color="#FFFFFF" face="MS Sans Serif"><strong>Descripción
    profesional</strong></font></td>
  </tr>
  <tr align="center">
    <td width="100%" bgcolor="#FFFFFF"><div align="center"><center><table border="0"
    width="500" cellspacing="0" cellpadding="2">
      <tr>
        <td valign="top" align="left"><small><strong><font face="MS Sans Serif"><small>Experiencia laboral</small></font></strong></small></td>
        <td align="left"><font face="MS Sans Serif">$experiencia_laboral</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><small><font face="MS Sans Serif">Cursos y o Seminarios</font></small></strong></small></td>
        <td align="left"><font face="MS Sans Serif">$cursos_y_seminarios</font></td>
      </tr>
    </table>
    </center></div></td>
  </tr>
  <tr align="center">
    <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left"
    bgcolor="#0080C0"><font color="#FFFFFF" face="MS Sans Serif"><strong>Información general</strong></font></td>
  </tr>
  <tr align="center">
    <td width="100%" bgcolor="#FFFFFF" style="border-bottom: medium none"><div align="center"><center><table
    border="0" cellspacing="0" cellpadding="2" width="500">
      <tr>
        <td valign="top" align="left"><small><strong><font face="MS Sans Serif"><small>Software
        que maneja</small></font></strong></small></td>
        <td align="left"><font face="MS Sans Serif" size="3">$software_que_maneja</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><font face="MS Sans Serif"><small>Hobbies</small></font></strong></small></td>
        <td align="left"><font face="MS Sans Serif" size="3">$hobbies</font></td>
      </tr>
      <tr>
        <td valign="top" align="left"><small><strong><font face="MS Sans Serif"><small>Intereses
        profesionales</small></font></strong></small></td>
        <td align="left"><font face="MS Sans Serif" size="3">$intereses_profesionales</font></td>
      </tr>
    </table>
    </center></div></td>
  </tr>
</table>
</center></div>

<FORM ACTION="../cgi-bin/preview.pl" METHOD="POST">
	<INPUT TYPE="hidden" NAME="login" VALUE="$login">
	<INPUT TYPE="hidden" NAME="paswd" VALUE="$paswd">
	<INPUT TYPE="hidden" NAME="situacion" VALUE="nuevo_curriculo">
	<INPUT TYPE="hidden" NAME="apellidos_y_nombres" VALUE="$apellidos_y_nombres">
	<INPUT TYPE="hidden" NAME="direccion_actual" VALUE="$direccion_actual">
	<INPUT TYPE="hidden" NAME="telefono" VALUE="$telefono">
	<INPUT TYPE="hidden" NAME="correo_electronico" VALUE="$correo_electronico">
	<INPUT TYPE="hidden" NAME="lugar_y_fecha_de_nacimiento" VALUE="$lugar_y_fecha_de_nacimiento">
	<INPUT TYPE="hidden" NAME="documento_de_identidad" VALUE="$documento_de_identidad">
	<INPUT TYPE="hidden" NAME="primaria" VALUE="$primaria">
	<INPUT TYPE="hidden" NAME="secundaria" VALUE="$secundaria">
	<INPUT TYPE="hidden" NAME="superior" VALUE="$superior">
	<INPUT TYPE="hidden" NAME="otros_estudios" VALUE="$otros_estudios">
	<INPUT TYPE="hidden" NAME="lengua_nativa" VALUE="$lengua_nativa">
	<INPUT TYPE="hidden" NAME="idioma_1" VALUE="$idioma_1">
	<INPUT TYPE="hidden" NAME="idioma_2" VALUE="$idioma_2">
	<INPUT TYPE="hidden" NAME="otro_idioma" VALUE="$otro_idioma">
	<INPUT TYPE="hidden" NAME="experiencia_laboral" VALUE="$experiencia_laboral">
	<INPUT TYPE="hidden" NAME="cursos_y_seminarios" VALUE="$cursos_y_seminarios">
	<INPUT TYPE="hidden" NAME="software_que_maneja" VALUE="$software_que_maneja">
	<INPUT TYPE="hidden" NAME="hobbies" VALUE="$hobbies">
	<INPUT TYPE="hidden" NAME="intereses_profesionales" VALUE="$intereses_profesionales">
	<CENTER>
		<INPUT TYPE="submit" VALUE="Aceptar datos ingresados" style="background-color: #0080C0; color: #FFFFFF; font-family: MS Sans Serif; border: 2 outset #000080; padding: 3">
	</CENTER>	
</FORM>

<hr align="center" width="80%" noshade size="5" color="#0080C0">
<div align="center"><center>
<table border="0" width="75%" bgcolor="#C0C0C0" cellspacing="0" cellpadding="5">
  <tr>
    <td width="100%" bgcolor="#0080C0"><p align="left"><font color="#FFFFFF"
    face="MS Sans Serif"><small><small>Este es un servicio gratuito de<strong> <a
    href="http://pdeinfo.com" target="_blank" style="color: rgb(255,255,255)">Punto de
    Información</a></strong></small></small></font></p>
    <blockquote>
      <blockquote>
        <blockquote>
          <p align="center"><font color="#FFFFFF" face="MS Sans Serif"><small><small>Aunque Punto de
          Información hace un esfuerzo por validar la información que se presenta en estas
          páginas, no es responsable por errores u omisiones incluidos en estas. </small></small></font></p>
        </blockquote>
      </blockquote>
    </blockquote>
    <blockquote>
      <p align="right"><font color="#FFFFFF" face="MS Sans Serif"><small><small>Todos los
      derechos reservados - Sistemas PdeInfo - 1999</small></small></font></p>
    </blockquote>
    </td>
  </tr>
</table>
</center></div>
<blockquote>
  <hr align="center">
</blockquote>
</body>
</html>
_HTML_


print $Web;
}