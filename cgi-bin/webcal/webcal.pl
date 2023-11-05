#!/usr/bin/perl

############################################
##                                        ##
##                 WebCal                 ##
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

# COPYRIGHT NOTICE:
#
# Copyright 2000 Darryl C. Burgdorf.  All Rights Reserved.
#
# This program is being distributed as shareware.  It may be used and
# modified by anyone, so long as this copyright notice and the header
# above remain intact, but any usage should be registered.  (See the
# program documentation for registration information.)  Selling the
# code for this program without prior written consent is expressly
# forbidden.  Obtain permission before redistributing this program
# over the Internet or in any other medium.  In all cases copyright
# and header must remain intact.
#
# This program is distributed "as is" and without warranty of any
# kind, either express or implied.  (Some states do not allow the
# limitation or exclusion of liability for incidental or consequential
# damages, so this notice may not apply to you.)  In no event shall
# the liability of Darryl C. Burgdorf and/or Affordable Web Space
# Design for any damages, losses and/or causes of action exceed the
# total amount paid by the user for this software.

# VERSION HISTORY:
#
# 1.21  01/04/00  Corrected add script's handling of 4-digit years
#                 Changed deliter used in delete script from :: to |
# 1.20  12/30/99  Allowed for use of multiple data files
#                 Made display of "day counter" optional
#                 Added (optional) calculation of lunar phases
#                 Changed "annual" code to "x" to allow 0 for 2000
#                 Short year entries now 1950-2049
#                 Extended one-year limit on "day each week" entries
#                 Squashed "day each week / MonSunWeek" entry bug
#                 Added check for entry dir validity before using
#                 Added line/paragraph parsing to "data dir" entries
#                 Added separate header/footer for "data dir" entries
#                 Improved checks on entry validity
#                 Replaced "reload to add another" with FORM button
#                 Added $CalendarTitle and $TableFont
#                 Added $HourOffset
#                 Lots of minor tweaks, after two years.... ;)
# 1.11  01/30/98  Corrected small problem with some versions of Perl 5
# 1.10  01/29/98  FIRST SHAREWARE RELEASE
#                 Moved configuration variables to separate file
#                 Added configurable table colors
#                 Added "Small Table" option (with or without text)
#                 Stripped "empty" entries from text listing
#                 Allowed for "Monday-Sunday" weeks
#                 Allowed for two-digit year entry (1900s)
#                 Allowed for "date range" entries
#                 Added option to allow HTML in calendar data entries
#                 Limited basic event entries to 80 characters
#                 Added optional "data dir" for more extensive entries
#                 Allowed disabling of user choice of style
#                 Fixed bug that made some entries "undeletable"
# 1.00  01/05/98  Initial "public" release

require "/usr/foo/webcal/webcal.config.pl";

# NOTHING BELOW THIS LINE NEEDS TO BE ALTERED!

$DefaultUsed = 0;

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$INPUT{$name} = $value;
}

if ($INPUT{'Year'} =~ /\D/) { $INPUT{'Year'} = 0; }
elsif ($INPUT{'Year'} < 50) { $INPUT{'Year'} += 2000; }
elsif ($INPUT{'Year'} < 100) { $INPUT{'Year'} += 1900; }

if (($INPUT{'Year'} < 1601) || ($INPUT{'Year'} > 2899)) {
	&Header("Date Out of Range!");
	print "<H1 ALIGN=CENTER>Date Out of Range!</H1>\n";
	print "<P ALIGN=CENTER>The date you provided is out of range.";
	print "<BR>It must be between 1601 and 2899 A.D.\n";
	&Footer;
	exit;
}

foreach $datafile (@datafiles) {
	open (DATA,$datafile);
	while ($line=<DATA>) {
		push (@unsorteddata,$line);
	}
	close (DATA);
}

@data = sort {$a <=> $b} (@unsorteddata);

