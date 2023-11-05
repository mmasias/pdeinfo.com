#!/usr/bin/perl

############################################
##                                        ##
##        WebCal (Addition Script)        ##
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

require "/usr/foo/webcal/webcal.config.pl";

# NOTHING BELOW THIS LINE NEEDS TO BE ALTERED!

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$INPUT{$name} = $value;
}

unless (-w "$DataDirPath") { $DataDirPath = ""; }

if ($INPUT{'Add'}) { &Add; }
else { &Display; }

sub Display {
	&Header("Add Calendar Entry");
	print "<H1 ALIGN=CENTER>Add New Calendar Entry:</H1>\n";
	print "<CENTER><FORM METHOD=POST ACTION=$addcgiurl>\n";
	$datafiles = (keys %editfiles);
	if ($datafiles > 1) {
		print "<P><STRONG>Data File to Edit:</STRONG> <SELECT NAME=\"datafile\">";
		foreach $key (sort keys %editfiles) {
			print "<OPTION VALUE=\"$editfiles{$key}\">$key";
		}
		print "</SELECT>\n";
	}
	else {
		foreach $key (keys %editfiles) {
			print "<INPUT TYPE=HIDDEN NAME=\"datafile\" ";
			print "VALUE=\"$editfiles{$key}\">\n";
		}
	}
	print "<P><EM>Input the date of the event below.";
	print "<BR>Use a year designation of &quot;x&quot; ";
	print "for an annual (every year) event.";
	print "<BR>Two-digit year entries will be understood ";
	print "<BR>to lie between 1950 and 2049 A.D.</EM>\n";
	print "<P><STRONG>Month:</STRONG> <SELECT NAME=StartMonth>";
	print "<OPTION VALUE=0>";
	foreach $key (1..12) {
		$xshortmonth = @shortmonths[$key-1];
		print "<OPTION VALUE=$key>$xshortmonth";
	}
	print "</SELECT> ";
	print "<STRONG>Date:</STRONG> ";
	print "<INPUT TYPE=TEXT NAME=StartDate SIZE=2> ";
	print "<STRONG>Year:</STRONG> ";
	print "<INPUT TYPE=TEXT NAME=StartYear SIZE=4>\n";
	if ($AllowMultiDate) {
		print "<P><EM>If you wish an event to appear ";
		print "on a series of dates,<BR>";
		print "enter the ending date below.</EM>\n";
		print "<P><STRONG>End Month:</STRONG> ";
		print "<SELECT NAME=EndMonth>";
		print "<OPTION VALUE=0>";
		foreach $key (1..12) {
			$xshortmonth = @shortmonths[$key-1];
			print "<OPTION VALUE=$key>$xshortmonth";
		}
		print "</SELECT> ";
		print "<STRONG>End Date:</STRONG> ";
		print "<INPUT TYPE=TEXT NAME=EndDate SIZE=2> ";
		print "<STRONG>End Year:</STRONG> ";
		print "<INPUT TYPE=TEXT NAME=EndYear SIZE=4>\n";
		print "<P><EM>Instead of specifying a straight series ";
		print "of dates above,<BR>you may specify a certain day ";
		print "(e.g., &quot;Second Tuesday&quot;)<BR>of each of a ";
		print "series of months.</EM>";
		print "<P><STRONG>Day:</STRONG> ";
		print "<SELECT NAME=RangeNumber><OPTION VALUE=0>";
		print "<OPTION VALUE=1>First<OPTION VALUE=2>Second";
		print "<OPTION VALUE=3>Third<OPTION VALUE=4>Fourth";
		print "<OPTION VALUE=5>Every</SELECT> \n";
		print "<SELECT NAME=RangeDay><OPTION VALUE=0>";
		foreach $key (1..7) {
			$xday = @days[$key-1];
			print "<OPTION VALUE=$key>$xday";
		}
		print "</SELECT> ";
		print "<P><STRONG>First Month:</STRONG> ";
		print "<SELECT NAME=FirstMonth><OPTION VALUE=0>";
		foreach $key (1..12) {
			$xshortmonth = @shortmonths[$key-1];
			print "<OPTION VALUE=$key>$xshortmonth";
		}
		print "</SELECT> ";
		print "<STRONG>Year:</STRONG> ";
		print "<INPUT TYPE=TEXT NAME=FirstYear SIZE=4> ";
		print "<STRONG>Last Month:</STRONG> ";
		print "<SELECT NAME=LastMonth><OPTION VALUE=0>";
		foreach $key (1..12) {
			$xshortmonth = @shortmonths[$key-1];
			print "<OPTION VALUE=$key>$xshortmonth";
		}
		print "</SELECT> ";
		print "<STRONG>Year:</STRONG> ";
		print "<INPUT TYPE=TEXT NAME=LastYear SIZE=4>\n";
	}
	print "<P><EM>Input a brief description (or title) ";
	print "of the event below.<BR>You may also include a URL ";
	print "(Web page address)<BR>if you wish to link to ";
	print "a page with more detailed information.</EM>\n";
	if ($AllowHTML) {
		print "<BR><EM>(HTML tags may be included in the event ";
		print "description.<BR>However, if you use them, ";
		print "please include any URL in the ";
		print "description<BR>instead of inputting it in the ";
		print "separate URL box. Thanks!)</EM>\n";
	}
	print "<P><STRONG>Event:</STRONG> ";
	print "<INPUT TYPE=TEXT NAME=Add SIZE=40 MAXLENGTH=80>\n";
	print "<P><STRONG>URL (optional):</STRONG> ";
	print "<INPUT TYPE=TEXT NAME=URL ";
	print "VALUE=\"http://\" SIZE=50>\n";
	if ($DataDirPath && $DataDirURL) {
		print "<P><EM>If you have no URL, but want ";
		print "to include more information, enter it ";
		print "here.<BR>A document will be created ";
		print "for you, to which the entry will ";
		print "link.</EM>\n";
		if ($AllowHTML) {
			print "<BR><EM>(Again, you are welcome ";
			print "to include HTML tags here.)</EM>\n";
		}
		print "<P><STRONG>Detailed Information:</STRONG>\n";
		print "<BR><TEXTAREA COLS=50 ROWS=10 ";
		print "NAME=FullText WRAP=VIRTUAL></TEXTAREA>\n";
	}
	print "<P><INPUT TYPE=SUBMIT VALUE=\"Add Event to Calendar\">\n";
	print "</FORM></CENTER>\n";
	&Footer;
	exit;
}

