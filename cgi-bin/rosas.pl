#!/usr/local/bin/perl
#---------------------------------------------------
#--->>>Revisado por Manolo 09:25 p.m. 23/12/99<<<---
#---------------------------------------------------
$SEND_MAIL="/usr/sbin/sendmail -t";
read(STDIN, $save_string, $ENV{CONTENT_LENGTH});  # Yes- Use it
# separa la cadena de caracteres en una lista
@prompts = split(/&/,$save_string);
# recorre la lista
foreach (@prompts) {
    # separa el par nombre=valor
    ($name,$value) = split(/=/,$_);
    # decodifica los nombres
    $name =~   s/\%(..)/pack("c",hex($1))/ge;
    # decodifica valores
    $value =~ tr/+/ /;
    $value =~  s/\%(..)/pack("c",hex($1))/ge;
    # crea una lista asociativa     
    $fields{$name}=$value;
}
# cabecera HTTP
#$fields{}

$Web = <<_HTML_;
Content-Type: text/html\n\n
<HEAD><TITLE>Resultados</TITLE>
<style>
<!--
a:link       { text-decoration: none }
a:visited    { text-decoration: none }
a:hover      { text-decoration: underline }
-->
</style>
</HEAD><body>
<table border='0' width='100%' cellspacing='0' cellpadding='0'><tr>
<td width='50%'><img border='0' src='../rosas/images/roseslove.gif' align='center' width='238' height='70'></td>
<td width='50%'><div align='right'>
<table border='0' width='100%' cellspacing='0' cellpadding='2'>
<tr>
<td width='52'><b><font face='MS Sans Serif' size='1'><a href='/'><img border='0' src='../rosas/images/logo.gif' width='52' height='51'></a></font></b></td>
<td valign='top' width='100%'>
<p align='left'><b><font color='#FF9933' size='4' face='Tahoma'>Punto
de Información</font><font face='MS Sans Serif' size='3' color='#FF9933'><br>
</font></b><font face='MS Sans Serif' size='1' color='#FF9933'><b>Soluciones
creativas en el Web<br>
</b></font><font face='MS Sans Serif' size='1' color='#000000'>http://pdeinfo.com</font></td>
</tr><tr>
<td colspan='2' bgcolor='#FFEAA4' style='border-top: 1 solid #FF9933; border-bottom: 2 solid #FF9933'>
<p align='center'><font face='MS Sans Serif' size='1'><a href='../anuncios'><font color='#000000'>anuncios</font></a>
 | <a href='../curriculos'><font color='#000000'>currículos</font></a>
 | <a href='../web'><font color='#000000'>web</font></a> | <a href='../email'><font color='#000000'>e-mail</font></a>
 | <a href='../listas'><font color='#000000'>listas de
 interés</font></a> | <a href='../novedades'><font color='#000000'>novedades</font></a>
 | <a href='../postales'><font color='#000000'>postales</font></a></font></td>
</tr></table></div></td></tr><tr>
<td width='100%' colspan='2' style='border-bottom: 1 solid #FFCCCC'>
<p align='center'><font color='#CC3300' size='7'><b><i>Rosas online</i></b></font></td>
</tr></table>
<font face='Tahoma' size='3' color='#CC3300'><B>Se ha recepcionado el siguiente pedido</B></font>
<font face='Tahoma' size='2'><P>Entregar <B>$fields{numero}</B> rosas de color <B>$fields{color_rosas}</B>,
estilo <B>$fields{estilo}</B>, con un lazo de color <B>$fields{color_lazo}</B> a 
<B>$fields{entrega_nombre}</B>, con domicilio en <B>$fields{entrega_direccion}</B>, el 
<B>$fields{entrega_fecha}</B> a las <B>$fields{entrega_hora}</B>, con el siguiente mensaje 
en la tarjeta:
<hr size="1" color="#CC3300">
<h2>Mensaje</h2>
<table border=1 cellspacing=2>
<tr><td>De</td><td>$fields{de}</td></tr>
<tr><td>Para</td><td>$fields{para}</td></tr>
<tr><td>Mensaje</td><td>$fields{mensaje}</td></tr>
</table>
<h2>Datos de cobranza</h2>
<table border=1 cellspacing=2>
<tr><td>Nombre</td><td>$fields{envia_nombre}</td></tr>
<tr><td>Direccion</td><td>$fields{envia_direccion}</td></tr>
<tr><td>Telefono</td><td>$fields{envia_telefono}</td></tr>
</table>
<hr size="2" color="#CC3300">
<table border='0' width='100%' cellpadding='0'>
<tr>
<td width='33%' rowspan='2'><a href='../rosas/cajas.htm' class='info'><font face='MS Sans Serif' size='2' color='#CC3300'><b>Rosas
 en cajas decoradas</b></font></a></td>
<td width='17%'>
<p align='right'><font face='MS Sans Serif' size='2' color='#CC3300'>Arreglos<b>:</b></font></td>
<td width='16%'><font face='MS Sans Serif' size='2' color='#CC3300'><b>&nbsp;</b></font><a href='../rosas/arreglos_canastas.htm' class='info'><font face='MS Sans Serif' size='2' color='#CC3300'><b>Canastas</b></font></a></td>
<td width='34%' rowspan='2'>
<p align='right'><a href='../rosas/decoraciones.htm' class='info'><font face='MS Sans Serif' size='2' color='#CC3300'><b>Decoraciones
 para reuniones</b></font></a></td>
