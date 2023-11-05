#!/usr/local/bin/perl
################################################################## 
#  Por Manuel Masías - Punto de Información

use Socket;

$|=1;

#### PROGRAM CONFIGURATION SECTION ############################
# 
# Modify each item below to meet your needs.
#
# DAYS: number of days to keep cards before purging
# SMTP_SERVER: the name of the system acting as your sendmail gateway
#   localhost should work on most systems.
# IF NOT- SET THE SEND_MAIL VARIABLE!
# BASEDIR is the unix directory that your greeting cards will
#   be stored in.
# BASEURL is the URL (http address) of the directory your cards
#   will be stored in.
# SITEURL is the home page URL for your site.
# SITENAME is the Name of your site, ie Title
# EXT is the ending name for your card files. NEVER, EVER USE shtml!!
# PROGNAME is the URL of THIS script.
# MAILLOG is a file name that you can capture e-mail addresses in
# FOR SECURITY REASONS: RENAME THIS FILE!!!!!!!!
# okaydomains are (if specified, the ONLY domains that the script
#    can be run from. If left empty, anyone could run your script,
#    but they wouldn't see any graphics!!! If your site answers to
#    both www.domain.com and domain.com, then use both!
#

@okaydomains=("");
$DAYS=30;

# USE EITHER SMTP OR SEND_MAIL DEPENDING ON YOUR SYSTEM-
# BUT NOT BOTH!

#$SMTP_SERVER="localhost";
$SEND_MAIL="/usr/sbin/sendmail -t";

$BASEDIR="../postales";
$BASEURL="http://pdeinfo.com/postales";
$SITEURL="http://pdeinfo.com/";
$SITENAME="pdeinfo.com";
$EXT=".html";
$PROGNAME="/cgi-bin/postales.cgi";
$MAILLOG="maillog";
$SUBJECT ="Una tarjeta virtual está esperando por ti!";

###############################################################

  &main_driver;

###############################################################
#
# Now go thru the program looking for the string "BNB SAYS!"
# to locate other changes you should make, such as wording of
# the notification e-mail and "plug" for the site.
#
# to keep things simple, the field names are hard coded in.
# you can of course modify what you wish.
###############################################################

sub thank_you
{
 if ($MAILLOG ne "")
  {
   open (ML,">>$BASEDIR/$MAILLOG");      
   print ML "$fields{'recip_email'}\n";  
   print ML "$fields{'sender_email'}\n"; 
   close(ML);
  }

# PONER AQUI EL AGRADECIMIENTO DE LAS POSTALES
# --------------------------------------------
print "Content-type: text/html\n\n";
print <<__STOP_OF_THANKS__;
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
	<title>Gracias por enviar una postal de Punto de Información!</title>
	</head>
	<body background="../_themes/arcs/arctile.jpg" bgcolor="#FFFFFF" text="#000000" link="#3399FF" vlink="#666666" alink="#FF9900">
	<font face="Verdana, Arial, Helvetica">
	<H1 align="left"><font face="Times New Roman, Times New Roman, Times" color="#3399FF"><B>GRACIAS!</B></font></H1>
	<p align="left">una notificación de la tarjeta que has creado ha sido enviada a $fields{'recip_name'}
	<p align="left">La dirección de la tarjeta es</p>
	<CENTER><P><A HREF="$URL_NAME">$URL_NAME</A>
	<p align="center"><img src="../_themes/arcs/arcsepa.gif" width="600" height="10"></p>
	<P>
	<B><A HREF=$fields{'parent'}>Volver al creador de Tarjetas</A></B>
	</font></body>
</html>
__STOP_OF_THANKS__
}

# BNB SAYS! 
# THIS IS WHERE YOU CAN CUSTOMIZE YOUR NOTIFICATION LETTER
# DO NOT TOUCH THE TWO LINES WITH __STOP_OF_MESSAGE__ ON
# THEM!!!!

sub setup_letter
{
$msgtext =<<__STOP_OF_MESSAGE__;
Holas!!!

$fields{'sender_name'} estuvo paseando por el sitio web de Punto de Información, $SITENAME
y creo una tarjeta virtual para ti! Para recogerla simplemente apunta tu navegador a la 
pagina que se indica abajo:

   $URL_NAME

La tarjeta estará disponible en nuestros servidores por 30 días, de modo que te rogamos
la imprimas o la guardes en tu disco duro si deseas conservarla.

__STOP_OF_MESSAGE__
}

