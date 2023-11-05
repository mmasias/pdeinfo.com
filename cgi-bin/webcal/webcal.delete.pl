#!/usr/bin/perl

############################################
##                                        ##
##        WebCal (Deletion Script)        ##
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
	if ($name eq "Delete") {
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&amp;/&/g;
		push (@Delete,$value);
	}
	elsif ($name eq "datafile") {
		$INPUT{'datafile'} = $value;
	}
}

if (@Delete) { &Delete; }
else { &Display; }

sub Display {
	$datafiles = (keys %editfiles);
	unless ($INPUT{'datafile'}) {
		if ($datafiles > 1) {
			&Header("Select Data File");
			print "<H1 ALIGN=CENTER>Select Data File</H1>\n";
			print "<CENTER><FORM METHOD=POST ACTION=$deletecgiurl>\n";
			print "<P><STRONG>Data File to Edit:</STRONG> <SELECT NAME=\"datafile\">";
			foreach $key (sort keys %editfiles) {
				print "<OPTION VALUE=\"$key|$editfiles{$key}\">$key";
			}
			print "</SELECT>\n";
			print "<P><INPUT TYPE=SUBMIT VALUE=\"Select\">";
			print "</FORM></CENTER>\n";
			&Footer;
			exit;
		}
		else {
			foreach $key (keys %editfiles) {
				$INPUT{'datafile'} = "$key|$editfiles{$key}";
			}
		}
	}
	($datafilename,$datafilepath) = split(/\|/,$INPUT{'datafile'});
	open (DATA,$datafilepath);
	@data = <DATA>;
	close (DATA);
	&Header("Delete Calendar Entries");
	print "<H1 ALIGN=CENTER>Existing Calendar Entries:</H1>\n";
	print "<P ALIGN=CENTER><STRONG>Data File to Edit:</STRONG> $datafilename\n";
	print "<FORM METHOD=POST ACTION=$deletecgiurl>\n";
	print "<INPUT TYPE=HIDDEN NAME=datafile VALUE=\"$INPUT{'datafile'}\">\n";
	$lastyear = "";
	$eventcount = 0;
	foreach $line (@data) {
		next if ($line =~ /^\#/);
		next if (length($line) < 5);
		$eventcount++;
		$line =~ s/\n//g;
		$line =~ s/&/&amp;/g;
		$line =~ s/"/&quot;/g;
		$line =~ s/>/&gt;/g;
		$line =~ s/</&lt;/g;
		($date,$desc,$URL) = split (/\|/, $line);
		($dateyear,$datemonth,$dateday) = 
		  $date =~ m#(\d\d\d\d)(\d\d)(\d\d)#o;
		if ($dateyear < 1) { $dateyear = "Annual Events"; }
		unless ($lastyear eq $dateyear) {
			print "<P><BIG><STRONG>$dateyear:</STRONG></BIG>\n";
			$lastyear = $dateyear;
		}
		print "<BR><INPUT TYPE=CHECKBOX ";
		print "NAME=Delete VALUE=\"$line\"> ";
		$xshortmonth = @shortmonths[$datemonth-1];
		print "$xshortmonth $dateday: ";
		if ($URL) { print "<A HREF=\"$URL\">$desc</A>\n"; }
		else { print "$desc\n"; }
	}
	print "<CENTER>\n";
	unless ($eventcount) {
		print "<P>NO ENTRIES IN DATA FILE!";
	}
	else {
		print "<P><INPUT TYPE=SUBMIT ";
		print "VALUE=\"Delete Checkmarked Entries\">";
	}
	print "</CENTER></FORM>\n";
	if ($datafiles > 1) {
		print "<CENTER><FORM METHOD=POST ACTION=$deletecgiurl>\n";
		print "<INPUT TYPE=SUBMIT VALUE=\"Change Data File\">\n";
		print "</FORM></CENTER>\n";
	}
	&Footer;
	exit;
}

sub Delete {
	($datafilename,$datafilepath) = split(/\|/,$INPUT{'datafile'});
	open (DATA,$datafilepath);
	@data = <DATA>;
	close (DATA);
	open (DATA,">$datafilepath");
	foreach $line (@data) {
		if ($line =~ /\n$/) { chop ($line); }
		$deleteflag = 0;
		foreach $deleteline (@Delete) {
			if ($line eq $deleteline) {
				$deleteflag = 1;
			}
		}
		if ($deleteflag == 0) {
			print DATA "$line\n";
		}
	}
	close (DATA);
	if ($DataDirPath && $DataDirURL) {
		foreach $deleteline (@Delete) {
			$deleteline =~ s/^.*$DataDirURL/$DataDirPath/;
			unlink ($deleteline);
		}
	}
	&Display;
}

