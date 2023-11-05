#!usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
    $fields{$name}=$value;
#Tratamiento de los datos
#------------------------

	if ($name eq "login") {$_ = $value;s/\+/ /g;$login = $_;}
	if ($name eq "paswd") {$_ = $value;s/\+/ /g;$paswd = $_;}
}

$directorio="/www/pdeinfo/base";
$basedatos="curri.bd";

open(Farch,"$basedatos");
$enc="no";
while(<Farch>) {
 $linea=$_;
 @lista=split(/\^/,$linea);
 $lg=@lista[0];
 $pw=@lista[1];
 if (($lg eq $login) && ($pw eq $paswd)) {
    $enc="si";
    last;
 }
}
close(Farch);
if ($enc eq "no"){
 print ("Content-Type: text/html\n\n");
 print ("<body bgcolor=#ffffcc>\n");
 print "Sorry $login ";
 }
else {
 #print ("Content-Type: text/html\n\n");
 #print ("<body bgcolor=#ffffcc>\n");
 #print ("<H3>Welcome $login </H3>\n");
 #Mostrar Form
 $apellidos_y_nombres=@lista[2];
 $direccion_actual=@lista[3];
 $telefono=@lista[4];
 $correo_electronico=@lista[5];
 $lugar_y_fecha_de_nacimiento=@lista[6];
 $documento_de_identidad=@lista[7];
 $primaria=@lista[8];
 $secundaria=@lista[9];
 $superior=@lista[10];
 $otros_estudios=@lista[11];
 @lis=split(/<br>/,$otros_estudios);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $otros_estudios=$a;
 $lengua_nativa=@lista[12];
 $idioma_1=@lista[13];
 $idioma_2=@lista[14];
 $otro_idioma=@lista[15];
 $experiencia_laboral=@lista[16];
 @lis=split(/<br>/,$experiencia_laboral);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $experiencia_laboral=$a;
 $cursos_y_seminarios=@lista[17];
 @lis=split(/<br>/,$cursos_y_seminarios);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $cursos_y_seminarios=$a;
 $software_que_maneja=@lista[18];
 @lis=split(/<br>/,$software_que_maneja);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $software_que_maneja=$a;
 $hobbies=@lista[19];
 @lis=split(/<br>/,$hobbies);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $hobbies=$a;
 $intereses_profesionales=@lista[20];	
 @lis=split(/<br>/,$intereses_profesionales);
 $a='';
 foreach(@lis){
  if($_ eq ''){
  }
  else {
  	$a=$a."$_\n";
  }
 }
 $intereses_profesionales=$a;
 @masias=("Español","Ingles","Francés","Alemán","Italiano","Japonés","Otro");
 @leng=("","","","","","");
 @leng1=("","","","","","");
 @leng2=("","","","","","");
 $i=0;
 foreach(@masias){
 if($_ eq $lengua_nativa) {
	@leng[$i]="SELECTED";
 }
 $i++;
 } 

 $i=0;
 foreach(@masias){
 if($_ eq $idioma_1) {
	@leng1[$i]="SELECTED";
 }
 $i++;
 } 

 $i=0;
 foreach(@masias){
 if($_ eq $idioma_2) {
	@leng2[$i]="SELECTED";
 }
 $i++;
 } 

$Web =<<_HTML_;
<html>
<head>
<title>Ingreso de información</title>
<meta name="GENERATOR" content="Microsoft FrontPage 4.0">
<meta name="Microsoft Theme" content="sumipntg 111, default">
</head>
<body background="_themes/sumipntg/sumtextb.jpg" bgcolor="#FFFFCC" text="#000066" link="#660099" vlink="#993366" alink="#6666CC"><!--mstheme--><font face="Verdana, Arial, Helvetica">
<p>
</p>
<p>Para actualizar los datos de tu currículo usa el siguiente formulario:</p>
<hr align="center">
<form method="POST" action="../cgi-bin/preview.pl" name="FrontPage_Form1">
  <div align="center"><center><table border="0" width="600" cellspacing="0" cellpadding="5" style="border-right: 2px none rgb(0,0,0)">
    <tr>
      <td width="50%" style="border-right-style: none; border-right-width: medium; border-bottom: 1px solid rgb(0,0,0)" bgcolor="#000000"><font color="#FFFFFF">Login</font></td>
    </tr>
  </center>
    <tr>
      <td width="50%" bgcolor="#FFFFFF" align="left"><INPUT TYPE="hidden" NAME="situacion" VALUE="edita_curriculo">
        <p align="left">$login<input type="hidden" name="login" value='$login' size="17" style="font-family: Tahoma, Verdana; font-size: 14pt; text-align: center; background-color: rgb(190,190,255); border: 2 dashed rgb(0,0,255); margin: 2px"></td>
    </tr>
    <center>
    <tr>
      <td width="100%" style="border-right: medium none; border-bottom: 1px solid rgb(0,0,0)" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;Sus apellidos y nombres.&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" width="17" height="23"></a><font color="#FFFFFF">Apellidos
      y nombres</font></td>
    </tr>
    <tr>
      <td width="100%" bgcolor="#FFFFFF" style="border-left: 1px none rgb(0,0,0); border-right: 2px none rgb(0,0,0); border-top: 1px none rgb(0,0,0); border-bottom: 2px none rgb(0,0,0)"><div align="center"><p><input type="text" name="apellidos_y_nombres" value='$apellidos_y_nombres' size="60" style="font-family: Tahoma, Verdana; font-size: 14pt; text-align: center; background-color: rgb(190,190,255); border: 2 dashed rgb(0,0,255); margin: 2px">
        </div>
      </td>
    </tr>
    <tr align="center">
      <td width="100%">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;Los datos personales serán los que le permiten que alguna persona interesada pueda ubicarlo.&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" WIDTH="17" HEIGHT="23"></a><font color="#FFFFFF">Datos
      personales</font></td>
    </tr>
    <tr align="center">
      <td width="100%" bgcolor="#FFFFFF"><div align="right"><table border="0" cellspacing="0" cellpadding="2">
        <tr>
          <td style="border-bottom: 1px outset rgb(0,128,192)"><small>Dirección actual</small></td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><div align="right"><p><input type="text" name="direccion_actual" value='$direccion_actual' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">
            </div>
          </td>
        </tr>
        <tr>
          <td style="border-bottom: 1px outset rgb(0,128,192)"><small>Teléfono</small></td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="telefono" value='$telefono' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td style="border-bottom: 1px outset rgb(0,128,192)"><small>Correo electrónico</small></td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="correo_electronico" value='$correo_electronico' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td style="border-bottom: 1px outset rgb(0,128,192)"><small>Lugar y fecha de nacimiento</small></td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="lugar_y_fecha_de_nacimiento" size="60" value='$lugar_y_fecha_de_nacimiento' style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td style="border-bottom: 1px outset rgb(0,128,192)"><small>Documentos de Identidad</small></td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="documento_de_identidad" value='$documento_de_identidad' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
      </table>
      </div></td>
    </tr>
    <tr align="center">
      <td width="100%">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;La formación profesional indica los colegios en que ha estudiado, la carrera superior que ha seguido y otras carreras adicionales que pueda haber completado. Para estos datos, es importante tambien indicar las fechas en las que se realizaron los mismos.&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" WIDTH="17" HEIGHT="23"></a><font color="#FFFFFF">Formación</font></td>
    </tr>
    <tr align="center">
      <td width="100%" bgcolor="#FFFFFF"><div align="right"><table border="0" cellspacing="0" cellpadding="2">
        <tr>
          <td width="100%" style="border-bottom: 1px outset rgb(0,128,192)">Primaria</td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="primaria" value='$primaria' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td width="100%" style="border-bottom: 1px outset rgb(0,128,192)">Secundaria</td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="secundaria" value='$secundaria' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td width="100%" style="border-bottom: 1px outset rgb(0,128,192)">Superior</td>
          <td align="right" style="border-bottom: 1px outset rgb(0,128,192)"><input type="text" name="superior" value='$superior' size="60" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
        <tr>
          <td width="100%" style="border-bottom: 1px outset rgb(0,128,192)">Otros estudios</td>
          <td align="left" valign="bottom" style="border-bottom: 1px outset rgb(0,128,192)"><textarea rows="10" name="otros_estudios"  cols="60" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$otros_estudios</textarea></td>
        </tr>
      </table>
      </div></td>
    </tr>
    <tr align="center">
      <td width="100%">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" WIDTH="17" HEIGHT="23"></a><font color="#FFFFFF">Idiomas</font></td>
    </tr>
    <tr align="center">
      <td width="100%" bgcolor="#FFFFFF"><table border="0" width="100%" cellspacing="0" cellpadding="2">
        <tr>
          <td align="center"><small>Lengua nativa</small><br>
          <select name="lengua_nativa" size="1" style="background-color: rgb(190,190,255); border: 2 dashed rgb(0,0,255); padding: 2">
            <option value="Español"  @leng[0] >Español</option>
            <option value="Ingles" @leng[1] >Ingles</option>
            <option value="Francés" @leng[2] >Francés</option>
            <option value="Alemán" @leng[3] >Alemán</option>
            <option value="Italiano" @leng[4] >Italiano</option>
            <option value="Japonés" @leng[5] >Japonés</option>
            <option value="Otro" @leng[6] >Otro</option>
          </select></td>
          <td align="center"><small>Idioma 1</small><br>
          <select name="idioma_1" size="1" style="background-color: rgb(190,190,255); border: 2 dashed rgb(0,0,255); padding: 2">
            <option value="Español" @leng1[0] >Español</option>
            <option value="Ingles" @leng1[1]>Ingles</option>
            <option value="Francés" @leng1[2]>Francés</option>
            <option value="Alemán" @leng1[3]>Alemán</option>
            <option value="Italiano" @leng1[4]>Italiano</option>
            <option value="Japonés" @leng1[5]>Japonés</option>
            <option value="Otro" @leng1[6]>Otro</option>
          </select></td>
          <td align="center"><small>Idioma 2</small><br>
          <select name="idioma_2" size="1" style="background-color: rgb(190,190,255); border: 2 dashed rgb(0,0,255); padding: 2">
            <option value="Español" @leng2[0]>Español</option>
            <option value="Ingles" @leng2[1]>Ingles</option>
            <option value="Francés" @leng2[2]>Francés</option>
            <option value="Alemán" @leng2[3]>Alemán</option>
            <option value="Italiano" @leng2[4]>Italiano</option>
            <option value="Japonés" @leng2[5]>Japonés</option>
            <option value="Otro" @leng2[6]>Otro</option>
          </select></td>
          <td align="center"><small>Otros (sírvase especificar)</small><br>
            <input type="text" name="otro_idioma" value='$otro_idioma' size="20" style="background-color: rgb(190,190,255); text-align: right; font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2"></td>
        </tr>
      </table></td>
    </tr>
    <tr align="center">
      <td width="100%">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;La experiencia laboral se refiere a los trabajos en los que Ud. se ha desempeñado (sean trabajos o practicas pre-profesionales). En cuanto a los cursos, coloque aqui todos aquellos eventos en los que ha participado que no puedan considerarse como estudios por si mismos. En ambos casos, ayuda mucho indicar las fechas en que se desarrollaron los mismos.&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" WIDTH="17" HEIGHT="23"></a><font color="#FFFFFF">Descripción
      profesional</font></td>
    </tr>
    <tr align="center">
      <td width="100%" bgcolor="#FFFFFF"><div align="center"><table border="0" cellspacing="0" cellpadding="5">
        <tr>
          <td width="50%" align="left"><small>Experiencia laboral</small></td>
          <td width="50%" align="left" style="border-left: 2px outset rgb(0,128,192)"><small>Cursos
          y/o Seminarios</small></td>
        </tr>
        <tr>
          <td width="50%"><div align="right"><p><textarea rows="10" name="experiencia_laboral" cols="37" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$experiencia_laboral</textarea>
            </div>
          </td>
          <td width="50%" style="border-left: 2px outset rgb(0,128,192)"><div align="right"><p><textarea rows="10" name="cursos_y_seminarios" cols="37" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$cursos_y_seminarios</textarea>
            </div>
          </td>
        </tr>
      </table></div></td>
    </tr>
    <tr align="center">
      <td width="100%">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)" align="left" bgcolor="#000000"><a href="JavaScript:hhctrl.TextPopup(&quot;Esta información permite terminar de describirlo profesionalmente. Usela para terminar de guiar a las personas que puedan estar leyendo su curriculo, para que conozcan hacia adonde quiere usted apuntar profesionalmente.&quot;,&quot;Tahoma,10&quot;,9,9,-1,-1)"><img src="images/ayuda.GIF" border="0" hspace="2" align="absbottom" WIDTH="17" HEIGHT="23"></a><font color="#FFFFFF">Información
      general</font></td>
    </tr>
    <tr align="center">
      <td width="100%" bgcolor="#FFFFFF"><table border="0" cellspacing="0" cellpadding="2">
        <tr>
          <td style="border-right: medium none"><small>Software que maneja</small></td>
          <td style="border-left: 2px ridge rgb(0,128,192); border-right: 2px ridge rgb(0,128,192)"><small>Hobbies</small></td>
          <td><small>Intereses profesionales</small></td>
        </tr>
        <tr>
          <td align="center" style="border-right: medium none"><textarea rows="10" name="software_que_maneja" cols="25" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$software_que_maneja</textarea></td>
          <td align="center" style="border-left: 2px ridge rgb(0,128,192); border-right: 2px ridge rgb(0,128,192)"><textarea rows="10" name="hobbies" cols="25" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$hobbies</textarea></td>
          <td align="center"><textarea rows="10" name="intereses_profesionales" cols="25" style="background-color: rgb(190,190,255); font-family: Tahoma; border: 2 dashed rgb(0,0,255); padding: 2">$intereses_profesionales</textarea></td>
        </tr>
      </table></td>
    </tr>
    <tr align="center">
      <td width="100%" style="border-bottom: 1px solid rgb(0,0,0)">
        <hr align="center">
      </td>
    </tr>
    <tr align="center">
      <td width="100%"></td>
    </tr>
    <tr align="center">
      <td width="100%"><div align="center"><p><input type="submit" value="Actualizar" name="btnEnviar">
        </div>
      </td>
    </tr>
  </table>
  </center></div>	<INPUT TYPE="hidden" NAME="situacion" VALUE="edita_curriculo">
</form>
<hr align="center">
<p align="center">Este es un servicio gratuito de <a href="http://pdeinfo.com" target="_blank">Punto de Información</a></p>
<blockquote>
  <p><small>Aunque Punto de Información hace un esfuerzo por validar la información que se
  presenta en estas páginas, no es responsable por errores u omisiones incluidos en estas. </small></p>
  <p><small><br>
  Todos los derechos reservados - Sistemas PdeInfo - 1999</small></p>
  <hr align="center">
</blockquote>
<p align="center">&nbsp;</body>
</html>
_HTML_

print $Web;
}