# BNB SAYS! 
# This is what makes up the body of your card. DO NOT REMOVE OR
# MODIFY THE LINES ABOVE THE WORD $param or the $param line
# itself. Doing so will cause the script to fail.
sub make_body
{
$cardbody =<<__END_OF_CARD_BODY__;
$BODYTAG
$params
<CENTER>
<P>
<TABLE WIDTH=580 BGCOLOR=$fields{'back_color'} BORDER=2 cellpadding=5 cellspacing=0>
 <TR>
 <TD>
<TABLE WIDTH=580 BGCOLOR=$fields{'back_color'}>
 <TR>
 <TD>
  <TABLE WIDTH=200 BORDER=1 cellpadding=2 cellspacing=0>
    <TR>
      <TD ALIGN=CENTER VALIGN=CENTER>
       <IMG SRC=$BASEURL/$fields{'pic_select'} BORDER=0>
      </TD>
    </TR>
  </TABLE>
 </TD>
 <TD WIDTH=380 VALIGN=TOP >
   <CENTER>
   <FONT SIZE=+2 COLOR=$fields{'text_color'}
     FACE=ARIAL><B>$fields{'the_title'}</B></FONT>
   <HR WIDTH=200>
   <TABLE WIDTH=355>
    <TR>
     <TD><FONT FACE=ARIAL COLOR=$fields{'text_color'}>
         $fields{'the_message'}
      <P ALIGN=CENTER>
      <I>$fields{'sig_line'}
      </I>
      </P>
      </FONT>
      </TD>
    </TR>
   </TABLE>
   </CENTER>
 </TD>
 </TR>
</TABLE>
</TD>
</TR>
</TABLE>
<P>
<TABLE WIDTH=500>
  <TR>
  <TD>
  <FONT FACE="ARIAL" SIZE=2>
  Esta postal ha sido creada por <A HREF=mailto:$fields{'sender_email'}>$fields{'sender_name'}</A>
  expresamente para <A HREF=mailto:$fields{'recip_email'}>$fields{'recip_name'}</A>. 
  <BR>Si deseas enviar otra tarjeta puedes ir al <A HREF='http://pdeinfo.com/postales'>sitio de postales de PdeInfo</A> y crear tu propia postal virtual.
	</FONT>
  </TD>
  </TR>
</TABLE>
<FONT FACE="ARIAL" SIZE=1>
<SCRIPT LANGUAGE="JavaScript">
<!--
if(navigator.userAgent.indexOf("MSIE") != -1)
document.writeln ('');
else
document.writeln ('<EMBED SRC="$BASEURL/$fields{'midifile'}" AUTOSTART="true" HIDDEN="true" VOLUME="80%">');
//-->
</SCRIPT>
<BGSOUND SRC="$BASEURL/$fields{'midifile'}">
<HR><SMALL>
  Este es un servicio gratuito de <A HREF="http://pdeinfo.com">Punto de Información</A><BR> 
	Sistemas de Punto de Información - Todos los derechos reservados.   
</BODY>
</HTML>
__END_OF_CARD_BODY__
}

sub pass_params
{
$params=<<__END_OF_PARAMS__;
<CENTER>
<TABLE WIDTH=500>
<TR>
<TD>
<FONT FACE="MS Sans Serif" SIZE=2>
Para enviar la postal que acabas de crear, pulsa en el botón ENVIAR POSTAL.<BR>
Si deseas regresar a la pantalla de diseño sin enviarla, pulsa el botón de ATRAS en tu navegador.
</FONT>
<CENTER>
<FORM METHOD="POST" ACTION="$PROGNAME">
<INPUT TYPE="HIDDEN" NAME="action_code" VALUE="SENDCARD">
<INPUT TYPE="HIDDEN" VALUE="$fields{'pic_select'}" NAME="pic_select">
<INPUT TYPE="HIDDEN" VALUE="$fields{'sender_name'}" NAME="sender_name">
<INPUT TYPE="HIDDEN" VALUE="$fields{'sender_email'}" NAME="sender_email">
<INPUT TYPE="HIDDEN" VALUE="$fields{'recip_name'}" NAME="recip_name">
<INPUT TYPE="HIDDEN" VALUE="$fields{'recip_email'}" NAME="recip_email">
<INPUT TYPE="HIDDEN" VALUE="$fields{'text_color'}" NAME="text_color">
<INPUT TYPE="HIDDEN" VALUE="$fields{'back_color'}" NAME="back_color">
<INPUT TYPE="HIDDEN" VALUE="$fields{'the_title'}" NAME="the_title">
<INPUT TYPE="HIDDEN" VALUE="$fields{'the_message'}" NAME="the_message">
<INPUT TYPE="HIDDEN" VALUE="$fields{'sig_line'}" NAME="sig_line">
<INPUT TYPE="HIDDEN" VALUE="$fields{'midifile'}" NAME="midifile">
<INPUT TYPE="HIDDEN" VALUE="$fields{'background'}" NAME="background">
<INPUT TYPE="HIDDEN" VALUE="$ENV{'HTTP_REFERER'}" NAME="parent">
<INPUT TYPE="submit" VALUE="ENVIAR POSTAL" style="background-color: #6699CC; color: #FFFFFF; border: 1 outset #6699CC; padding: 2">   
</FORM>
</CENTER>
 </TD>
 </TR>
</TABLE>
__END_OF_PARAMS__
}


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