foreach $line (@data) {
	if ($line =~ /\n$/) { chop ($line); }
	($date,$desc,$URL) = split (/\|/, $line);
	($dateyear,$datemonth,$dateday) = 
	  $date =~ m#(\d\d\d\d)(\d\d)(\d\d)#o;
	if ((int($dateyear) == int($INPUT{'Year'}))
	  || (int($dateyear) < 1)) {
		if (int($datemonth) == int($INPUT{'Month'})) {
			$textdesc = $desc;
			$textdesc =~ s/<([^>]|\n)*>//g;
			if ($URL) {
				$Table{int($dateday)} .= "<P><A HREF=\"$URL\">";
				$Table{int($dateday)} .= "$desc</A>";
				$SmallTable{int($dateday)} .= "<BR><HR NOSHADE WIDTH=25%><A ";
				$SmallTable{int($dateday)} .= "HREF=\"$URL\">";
				$SmallTable{int($dateday)} .= "$desc</A>";
				$Text{int($dateday)} .= "                    ";
				$Text{int($dateday)} .= "<A HREF=\"$URL\">";
				$Text{int($dateday)} .= "$textdesc</A>\n";
			}
			else {
				$Table{int($dateday)} .= "<P>$desc";
				$SmallTable{int($dateday)} .= "<BR><HR NOSHADE WIDTH=25%>$desc";
				$Text{int($dateday)} .= "                    ";
				$Text{int($dateday)} .= "$textdesc\n";
			}
		}
	}
	$SmallTable{int($dateday)} =~ s/^<BR><HR NOSHADE WIDTH=25%>//;
	$Text{int($dateday)} =~ s/^                    //;
}

&PerpetualCalendar(int($INPUT{'Month'}),1,int($INPUT{'Year'}));

$xmonth = @months[int($INPUT{'Month'})-1];
$heading = "$xmonth $INPUT{'Year'}";
&Header("$heading");

if ($CalendarTitle) {
	print "<H1 ALIGN=CENTER>$CalendarTitle</H1>\n";
}

