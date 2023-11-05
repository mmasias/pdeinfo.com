#!/usr/local/bin/perl5
# The above line may need to be changed to reflect the location of
# the perl interpreter on your system.  Use "which perl" on a Unix system
# to make a noble attempt to locate your perl interpreter.
# If you are on an NT system then you probably will not have to change
# the above line.

############################################################################
# This is a simple Perl CGI application that you can use to make sure that
# CGI scripts are working properly through your server.  If this script
# runs properly, you should see a web page that says "The Simple CGI Test
# script is functioning properly."
############################################################################

# HTTP 1.0 Header.
print "Content-type: text/html\n\n";

# Message body in HTML.
print "<html><head><title>Simple CGI Test</title></head><body>\n";
print "<center>\n";
print "The Simple CGI Test script is functioning properly.\n";
print "</center>\n</body></html>";