sub card_expire
 {
  local(@items, $item);
  opendir(CARDDIR, "$BASEDIR");
  @items = grep(/[0-9]$EXT/,readdir(CARDDIR));
  closedir(CARDDIR);
  foreach $item (@items)
   {
    if (-M "$BASEDIR/$item" > $DAYS)
     {
      unlink("$BASEDIR/$item");
     }
   }
 }



##################################################################
sub valid_address 
 {
  $testmail = $fields{'recip_email'};
  if ($testmail =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)/ ||
  $testmail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/)
   {
     return 0;
   }
   else 
    {
      return 1;
    }
}


sub bad_email
{
print <<__STOP_OF_BADMAIL__;
Content-type: text/html

<FONT SIZE="+1">
<B>
Hey! tu tarjeta no puede ser enviada porque hay un error
en la dirección de correo electrónico. Por favor usa el botón 
de "Atras" e intenta nuevamente.
</B>
</FONT>
__STOP_OF_BADMAIL__
}

sub test_basedir
{
  if (not -w $BASEDIR)
   {
print <<__STOP_OF_BADBASE__;
Content-type: text/html

<FONT SIZE="+1">
<B>
The script cannot either find or write to the<BR>
$BASEDIR directory. Please check this setting if
the BASEDIR variable, and the permissions of the
directory. If you have them set to 755, please 
change them to 777.
</B>
</FONT>
__STOP_OF_BADBASE__
exit;
   }
}

##################################################################
sub valid_page
 {
 if (@okaydomains == 0) {return;}
  $DOMAIN_OK=0;                                         
  $RF=$ENV{'HTTP_REFERER'};                             
  $RF=~tr/A-Z/a-z/;                                     
  foreach $ts (@okaydomains)                            
   {                                                    
     if ($RF =~ /$ts/)                                  
      { $DOMAIN_OK=1; }
   }                                                    
   if ( $DOMAIN_OK == 0)                                
     { print "Content-type: text/html\n\n Sorry, cant run it from here....";    
      exit;
     }                                                  
}

sub decode_vars
{
#This part of the program splits up our data and gets it
#ready for formatting.
  $i=0;
  read(STDIN,$temp,$ENV{'CONTENT_LENGTH'});
  @pairs=split(/&/,$temp);
  foreach $item(@pairs)
   {
    ($key,$content)=split(/=/,$item,2);
    $content=~tr/+/ /;
    $content=~s/%(..)/pack("c",hex($1))/ge;
    $content =~ s/<!--(.|\n)*-->//g;
    $fields{$key}=$content;
    $i++;
    $item{$i}=$key;
    $response{$i}=$content;
   }
}

sub get_file_name
{
   $proc=$$;
   $newnum=time;
   $newnum=substr($newnum,4,5);
   $date=localtime(time);  
   ($day, $month, $num, $time, $year) = split(/\s+/,$date); 
   $month=~tr/A-Z/a-z/;
   $PREF = "$month$num-";
   $FILE_NAME="$BASEDIR/$PREF$newnum$proc$EXT";
   $URL_NAME="$BASEURL/$PREF$newnum$proc$EXT";
}


#Write out our HTML FILE
sub create_file
{
  open(OUTFILE,">$FILE_NAME") ;
  print OUTFILE "$cardbody\n";
  close (OUTFILE);
}

#Set up our HTML Preview Form
sub do_preview
{
$fields{'the_message'} =~s/\"/\'/g;
  &pass_params;
  &make_body;
print "Content-type: text/html\n\n";
print "$cardbody\n";
}

sub main_driver
{
   &valid_page;
   &test_basedir;
   &decode_vars;

   if ($fields{'recip_email'} eq "")
     { &no_email; exit; } 
   if (&valid_address == 0)
    { &bad_email; exit; }
   if ($fields{'sender_email'} eq "")
     { &no_email; exit; }

   if ($fields{'background'} ne "")
    { $BODYTAG="<BODY topmargin=\"0\" background=\"_themes/arcs/arctile.jpg\" bgcolor=\"#FFFFFF\" text=\"#000000\" link=\"#3399FF\" vlink=\"#666666\" alink=\"#FF9900\">";}
     else { $BODYTAG="<body topmargin=\"0\" background=\"_themes/arcs/arctile.jpg\" bgcolor=\"#FFFFFF\" text=\"#000000\" link=\"#3399FF\" vlink=\"#666666\" alink=\"#FF9900\">";}

   if ($fields{'action_code'} eq "NEW") 
     { &do_preview; }

   if ($fields{'action_code'} eq "SENDCARD") 
     {                             
      &make_body;
      &get_file_name;
      &create_file;
      &setup_letter;
      $mailresult=&sendmail($fields{sender_email}, $fields{sender_email}, $fields{recip_email}, $SMTP_SERVER, $SUBJECT, $msgtext); 
      &thank_you;
      if ($DAYS > 0)
       {&card_expire;}
     }

}