sub Add {
	unless ((($INPUT{'RangeNumber'} && $INPUT{'RangeDay'}
	  && $INPUT{'FirstMonth'} && $INPUT{'LastMonth'})
	  || ($INPUT{'StartMonth'} && $INPUT{'StartDate'}))
	  && $INPUT{'Add'} && $INPUT{'datafile'}) {
		&Header("Incomplete Submission");
		print "<H1 ALIGN=CENTER>Incomplete Submission!</H1>\n";
		print "<P ALIGN=CENTER>You didn't include enough information!\n";
		print "<P ALIGN=CENTER><EM>(Use your browser's ";
		print "&quot;Back&quot; button<BR>or just reload ";
		print "this page to try again!)</EM>\n";
		&Footer;
		exit;
	}
	$INPUT{'Add'} =~ s/|//g;
	$INPUT{'Add'} =~ s/\n//g;
	if ($AllowHTML) {
		$INPUT{'Add'} =~ s/<!--([^>])*-->//g;
	}
	else {
		$INPUT{'Add'} =~ s/<([^>])*>//g;
		$INPUT{'Add'} =~ s/<//g;
		$INPUT{'Add'} =~ s/>//g;
	}
	$INPUT{'URL'} =~ s/\s//g;
	unless ($INPUT{'URL'} =~ /\*|(\.\.)|(^\.)|(\/\/\.)/
	  || $INPUT{'URL'} !~ /.*\:\/\/.*\..*/) {
		$URL = "$INPUT{'URL'}";
	}
	if ($INPUT{'FullText'} && !($URL)) {
		$time = time;
		$URL = "$DataDirURL/$time.html";
	}
	if ($INPUT{'RangeNumber'} && $INPUT{'RangeDay'}
	  && $INPUT{'FirstMonth'} && $INPUT{'LastMonth'}) {
		$Year = $INPUT{'FirstYear'};
		$Date = 1;
		$Month = int($INPUT{'FirstMonth'});
		if ($Year =~ /\D/) { $Year = 0; }
		elsif ($Year < 50) { $Year += 2000; }
		elsif ($Year < 100) { $Year += 1900; }
		$EndYear = $INPUT{'LastYear'};
		$EndDate = 1;
		$EndMonth = int($INPUT{'LastMonth'})+1;
		if ($EndMonth == 13) {
			$EndMonth = 1;
			$EndYear += 1;
		}
		if ($EndYear =~ /\D/) { $EndYear = 0; }
		elsif ($EndYear < 50) { $EndYear += 2000; }
		elsif ($EndYear < 100) { $EndYear += 1900; }
		if (($Year < 1601) || ($Year > 2899)
		  || ($EndYear < 1601) || ($EndYear > 2899)) {
			&Error_OutOfRange;
		}
		&PerpCal($Month,$Date,$Year);
		$StartDay = $perp_days;
		&PerpCal($EndMonth,$EndDate,$EndYear);
		$EndDay = $perp_days-1;
		if (($EndDay <= $StartDay) || (($EndDay-$StartDay)>3700)) {
			&Header("Invalid Date Range");
			print "<H1 ALIGN=CENTER>Invalid Date Range!</H1>\n";
			print "<P ALIGN=CENTER>Either your start date comes ";
			print "after your end date,<BR>or the range specified ";
			print "is too wide.<BR>";
			print "(&quot;Once a month&quot; entries can span ";
			print "up to 10 years.)\n";
			print "<P ALIGN=CENTER><EM>(Use your browser's ";
			print "&quot;Back&quot; button<BR>or just reload ";
			print "this page to try again!)</EM>\n";
			&Footer;
			exit;
		}
	}
	else {
		$Year = $INPUT{'StartYear'};
		$Date = int($INPUT{'StartDate'});
		$Month = int($INPUT{'StartMonth'});
		if (($Year == 0) && ($Year =~ /\D/)) { $Year = 0; $NewEntry = "0000"; }
		elsif ($Year < 0) { $Year = 1; }
		elsif ($Year < 50) { $Year += 2000; $NewEntry = $Year; }
		elsif ($Year < 100) { $Year += 1900; $NewEntry = $Year; }
		else { $NewEntry = $Year; }
		if (($Year != 0) && (($Year < 1601) || ($Year > 2899))) {
			&Error_OutOfRange;
		}
		if ($Month < 10) { $NewEntry .= "0"; }
		$NewEntry .= "$Month";
		if ($Date < 10) { $NewEntry .= "0"; }
		$NewEntry .= "$Date|$INPUT{'Add'}|$URL\n";
		if ($INPUT{'EndMonth'} && $INPUT{'EndDate'} && ($Year > 0)) {
			$EndYear = $INPUT{'EndYear'};
			$EndDate = int($INPUT{'EndDate'});
			$EndMonth = int($INPUT{'EndMonth'});
			if ($EndYear =~ /\D/) { $EndYear = 0; }
			elsif ($EndYear < 50) { $EndYear += 2000; }
			elsif ($EndYear < 100) { $EndYear += 1900; }
			if (($EndYear < 1601) || ($EndYear > 2899)) {
				&Error_OutOfRange;
			}
			&PerpCal($Month,$Date,$Year);
			$StartDay = $perp_days;
			&PerpCal($EndMonth,$EndDate,$EndYear);
			$EndDay = $perp_days;
			if (($EndDay <= $StartDay) || (($EndDay-$StartDay)>92)) {
				&Header("Invalid Date Range");
				print "<H1 ALIGN=CENTER>Invalid Date Range!</H1>\n";
				print "<P ALIGN=CENTER>Either your start date comes ";
				print "after your end date,<BR>or the range specified ";
				print "is too wide.<BR>";
				print "(Daily entries can span ";
				print "up to three months.)\n";
				print "<P ALIGN=CENTER><EM>(Use your browser's ";
				print "&quot;Back&quot; button<BR>or just reload ";
				print "this page to try again!)</EM>\n";
				&Footer;
				exit;
			}
		}
	}
	if ($EndDay > 0) {
		foreach $date ($StartDay..$EndDay) {
			&PerpCalRev($date);
			if ($perp_day == 1) {
				for $key (0..6) {
					$dow[$key] = 0;
				}
			}
			$perp_dow = $date - (int($date/7)*7);
			if ($perp_dow == 7) { $perp_dow = 0; }
			if ($MonSunWeek) {
				$perp_dow -= 1;
				if ($perp_dow == -1) { $perp_dow = 6; }
			}
			$dow[$perp_dow] += 1;
			if ($INPUT{'RangeNumber'} && $INPUT{'RangeDay'}) {
				next unless (($INPUT{'RangeNumber'} == 5)
				  || ($INPUT{'RangeNumber'} ==
				  $dow[$perp_dow]));
				next unless ($INPUT{'RangeDay'} ==
				  ($perp_dow+1));
				if ($DateSet) { $DateSet .= "<BR>"; }
				$DateSet .= "$perp_day ";
				$DateSet .=
				  "$shortmonths[$perp_mon-1] $perp_year";
			}
			$NextEntry = $perp_year;
			if ($perp_mon < 10) { $NextEntry .= "0"; }
			$NextEntry .= "$perp_mon";
			if ($perp_day < 10) { $NextEntry .= "0"; }
			$NextEntry .= "$perp_day|$INPUT{'Add'}|$URL\n";
			&AddEntry($NextEntry);
		}
	}
	else {
		&AddEntry($NewEntry);
	}
	if ($INPUT{'FullText'}) {
		if ($AllowHTML) {
			$INPUT{'FullText'} =~ s/<!--([^>]|\n)*-->/ /g;
		}
		else {
			$INPUT{'FullText'} =~ s/<([^>]|\n)*>/ /g;
			$INPUT{'FullText'} =~ s/\&/\&amp\;/g;
			$INPUT{'FullText'} =~ s/"/\&quot\;/g;
			$INPUT{'FullText'} =~ s/</\&lt\;/g;
			$INPUT{'FullText'} =~ s/>/\&gt\;/g;
		}
		$INPUT{'FullText'} =~ s/\cM\n*/\n/g;
		$INPUT{'FullText'} =~ s/\n/<BR>/g;
		$INPUT{'FullText'} =~ s/<BR>\s\s\s+/<BR><BR>/g;
		$INPUT{'FullText'} =~ s/<BR>\t/<BR><BR>/g;
		$INPUT{'FullText'} =~ s/\s+/ /g;
		$INPUT{'FullText'} =~ s/<BR>\s/<BR>/g;
		$INPUT{'FullText'} =~ s/\s<BR>/<BR>/g;
		$INPUT{'FullText'} =~ s/<BR><BR>/<P>/g;
		$INPUT{'FullText'} =~ s/<P><BR>/<P>/g;
		$INPUT{'FullText'} =~ s/\s+/ /g;
		$INPUT{'FullText'} =~ s/^\s+//g;
		$INPUT{'FullText'} =~ s/\s+$//g;
		$INPUT{'FullText'} =~ s/<P>/\n<P>/g;
		$INPUT{'FullText'} =~ s/<BR>/\n<BR>/g;
		$INPUT{'FullText'} =~ s/<P>\n//g;
		$INPUT{'FullText'} =~ s/<BR>\n//g;
		open (DATA,">$DataDirPath/$time.html");
		print DATA "<HTML><HEAD><TITLE>";
		print DATA "$INPUT{'Add'}</TITLE></HEAD>\n";
		print DATA "<BODY $bodyspec>\n";
		if ($DataDir_header) {
			open (HEADER,"$DataDir_header");
			@header = <HEADER>;
			close (HEADER);
			foreach $line (@header) {
				print DATA"$line";
			}
		}
		print DATA "<H1 ALIGN=CENTER>$INPUT{'Add'}</H1>\n";
		print DATA "<P ALIGN=CENTER><BIG><STRONG>";
		if ($DateSet) {
			print DATA "$DateSet";
		}
		else {
			print DATA "$Date $shortmonths[$Month-1] ";
			if ($Year == 0) { print DATA "Annually"; }
			else { print DATA "$Year"; }
			if ($EndDay) {
				print DATA " - $EndDate ";
				print DATA "$shortmonths[$EndMonth-1] $EndYear";
			}
		}
		print DATA "</STRONG></BIG>\n";
		print DATA "<P>$INPUT{'FullText'}\n";
		if ($DataDir_footer) {
			open (FOOTER,"$DataDir_footer");
			@footer = <FOOTER>;
			close (FOOTER);
			foreach $line (@footer) {
				print DATA"$line";
			}
		}
	}
	&Header("Entry Complete");
	print "<H1 ALIGN=CENTER>Entry Complete!</H1>\n";
	print "<P ALIGN=CENTER>The following entry has been added:\n";
	print "<P ALIGN=CENTER><STRONG>";
	if ($DateSet) {
		print "$DateSet";
	}
	else {
		print "$Date $shortmonths[$Month-1] ";
		if ($Year == 0) { print "Annually"; }
		else { print "$Year"; }
		if ($EndDay) {
			print " - $EndDate ";
			print "$shortmonths[$EndMonth-1] $EndYear";
		}
	}
	print "\n<P ALIGN=CENTER>";
	if ($URL) {
		print "<A HREF=\"$URL\">$INPUT{'Add'}</A>";
	}
	else {
		print "$INPUT{'Add'}";
	}
	print "</STRONG>\n";
	print "<CENTER><FORM METHOD=POST ACTION=$addcgiurl>\n";
	print "<INPUT TYPE=SUBMIT VALUE=\"Add Another Entry\">";
	print "</FORM></CENTER>\n";
	&Footer;
	exit;
}

