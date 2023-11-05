#!/usr/local/bin/perl
#---------------------------------------------------
#--->>>Revisado por Manolo 09:20 p.m. 23/12/99<<<---
#---------------------------------------------------

$criterio_a_buscar = $ENV{"QUERY_STRING"};
$criterio_a_buscar =~ tr/a-z/A-Z/;
# ----------------------------
# Busqueda en la base de datos
# ----------------------------
$encontrado="";
open(Farch,"curri.bd");
while(<Farch>) {
	$linea = $_;
	@linea = split(/\^/,$linea);
	$linea_donde_buscar = $linea[0];
	$linea_donde_buscar =~ tr/a-z/A-Z/;
	if ($linea_donde_buscar eq $criterio_a_buscar) {
		$encontrado=$linea;
		last;
	}
}
close(Farch);

if ($encontrado eq ""){
print ("Content-Type: text/html\n\n");
print "No se encontro ninguno";
}
else
{
	# --------------------------------------------
	# $encontrado contiene lo que queremos mostrar
	# --------------------------------------------
	@tmp= split(/\^/,$encontrado); 
	#Tratamiento de los datos
	$apellidos_y_nombres = @tmp[2];
	$direccion_actual = @tmp[3];
	$telefono = @tmp[4];
	$correo_electronico = @tmp[5];
	$lugar_y_fecha_de_nacimiento = @tmp[6];
	$documento_de_identidad = @tmp[7];
	$primaria = @tmp[8];
	$secundaria = @tmp[9];
	$superior = @tmp[10];
	$otros_estudios =@tmp[11];
	$lengua_nativa = @tmp[12];
	$idioma_1 = @tmp[13];
	$idioma_2 = @tmp[14];
	$otro_idioma = @tmp[15];
	$cursos_y_seminarios = @tmp[16];
	$experiencia_laboral = @tmp[17];
	$software_que_maneja = @tmp[18];
	$hobbies = @tmp[19];
	$intereses_profesionales = @tmp[20];

	# Impresion

$Web =<<_HTML_;
<html><head><title>Currículums</title>
	<style>
	<!--
	td { border-bottom: 1px solid rgb(0,128,192) }
	-->
	</style>
	</head>
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
	
	print ("Content-Type: text/html\n\n");
	print $Web;
}