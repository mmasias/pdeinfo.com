#!/usr/local/bin/perl
$SEND_MAIL="/usr/sbin/sendmail -t";
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
    $fields{$name}=$value;
#Tratamiento de los datos
#------------------------
	if ($name eq "email") {$_ = $value;s/\+/ /g;$email = $_;}
	if ($name eq "amg1") {$_ = $value;s/\+/ /g;$amg1 = $_;}
	if ($name eq "eamg1") {$_ = $value;s/\+/ /g;$eamg1 = $_;}
	if ($name eq "amg2") {$_ = $value;s/\+/ /g;$amg2 = $_;}
	if ($name eq "eamg2") {$_ = $value;s/\+/ /g;$eamg2 = $_;}
	if ($name eq "amg3") {$_ = $value;s/\+/ /g;$amg3 = $_;}
	if ($name eq "eamg3") {$_ = $value;s/\+/ /g;$eamg3 = $_;}
	if ($name eq "txtmes") {$_ = $value;s/\+/ /g;$txtmes = $_;}
}
print ("Content-Type: text/html\n\n");
$amigos="$amg1:$amg2:$amg3";
$eamigos="$eamg1:$eamg2:$eamg3";
@lista=split(":",$eamigos);
@elista=split(":",$eamigos);
$i=0;
open(Flog,">>emailenviados.log");
foreach(@lista){
 if ($_ ne ""){
  $asunto="Te invito a conocer PdeInfo";
  $mensaje="$txtmes\n";
  #Contenido del email
  open(Farch,"amigos.bd");
  while(<Farch>){
	$mensaje=$mensaje."$_";
  }
  close(Farch);
  @nada=split(/\@/,$email);
  $de=@nada[0]."\@".@nada[1];
  @nada=split(/\@/,@elista[$i]);
  $para=@nada[0]."\@".@nada[1];
  &sendmail($de, "", $para, "", $asunto, $mensaje);
 }
 print Flog "Invita: $de A: $para \n";
$i++;
}
close(Flog);
$Web =<<_HTML_;
<html><head><title>Gracias por invitar a sus amigos a PdeInfo</title>
<style>
<!--
a:link { text-decoration:none }
a:visited { text-decoration:none }
a:hover { text-decoration:underline }
-->
</style>
</head>
<body topmargin="0" leftmargin="0">
<table border="0" width="100%" cellspacing="0">
  <tr>
    <td style="border-bottom: 1 solid #FF9900" width="101"><img border="0" src="../imagenes/logos/logo_pequeno.gif" width="100" height="103"></td>
    <td style="border-bottom: 1 solid #F09858" valign="top" width="669">
      <b><font face="Tahoma" color="#F09858" size="5">Punto de Información<br>
      </font><font size="1" face="MS Sans Serif" color="#F09858">Soluciones
            creativas en el Web<br>
      </font></b>
      <font face="MS Sans Serif" size="1">http://pdeinfo.com
      </font> 
      <p align="center">
      &nbsp;<font color="#ff9900" face="MS SANS SERF, ARIAL" size="5">Cuéntele a
        un amigo acerca de Punto de Información</font>
      </p>
 </td>
  </tr>
  <tr>
    <td style="border-bottom: 2 solid #F09858" colspan="2" bgcolor="#FFEBA4" valign="top">
      <p align="center"><font face="MS Sans Serif" size="1"><b><a href="../anuncios/"><font color="#000000">Anuncios</font></a> -
      <a href="../compras/"><font color="#000000">Compras</font></a>
      - <a href="../curriculos/"><font color="#000000">Currículos</font></a> - <a href="../web/"><font color="#000000">Diseños
      Web</font></a>
      - <a href="../email/"><font color="#000000" size="1" face="MS Sans Serif">e-mail
      gratuito</font></a>
      - <a href="../listas/"><font color="#000000">Listas
      de Interés</font></a> - <a href="javascript:void" onclick="window.open('novedades.htm','novedades','height=150,width=400')"><font color="#000000" size="1" face="MS Sans Serif">Novedades</font></a>
      - <a href="../postales/"><font color="#000000">Postales</font></a></b></font>
    </td>
  </tr>
</table>
<div align="center">
  <center>
  <table border="0" cellPadding="0" cellSpacing="0" width="600">
    <tr>
      <td>
        <blockquote>
          <p><font face="MS Sans Serif" size="2"><br>
          </font><font face="MS Sans Serif" size="3">Gracias por invitar a sus
          amigos a la página de Punto de Información. Pulse <A HREF='javascript:history.go(-2)'><B>aquí</B></A> para volver
          a la página de donde vino.</font></p>
          <hr noshade size="1" color="#F09858">
        </blockquote>
        </table>
  </center>
  </div>
<p align="right"><font face="MS Sans Serif" size="1"><b><a href="/"><font color="#000000">Punto
de Información</font></a></b> 2000 - Todos los derechos reservados</font></p>
</body>
</html>
_HTML_

print $Web;


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