sub AddEntry {
	local($Entry) = @_;
	$check = 0;
	open (DATA,$INPUT{'datafile'});
	@data = <DATA>;
	close (DATA);
	open (DATA,">$INPUT{'datafile'}");
	foreach $line (@data) {
		if ($line < $Entry) {
			print DATA "$line";
		}
		else {
			if ($check == 0) {
				print DATA "$Entry";
				print DATA "$line";
				$check = 1;
			}
			else {
				print DATA "$line";
			}
		}
	}
	if ($check == 0) {
		print DATA "$Entry";
	}
	close (DATA);
}

sub Error_OutOfRange {
	&Header("Date(s) Out of Range");
	print "<H1 ALIGN=CENTER>Date(s) Out of Range!</H1>\n";
	print "<P ALIGN=CENTER>Dates entered ";
	print "must be between 1601 and 2899 A.D.\n";
	print "<P ALIGN=CENTER><EM>(Use your browser's ";
	print "&quot;Back&quot; button<BR>or just reload ";
	print "this page to try again!)</EM>\n";
	&Footer;
	exit;
}

sub PerpCal {
	($perp_mon,$perp_day,$perp_year) = @_;
	%day_counts =
	  (1,0,2,31,3,59,4,90,5,120,6,151,7,181,
	  8,212,9,243,10,273,11,304,12,334);
	$perp_days = (($perp_year-1601)*365)+(int(($perp_year-1601)/4));
	$perp_days += $day_counts{$perp_mon};
	$perp_days += $perp_day;
	if (int(($perp_year-1600)/4) eq (($perp_year-1600)/4)) {
		if ($perp_mon > 2) {
			$perp_days++;
		}
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ((($perp_year == $key) && ($perp_mon > 2))
		  || ($perp_year > $key)) {
			$perp_days -= 1;
		}
	}
}