if ($INPUT{'Type'} eq "Text") {
	print "<H1 ALIGN=CENTER>$heading</H1>\n";
	print "<P><FONT FACE=\"Courier\"><PRE>\n";
	foreach $key (1..$perp_eom) {
		$weekday = ($key+$perp_dow)-(int(($key+$perp_dow)/7)*7);
		if ($weekday < 1) { $weekday = 7; }
		if ($DisplayPhases) {
			if (int((int((($perp_days-5.36945)/29.53031)+.5)*29.53031)+5.36945) == $perp_days) {
				if ($Text{$key}) { $Text{$key} .= "                    "; }
				$Text{$key} .= "New Moon\n";
			}
			if (int((int((($perp_days-12.75202)/29.53031)+.5)*29.53031)+12.75202) == $perp_days) {
				if ($Text{$key}) { $Text{$key} .= "                    "; }
				$Text{$key} .= "First Quarter Moon\n";
			}
			if (int((int((($perp_days-20.13460)/29.53031)+.5)*29.53031)+20.13460) == $perp_days) {
				if ($Text{$key}) { $Text{$key} .= "                    "; }
				$Text{$key} .= "Full Moon\n";
			}
			if (int((int((($perp_days-27.51718)/29.53031)+.5)*29.53031)+27.51718) == $perp_days) {
				if ($Text{$key}) { $Text{$key} .= "                    "; }
				$Text{$key} .= "Last Quarter Moon\n";
			}
		}
		$perp_days++;		
		if ($Text{$key}) {
			if ($key < 10) { print "0"; }
			print "$key ";
			$xshortmonth = @shortmonths[$INPUT{'Month'}-1];
			print "$xshortmonth ";
			print "$INPUT{'Year'} ";
			$xshortday = @shortdays[$weekday-1];
			print "($xshortday)   ";
			print "$Text{$key}";
		}
		if (($weekday == 7) && !($key == $perp_eom)) {
			print "\n                    ---------------\n\n";
		}
	}
	print "</PRE></FONT>\n";
}
elsif ($INPUT{'Type'} eq "Table") {
	print "<P><CENTER><SMALL><TABLE BORDER=6 CELLPADDING=6><TR>\n";
	print "<TH COLSPAN=7 ";
	print "BGCOLOR=\"#$bgcolor_header\">";
	print "<FONT COLOR=\"#$textcolor_header\" FACE=\"$TableFont\">";
	print "<H1>$heading</H1></FONT></TH>\n";
	print "</TR><TR>\n";
	foreach $key (1..7) {
		print "<TH ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<FONT COLOR=\"#$textcolor_normal\" FACE=\"$TableFont\">";
		$xday = @days[$key-1];
		print "<BIG>$xday</BIG></FONT></TH>";
	}
	print "\n</TR><TR>\n";
	if ($perp_dow > 0) {
		print "<TD COLSPAN=$perp_dow ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<P>&nbsp</TD>";
	}
	foreach $key (1..$perp_eom) {
		if ($DisplayPhases) {
			if (int((int((($perp_days-5.36945)/29.53031)+.5)*29.53031)+5.36945) == $perp_days) {
				$Table{$key} .= "<P><SMALL>New Moon</SMALL>";
			}
			if (int((int((($perp_days-12.75202)/29.53031)+.5)*29.53031)+12.75202) == $perp_days) {
				$Table{$key} .= "<P><SMALL>First Quarter Moon</SMALL>";
			}
			if (int((int((($perp_days-20.13460)/29.53031)+.5)*29.53031)+20.13460) == $perp_days) {
				$Table{$key} .= "<P><SMALL>Full Moon</SMALL>";
			}
			if (int((int((($perp_days-27.51718)/29.53031)+.5)*29.53031)+27.51718) == $perp_days) {
				$Table{$key} .= "<P><SMALL>Last Quarter Moon</SMALL>";
			}
		}
		$perp_days++;		
		print "<TD VALIGN=TOP BGCOLOR=\"#";
		if ($Table{$key}) { print "$bgcolor_special\">"; }
		else { print "$bgcolor_normal\">"; }
		if (($INPUT{'Year'} == $year)
		  && ($INPUT{'Month'} == $month)
		  && ($key == $mday)) {
			print "<FONT COLOR=\"#$textcolor_today\" FACE=\"$TableFont\">";
			print "<P><BIG><STRONG>$key</STRONG></BIG>";
		}
		else {
			print "<FONT COLOR=\"#$textcolor_normal\" FACE=\"$TableFont\">";
			print "<P><BIG>$key</BIG>";
		}
		if ($DisplayCounter) {
			print "<BR><SMALL>($perp_sofar/$perp_togo)</SMALL>";
		}
		$perp_sofar++;
		$perp_togo -= 1;
		print "</FONT>";
		if ($Table{$key}) {
			print "<FONT COLOR=\"#$textcolor_special\" FACE=\"$TableFont\">";
			print "$Table{$key}";
			print "</FONT>";
		}
		else { print "<P>&nbsp;"; }
		print "</TD>";
		$weekday = ($key+$perp_dow)-(int(($key+$perp_dow)/7)*7);
		if (($weekday == 0) && !($key == $perp_eom)) {
			print "\n</TR><TR>\n";
		}
	}
	if ($weekday > 0) {
		$leftover = 7-$weekday;
		print "<TD COLSPAN=$leftover ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<P>&nbsp;</TD>";
	}
	print "</TR></TABLE></SMALL></CENTER>\n";
}
else {
	if ($SmallTableText) {
		print "<P><CENTER><TABLE CELLPADDING=12><TR>";
		print "<TD VALIGN=TOP>\n";
		print "<P><CENTER><TABLE CELLPADDING=3>\n";
		foreach $key (1..$perp_eom) {
			if ($DisplayPhases) {
				if (int((int((($perp_days-5.36945)/29.53031)+.5)*29.53031)+5.36945) == $perp_days) {
					if ($SmallTable{$key}) { $SmallTable{$key} .= "<BR>"; }
					$SmallTable{$key} .= "New Moon\n";
				}
				if (int((int((($perp_days-12.75202)/29.53031)+.5)*29.53031)+12.75202) == $perp_days) {
					if ($SmallTable{$key}) { $SmallTable{$key} .= "<BR>"; }
					$SmallTable{$key} .= "First Quarter Moon\n";
				}
				if (int((int((($perp_days-20.13460)/29.53031)+.5)*29.53031)+20.13460) == $perp_days) {
					if ($SmallTable{$key}) { $SmallTable{$key} .= "<BR>"; }
					$SmallTable{$key} .= "Full Moon\n";
				}
				if (int((int((($perp_days-27.51718)/29.53031)+.5)*29.53031)+27.51718) == $perp_days) {
					if ($SmallTable{$key}) { $SmallTable{$key} .= "<BR>"; }
					$SmallTable{$key} .= "Last Quarter Moon\n";
				}
			}
			$perp_days++;		
			next unless ($SmallTable{$key});
			print "<TR><TD BGCOLOR=\"#$bgcolor_normal\">";
			print "<FONT COLOR=\"#$textcolor_normal\" FACE=\"$TableFont\">";
			$xshortmonth = @shortmonths[$INPUT{'Month'}-1];
			print "$key $xshortmonth ";
			print "$INPUT{'Year'} ";
			$weekday =
			  ($key+$perp_dow)-(int(($key+$perp_dow)/7)*7);
			if ($weekday < 1) { $weekday = 7; }
			$xshortday = @shortdays[$weekday-1];
			print "($xshortday):";
			print "</FONT></TD>";
			print "</TR><TR>";
			print "<TD BGCOLOR=\"#$bgcolor_special\">";
			print "<FONT COLOR=\"#$textcolor_special\" FACE=\"$TableFont\">";
			print "$SmallTable{$key}</FONT></TD>";
			print "</TR>";
		}
		print "</TABLE></CENTER>";
		print "</TD><TD VALIGN=TOP>\n";
	}
	print "<P><CENTER><SMALL><TABLE BORDER=3 CELLPADDING=3><TR>\n";
	print "<TH COLSPAN=7 ";
	print "BGCOLOR=\"#$bgcolor_header\">";
	print "<FONT COLOR=\"#$textcolor_header\" FACE=\"$TableFont\">";
	print "<BIG>$heading</BIG></FONT></TH>\n";
	print "</TR><TR>\n";
	foreach $key (1..7) {
		print "<TH ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<FONT COLOR=\"#$textcolor_normal\" FACE=\"$TableFont\">";
		$xshortday = @shortdays[$key-1];
		print "$xshortday</FONT></TH>";
	}
	print "\n</TR><TR>\n";
	if ($perp_dow > 0) {
		print "<TD COLSPAN=$perp_dow ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<P>&nbsp</TD>";
	}
	foreach $key (1..$perp_eom) {
		print "<TD VALIGN=TOP ALIGN=RIGHT BGCOLOR=\"#";
		if ($SmallTable{$key}) { print "$bgcolor_special\">"; }
		else { print "$bgcolor_normal\">"; }
		if (($INPUT{'Year'} == $year)
		  && ($INPUT{'Month'} == $month)
		  && ($key == $mday)) {
			print "<FONT COLOR=\"#$textcolor_today\" FACE=\"$TableFont\">";
			print "<P>$key";
		}
		else {
			print "<FONT COLOR=\"#$textcolor_normal\" FACE=\"$TableFont\">";
			print "<P>$key";
		}
		print "</FONT></TD>";
		$weekday = ($key+$perp_dow)-(int(($key+$perp_dow)/7)*7);
		if (($weekday == 0) && !($key == $perp_eom)) {
			print "\n</TR><TR>\n";
		}
	}
	if ($weekday > 0) {
		$leftover = 7-$weekday;
		print "<TD COLSPAN=$leftover ";
		print "BGCOLOR=\"#$bgcolor_normal\">";
		print "<P>&nbsp;</TD>";
	}
	print "</TR></TABLE></SMALL></CENTER>\n";
}