</tr>
<tr>
<td width='17%'></td>
<td width='16%'><font face='MS Sans Serif' size='2' color='#CC3300'><b>&nbsp;</b></font><a href='../rosas/arreglos_ceramicas.htm' class='info'><font face='MS Sans Serif' size='2' color='#CC3300'><b>Cerámicas</b></font></a></td>
</tr>
</table>
</body>
_HTML_

$email = <<_email_;
Entregar $fields{numero} rosas de color $fields{color_rosas}
estilo $fields{estilo}, con un lazo de color $fields{color_lazo}
A $fields{entrega_nombre}, con domicilio en $fields{entrega_direccion}, 
DIA: $fields{entrega_fecha}
HORA: $fields{entrega_hora}
-------
Mensaje
-------
De: $fields{de}
Para: $fields{para}
Mensaje:
$fields{mensaje}
-----------------
Datos de cobranza
-----------------
Nombre: $fields{envia_nombre}
Direccion: $fields{envia_direccion}
Telefono: $fields{envia_telefono}
_email_


print "$Web";



&sendmail("rosas\@pdeinfo.com", "", "rosas\@pdeinfo.com", $smtp, "ROSAS", $email );




###################################################################
#Sendmail.pm routine below by Milivoj Ivkovic 
###################################################################
sub sendmail  {

# error codes below for those who bother to check result codes <gr>

# 1 success
# -1 $smtphost unknown
# -2 socket() failed
# -3 connect() failed
# -4 service not available
# -5 unspecified communication error
# -6 local user $to unknown on host $smtp
# -7 transmission of message failed
# -8 argument $to empty
#
#  Sample call:
#
# &sendmail($from, $reply, $to, $smtp, $subject, $message );
#
#  Note that there are several commands for cleaning up possible bad inputs - if you
#  are hard coding things from a library file, so of those are unnecesssary
#

    my ($fromaddr, $replyaddr, $to, $smtp, $subject, $message) = @_;

    $to =~ s/[ \t]+/, /g; # pack spaces and add comma
    $fromaddr =~ s/.*<([^\s]*?)>/$1/; # get from email address
    $replyaddr =~ s/.*<([^\s]*?)>/$1/; # get reply email address
    $replyaddr =~ s/^([^\s]+).*/$1/; # use first address
    $message =~ s/^\./\.\./gm; # handle . as first character
    $message =~ s/\r\n/\n/g; # handle line ending
    $message =~ s/\n/\r\n/g;
    $smtp =~ s/^\s+//g; # remove spaces around $smtp
    $smtp =~ s/\s+$//g;

    if (!$to)
    {
	return(-8);
    }

 if ($SMTP_SERVER ne "")
  {
    my($proto) = (getprotobyname('tcp'))[2];
    my($port) = (getservbyname('smtp', 'tcp'))[2];

    my($smtpaddr) = ($smtp =~
		     /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/)
	? pack('C4',$1,$2,$3,$4)
	    : (gethostbyname($smtp))[4];

    if (!defined($smtpaddr))
    {
	return(-1);
    }

    if (!socket(MAIL, AF_INET, SOCK_STREAM, $proto))
    {
	return(-2);
    }

    if (!connect(MAIL, pack('Sna4x8', AF_INET, $port, $smtpaddr)))
    {
	return(-3);
    }

    my($oldfh) = select(MAIL);
    $| = 1;
    select($oldfh);

    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-4);
    }

    print MAIL "helo $SMTP_SERVER\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-5);
    }

    print MAIL "mail from: <$fromaddr>\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-5);
    }

    foreach (split(/, /, $to))
    {
	print MAIL "rcpt to: <$_>\r\n";
	$_ = <MAIL>;
	if (/^[45]/)
	{
	    close(MAIL);
	    return(-6);
	}
    }

    print MAIL "data\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close MAIL;
	return(-5);
    }

   }

  if ($SEND_MAIL ne "")
   {
     open (MAIL,"| $SEND_MAIL");
   }

    print MAIL "To: $to\n";
    print MAIL "From: $fromaddr\n";
    print MAIL "Reply-to: $replyaddr\n" if $replyaddr;
    print MAIL "X-Mailer: Perl Powered Socket Mailer\n";
    print MAIL "Subject: $subject\n\n";
    print MAIL "$message";
    print MAIL "\n.\n";

 if ($SMTP_SERVER ne "")
  {
    $_ = <MAIL>;
    if (/^[45]/)
    {
	close(MAIL);
	return(-7);
    }

    print MAIL "quit\r\n";
    $_ = <MAIL>;
  }

    close(MAIL);
    return(1);
}


sub no_email
{
print <<__STOP_OF_NOMAIL__;
Content-type: text/html

<FONT SIZE="+1">
<B>
SORRY! Your request could not be processed because of missing
e-mail address(es). Please use your browser's back button to
return to the card entry page.
</B>
</FONT>
__STOP_OF_NOMAIL__
}

sub send_mail
{

&setup_letter;
$mailresult=&sendmail($fields{sender_email}, $fields{sender_email}, $fields{recip_email}, $SMTP_SERVER, $SUBJECT, $msgtext); 

}