sub PerpCalRev {
	local($perp_days) = @_;
	%day_counts =
	  (1,0,2,31,3,59,4,90,5,120,6,151,
	  7,181,8,212,9,243,10,273,11,304,12,334);
	$perp_year = (int(($perp_days-1)/1461))*4;
	$perp_days = $perp_days-(int(($perp_days-1)/1461)*1461);
	if ($perp_days == 1461) {
		$perp_year = 1601+$perp_year+3;
		$perp_days = $perp_days-1095;
	}
	else {
		$perp_year = 1601+$perp_year+(int(($perp_days-1)/365));
		$perp_days = $perp_days-(int(($perp_days-1)/365)*365);
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ((($perp_year == $key) && ($perp_days > 59))
		  || ($perp_year > $key)) {
			$perp_days += 1;
		}
	}
	if ((int(($perp_year)/4) eq (($perp_year)/4))
	  && ($perp_days > 366)) {
		$perp_days -= 366;
		$perp_year += 1;
	}
	elsif ((int(($perp_year)/4) ne (($perp_year)/4))
	  && ($perp_days > 365)) {
		$perp_days -= 365;
		$perp_year += 1;
	}
	foreach $key (sort {$a <=> $b} keys %day_counts) {
		$perp_count = $day_counts{$key};
		if ((int(($perp_year)/4) eq (($perp_year)/4))
		  && ($key>2)) {
			$perp_count++;
		}
		if ($perp_days > $perp_count) {
			$perp_mon = $key;
			$perp_subtract = $perp_count;
		}
	}
	$perp_day = $perp_days-$perp_subtract;
}