print "<P><CENTER><TABLE><TR>\n";

$LastYear = int($INPUT{'Year'});
$LastMonth = int($INPUT{'Month'})-1;
if ($LastMonth == 0) {
	$LastMonth = 12;
	$LastYear -= 1;
}
print "<TD><FORM METHOD=POST ACTION=$cgiurl>";
print "<INPUT TYPE=HIDDEN NAME=Month VALUE=$LastMonth>";
print "<INPUT TYPE=HIDDEN NAME=Year VALUE=$LastYear>";
print "<INPUT TYPE=HIDDEN NAME=Type VALUE=\"$INPUT{'Type'}\">";
print "<INPUT TYPE=SUBMIT VALUE=\"Previous Month\">";
print "</FORM></TD>\n";

$NextYear = int($INPUT{'Year'});
$NextMonth = int($INPUT{'Month'})+1;
if ($NextMonth == 13) {
	$NextMonth = 1;
	$NextYear += 1;
}
print "<TD><FORM METHOD=POST ACTION=$cgiurl>";
print "<INPUT TYPE=HIDDEN NAME=Month VALUE=$NextMonth>";
print "<INPUT TYPE=HIDDEN NAME=Year VALUE=$NextYear>";
print "<INPUT TYPE=HIDDEN NAME=Type VALUE=\"$INPUT{'Type'}\">";
print "<INPUT TYPE=SUBMIT VALUE=\"Next Month\">";
print "</FORM></TD>\n";

