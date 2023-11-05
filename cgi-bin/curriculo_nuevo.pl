#!/usr/local/bin/perl
require "curriculo_configuracion.pl";

read(STDIN,$input,$ENV{CONTENT_LENGTH});
print("Content-Type: text/html\n\n");
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
    $datos{$nombre}=$valor;
}

$Web =<<HTML;
<html><head>
<meta name='GENERATOR' content='Microsoft FrontPage 4.0'>
<meta name='ProgId' content='FrontPage.Editor.Document'>
<title>Currículos en PdeInfo</title>
<style>
.celda1      { border-right: 2 solid #993366; border-top: 1 solid #993366 }
.celda2      { border-left: 1 solid #993366; border-right: 2 solid #993366; 
               border-top: 1 solid #993366; border-bottom: 2 solid #993366 }
</style>
<meta name='Microsoft Theme' content='sumipntg 111, default'>
</head>
<body background='../_themes/sumipntg/sumtextb.jpg' bgcolor='#FFFFCC' text='#000066' link='#660099' vlink='#993366' alink='#6666CC'><font face='Verdana, Arial, Helvetica'>
<h1><font color='#993366'>Currículos en PdeInfo</font></h1>
<p>La siguiente información ha sido ingresada al sistema. Por favor sírvase
verificarla cuidadosamente. Si hay algún dato incorrecto, puede regresar a la
pantalla anterior y corregirlo. Pulse el botón de <b>Enviar la Información</b>
para grabar sus datos.</p>
<form method='POST' action='curriculo_grabar.pl'>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Datos de la cuenta</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <center>
  </font><table border='0' cellspacing='5' cellpadding='2' width='500'>
    <tr>
      <td valign='middle' style='border-right: 2 solid #993366; border-top: 1 solid #993366' width='40%'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Login</b></font></font></td>
      <td align='left' valign='top' width='60%'><font face='Verdana, Arial, Helvetica'>
        <p align='left'><font size='2'>$datos{login}</font></p>
      </font></td>
    </tr>
    <tr>
      <td valign='middle' style='border-right: 2 solid #993366; border-top: 1 solid #993366' width='40%'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Contraseña</b></font></font></td>
      <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>No se muestra</font></font></td>
    </tr>
  </table><font face='Verdana, Arial, Helvetica'>
  </center>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Datos personales</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <center>
  </font><table border='0' cellspacing='5' cellpadding='2' width='500'>
    <tr>
      <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Nombres</b></font></font></td>
      <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{nombre}</font></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Apellido
        Paterno</b></font></font></td>
      <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{ap_paterno}</font></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Apellido
        Materno</b></font></font></td>
      <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{ap_materno}</font></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Documento
        de Identidad</b></font></font></td>
    </center>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{identidad}</font></font></td>
  </tr>
  <center>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Género</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{genero}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Dirección
      actual</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{direccion}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Ciudad
      de residencia</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{ciudad}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Departamento</b></font></font></td>
  </center>
  <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{departamento}</font></font></td>
  </tr>
  <center>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Teléfono</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'></center><font size='2'>$datos{telefono1} -
    $datos{telefono2}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Correo
      electrónico</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{email}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Fecha
      de Nacimiento</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{dia} de $datos{mes} de
      $datos{ano}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>País
      de nacimiento</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{pais}</font></font></td>
  </tr>
  </table><font face='Verdana, Arial, Helvetica'>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Formación</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <center>
  </font><table border='0' cellspacing='5' cellpadding='2' width='500'>
    <tr>
      <td valign='top' colspan='2' width='40%'><font face='Verdana, Arial, Helvetica'><b><font size='2' color='#663399'>Superior</font></b></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Nivel</b></font></font></td>
    </center>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{superior_nivel}</font></font></td>
  </tr>
  <center>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Área
      de estudios</b></font></font></td>
  </center>
  <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{superior_area}</font></font></td>
  </tr>
  <center>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Centro
      de Estudios</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{superior_centro}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Último
      año cursado</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{superior_ano}</font></font></td>
  </tr>
  <tr>
    <td valign='top' colspan='2' width='40%'><font face='Verdana, Arial, Helvetica'><b><font size='2' color='#663399'>Secundaria</font></b></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Centro
      de estudios</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{secundaria_centro}</font></font></td>
  </tr>
  <tr>
    <td valign='middle' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Último
      año cursado</b></font></font></td>
    <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{secundaria_ano}</font></font></td>
  </tr>
  <tr>
    <td valign='top' colspan='2' width='40%'><font face='Verdana, Arial, Helvetica'><b><font size='2' color='#663399'>Otros
      estudios</font></b></font></td>
  </tr>
  <tr>
    <td valign='top' width='40%' style='border-right: 2 solid #993366; border-top: 1 solid #993366'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Sírvase
      indicar</b></font></font></td>
  </center>
  <td align='left' width='60%'><font face='Verdana, Arial, Helvetica'>
    <p align='left'><font size='2'>$datos{otros_estudios}</font></font></td>
  </tr>
  </table><font face='Verdana, Arial, Helvetica'>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Idiomas</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <center>
  </font><table border='0' cellspacing='5' cellpadding='2' width='500'>
    <tr>
      <td valign='middle' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Idioma 1</b></font></font></td>
      <td align='left' valign='middle' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{idioma1}
        </font><font size='2'>$datos{nivel1}</font></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Idioma 2</b></font></font></td>
      <td align='left' valign='middle' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{idioma2}
        $datos{nivel2}</font></font></td>
    </tr>
    <tr>
      <td valign='middle' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Otros</b></font></font></td>
      <td align='left' valign='middle' width='60%'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{otro_idioma}</font></font></td>
    </tr>
  </table><font face='Verdana, Arial, Helvetica'>
  </center>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Descripción profesional</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <div align='center'>
    <center>
    </font><table border='0' cellspacing='5' cellpadding='2' width='500'>
      <tr>
        <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Experiencia
          laboral</b></font></font></td>
      </center>
      <td align='center' valign='top' width='60%' class='celda2'><font face='Verdana, Arial, Helvetica'>
        <p align='left'><font face='Tahoma' color='#993366' size='1'>Años de
        experiencia:</font><font size='2'> $datos{experiencia_anos}<br>
        <br>
        </font><font color='#993366' face='Arial' size='1'>Descripción de la
        experiencia laboral</font><font size='2'><br>
        $datos{experiencia}</font></p>
      </font></td>
    </tr>
    <center>
    <tr>
      <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Cursos y/o
        Seminarios</b></font></font></td>
    </center>
    <td align='center' valign='top' width='60%' class='celda2'><font face='Verdana, Arial, Helvetica'>
      <p align='left'><font size='2'>$datos{cursos}</font></p>
    </font></td>
    </tr>
    <center>
    <tr>
      <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><font size='1'><b>Disponibilidad</b></font></font></td>
    </center>
    <td align='center' valign='top' width='60%'><font face='Verdana, Arial, Helvetica'>
      <p align='left'><font size='2'>$datos{disponibilidad}</font></font></td>
    </tr>
    </table><font face='Verdana, Arial, Helvetica'>
  </div>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <div align='center'>
    <center>
    </font><table border='0' width='600' bgcolor='#663399' cellspacing='0' cellpadding='5'>
      <tr>
        <td width='100%'><font face='Verdana, Arial, Helvetica'><b><font color='#FFFFFF'>Información general</font></b></font></td>
      </tr>
    </table><font face='Verdana, Arial, Helvetica'>
    </center>
  </div>
  <center>
  </font><table border='0' width='500' cellspacing='5' cellpadding='2'>
    <tr>
      <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><b><font size='1'>Software que
        maneja</font></b></font></td>
      <td valign='top' width='60%' class='celda2'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{software}</font></font></td>
    </tr>
    <tr>
      <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><b><font size='1'>Hobbies</font></b></font></td>
      <td valign='top' width='60%' class='celda2'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{hobbies}</font></font></td>
    </tr>
    <tr>
      <td valign='top' width='40%' class='celda1'><font face='Verdana, Arial, Helvetica'><b><font size='1'>Intereses
        profesionales</font></b></font></td>
      <td valign='top' width='60%' class='celda2'><font face='Verdana, Arial, Helvetica'><font size='2'>$datos{intereses}</font></font></td>
    </tr>
  </table><font face='Verdana, Arial, Helvetica'>
  </center>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
  <p align='center'><input type='submit' value='Enviar la información' name='btnEnviar' style='font-family: Tahoma; font-size: 10 pt; color: #FFFFFF; font-weight: bold; background-color: #663399; border: 2 outset #663399; padding: 2'></p>
  <!--msthemeseparator--><p align='center'><img src='../_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>
HTML

print $Web;

foreach $campo(@campos){
print "<input type='hidden' name='$campo' value='$datos{$campo}'>\n";
}

print "</form></font></body></html>";