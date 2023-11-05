#!/usr/bin/perl

############################################
##                                        ##
##         WebCal (Config Script)         ##
##           by Darryl Burgdorf           ##
##       (e-mail burgdorf@awsd.com)       ##
##                                        ##
##             version:  1.21             ##
##         last modified: 1/4/00          ##
##           copyright (c) 2000           ##
##                                        ##
##    latest version is available from    ##
##        http://awsd.com/scripts/        ##
##                                        ##
############################################

$cgiurl = "http://www.foo.com/webcal/webcal.pl";
$addcgiurl = "http://www.foo.com/webcal/webcal.add.pl";
$deletecgiurl = "http://www.foo.com/webcal/webcal.delete.pl";

@datafiles = (
  "/usr/foo/webcal/data.astro.txt",
  "/usr/foo/webcal/data.holidays.txt",
  "/usr/foo/webcal/data.jewish.txt"
  );

%editfiles = (
  "File 1","/usr/foo/webcal/data.edit1.txt",
  "File 2","/usr/foo/webcal/data.edit2.txt"
  );
  
$DataDirPath = "/usr/foo/webcal/data";
$DataDirURL = "http://www.foo.com/webcal/data";

$DataDir_header = "";
$DataDir_footer = "";

$bodyspec = "BGCOLOR=\"#ffffff\" TEXT=\"#000000\"";
$header_file = "/usr/foo/webcal/header.txt";
$footer_file = "/usr/foo/webcal/footer.txt";

$CalendarTitle = "WebCal Calendar";

$DisplayCounter = 1;
$DisplayPhases = 1;

$DefaultType = "Table";
$SmallTableText = 1;
$PreviousLastOnly = 0;
$AllowUserChoice = 1;

$AllowHTML = 1;
$AllowMultiDate = 1;

$bgcolor_normal = "ffffff";
$bgcolor_header = "6666ff";
$bgcolor_special = "ccccff";
$textcolor_normal = "000000";
$textcolor_header = "000000";
$textcolor_today = "ff0000";
$textcolor_special = "0000ff";

$TableFont = "Arial";

$HourOffset = 0;

$MonSunWeek = 0;

# NOTHING BELOW THIS LINE NEEDS TO BE ALTERED!

$version = "1.21";

@months =
  (January,February,March,April,May,June,
  July,August,September,October,November,December);
@shortmonths =
  (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec);
if ($MonSunWeek) {
	@days =
	  (Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday);
	@shortdays =
	  (Mon,Tue,Wed,Thu,Fri,Sat,Sun);
}
else {
	@days =
	  (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday);
	@shortdays =
	  (Sun,Mon,Tue,Wed,Thu,Fri,Sat);
}

$time = time;
($mday,$month,$year) = (localtime($time+($HourOffset*3600)))[3,4,5];
$month = $month+1;
$year += 1900;

unless ($INPUT{'Month'}) {
	$INPUT{'Month'} = $month;
}
unless ($INPUT{'Year'}) {
	$INPUT{'Year'} = $year;
}
unless ($INPUT{'Type'}) {
	$INPUT{'Type'} = $DefaultType; 
	$DefaultUsed = 1;
}

print "Content-type: text/html\n\n";

sub Header {
	($title) = @_;
	print "<HTML><HEAD><TITLE>$title</TITLE></HEAD>\n";
	print "<BODY $bodyspec>\n";
	if ($header_file) {
		open (HEADER,"$header_file");
		@header = <HEADER>;
		close (HEADER);
		foreach $line (@header) {
			if ($line =~ /<!--InsertAdvert\s*(.*)-->/i) {
				&insertadvert($1);
			}
			else {
				print "$line";
			}
		}
	}
}

sub Footer {
	unless ($PreviousLastOnly) {
		print "<P><HR WIDTH=75%>\n";
		print "<FORM METHOD=POST ACTION=$cgiurl>\n";
		print "<P><CENTER>Month: <SELECT NAME=Month>";
		foreach $key (1..12) {
			print "<OPTION VALUE=$key";
			if ($INPUT{'Month'} eq $key) { print " SELECTED"; }
			$xmonth = @months[$key-1];
			print ">$xmonth";
		}
		print "</SELECT> ";
		print "Year: <INPUT TYPE=TEXT NAME=Year ";
		print "VALUE=$INPUT{'Year'} SIZE=4> ";
		if ($AllowUserChoice) {
			print "Type: <SELECT NAME=Type>";
			print "<OPTION VALUE=Table";
			if ($INPUT{'Type'} eq "Table") {
				print " SELECTED";
			}
			print ">Table";
			print "<OPTION VALUE=\"Small Table\"";
			if ($INPUT{'Type'} eq "Small Table") {
				print " SELECTED";
			}
			print ">Small Table";
			print "<OPTION VALUE=Text";
			if ($INPUT{'Type'} eq "Text") {
				print " SELECTED";
			}
			print ">Text";
			print "</SELECT>";
		}
		print "\n";
		print "<P><INPUT TYPE=SUBMIT VALUE=\"View Calendar\">\n";
		print "</CENTER></FORM>\n";
	}
	if (($INPUT{'Type'} eq "Small Table")
	  && $SmallTableText && !($DefaultUsed)) {
		print "</TD></TR></TABLE></CENTER>\n";
	}
	print "<P><HR>\n<SMALL>\n<P ALIGN=CENTER>";
	print "Maintained with <STRONG>";
	print "<A HREF=\"http://awsd.com/scripts/webcal/\">";
	print "WebCal $version</A></STRONG>.\n</SMALL>\n";
	if ($footer_file) {
		open (FOOTER,"$footer_file");
		@footer = <FOOTER>;
		close (FOOTER);
		foreach $line (@footer) {
			if ($line =~ /<!--InsertAdvert\s*(.*)-->/i) {
				&insertadvert($1);
			}
			else {
				print "$line";
			}
		}
	}
	print "</BODY></HTML>\n";
}

sub insertadvert {
	local($adzone) = @_;
	$ADVNoPrint = 1;
	if ($adzone) { $ADVQuery = "zone=$adzone"; }
	else { $ADVQuery = ""; }
	require "/usr/www/users/dburgdor/scripts/ads/ads.pl";
}

1;