print "</TR></TABLE></CENTER>\n";

&Footer;
exit;

sub PerpetualCalendar {
	# This perpetual calendar routine provides accurate day/date
	# correspondences for dates from 1601 to 2899 A.D.  It is based on
	# the Gregorian calendar, so be aware that early correspondences
	# may not always be historically accurate.  The Gregorian calendar
	# was adopted by the Italian states, Portugal and Spain in 1582,
	# and by the Catholic German states in 1583.  However, it was not
	# adopted by the Protestant German states until 1699, by England
	# and its colonies until 1752, by Sweden until 1753, by Japan
	# until 1873, by China until 1912, by the Soviet Union until 1918,
	# and by Greece until 1923.
	($perp_mon,$perp_day,$perp_year) = @_;
	%day_counts =
	  (1,0,2,31,3,59,4,90,5,120,6,151,7,181,
	  8,212,9,243,10,273,11,304,12,334);
	$perp_days = (($perp_year-1601)*365)+(int(($perp_year-1601)/4));
	$perp_days += $day_counts{$perp_mon};
	$perp_days += $perp_day;
	$perp_sofar = $day_counts{$perp_mon};
	$perp_sofar += $perp_day;
	$perp_togo = 365-$perp_sofar;
	if (int(($perp_year-1600)/4) eq (($perp_year-1600)/4)) {
		$perp_togo++;
		if ($perp_mon > 2) {
			$perp_days++;
			$perp_sofar++;
			$perp_togo -= 1;
		}
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ((($perp_year == $key) && ($perp_mon > 2))
		  || ($perp_year > $key)) {
			$perp_days -= 1;
		}
	}
	$perp_dow = $perp_days - (int($perp_days/7)*7);
	if ($perp_dow == 7) { $perp_dow = 0; }
	if ($MonSunWeek) {
		$perp_dow -= 1;
		if ($perp_dow == -1) { $perp_dow = 6; }
	}
	$perp_eom = 31;
	if (($perp_mon == 4) || ($perp_mon == 6)
	  || ($perp_mon == 9) || ($perp_mon == 11)) {
		$perp_eom = 30;
	}
	if (($perp_mon == 2)) {
		$perp_eom = 28;
	}
	if ((int(($perp_year-1600)/4) eq (($perp_year-1600)/4))
	  && ($perp_mon == 2)) {
		$perp_eom = 29;
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ($perp_year == $key) {
			if ($perp_mon == 1) {
				$perp_togo -= 1;
			}
			elsif ($perp_mon == 2) {
				$perp_togo -= 1;
				$perp_eom = 28;
			}
			else {
				$perp_sofar -= 1;
			}
		}
	}
}

