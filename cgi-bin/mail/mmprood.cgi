#!/usr/bin/perl
#!c:/perl/bin/perl.exe
# The above line may need to be changed to reflect the location of
# the perl interpreter on your system.  Use "which perl" on a Unix system
# to make a noble attempt to locate your perl interpreter.  If you are
# installing this on an NT IIS server then you probably do not need to
# modify this line because it will most likely be ignored.  Apache under
# NT generally DOES require the top line to be configured.  We have provided
# two common paths above as examples, only the top line will be used, the
# second line is just there to provide an example.

############################################################################
# MailMan, Professional Edition, version 3.0.19
#
# Copyright (c) 1996 - 1999, Endymion Corporation. All rights reserved.
# Endymion Corporation: http://www.endymion.com/
# Originally by Ryan Alyn Porter, rap@endymion.com
#
# This product is not free and is not in the public domain.
# For detailed information on the licensing structure of MailMan, see
# http://www.endymion.com/products/mailman/
#
# Initiated:      9/07/1997 Version 1.1
# Re-awakened:    4/24/1998 Version 2.0 beta
# Released:       7/20/1998 Version 2.0
# Last Modified:  1/04/2000 Version 3.0.19
############################################################################

# If you are having problems with MailMan not working at all, please
# take a look at the MailMan FAQ, stored online at
# http://www.endymion.com/products/mailman/faq.htm.  A version of the FAQ
# should also have been in the distribution that contained this file.

package mailman;

# Enable these while you are working on modifications.  Make absolutely
# certain that 'use strict' is NOT enabled in production installations.
# CGI.pm and 'use strict' are not compatible, if you have 'use strict'
# enabled then your users will not be able to upload files because CGI.pm
# provides uploaded files using a bizarre on-the-fly file handle that will
# cause an error if you have 'use strict' enabled.  We think that this is
# ugly too, but there is no way around it at the moment.
#use strict;
#$^W = 1; # Warnings.

# Version information that might find its way into output.
$mailman::strMailManVersion = 'v3.0.19';
$mailman::strMailManEdition = 'Professional Edition';

# Variable initialization.  Clean and neat and all, but very necessary
# for mod_perl.
InitializeVars();

############################################################################
# This section contains a few variables that you might need to set  in order
# to get MailMan functioning properly.  If your installation is working,
# then you don't need to worry about any of these.
############################################################################

# Local Location Users
# IMPORTANT: Set this variable to point to a directory that you have 
# set up as the user storage area.  Make sure that your web user has
# read and write access to this directory.  This needs to be a path
# that makes sense at runtime for the web user, probably an absolute
# path like '/something/somewhere/mailman/users/' or 
# "C\:\\mailman\\users\\".  Note the terminal slash at the end.  That's
# important.  It won't work without that slash.  You probably shouldn't
# be storing your user messages in publicly readable areas of your
# web server for obvious security reasons, but some people don't have the
# option.  Just use your head, and ask us if you have any questions.
# Also PLEASE remember that the data that MailMan writes to this
# directory should be considered irreplacable user data and should be
# handled and backed up appropriately.
$mailman::strLocalLocationUsers = 'users/';

# User Disk Quota
# This is fairly self-explanatory, it's the number of bytes that users
# are allowed to use on your HTTP server for storing messages.  If this
# value is set to zero then no quota will be maintained and users will
# never see quota status indicators.  You can turn this on and off and
# mess with the size at will, but note that if you decrease the quota
# size after users have downloaded stuff then you could put some users
# over quota.  We have taken care to gracefully handle this situation
# but your users might not think that things look very graceful when that
# happens.  Remember to set this in bytes.  1024*1024 bytes in a megabyte,
# some common values are as follows:
# 1  MB = 1048576 B
# 2  MB = 2097152 B
# 5  MB = 5242880 B
# 10 MB = 10485760 B
# Note that there are a couple of ways that a user can go slightly
# over quota.  MailMan allows this in cases like the storage of an
# outgoing message and the like where recovery from a quota error
# would be very difficult and un-graceful.  Quotas are primarily
# enforced when a user downloads new messages.  If you notice that a
# particular user has gone slightly over 100% of his/her quota, please
# don't consider that a bug in MailMan.  We have intentionally set things
# up this way.  This is a hint to administrators to allow for a little
# more room on storage systems than the sum of all users' quotas.
$mailman::iUserDiskQuota = 5242880;

# Management Password
# This password must be included in any query to verify or repair
# the message store database.
$mailman::strManagementPassword = 'changethis';

# Download Individual Accounts
# Use this variable to tell MailMan that it should only download messages
# from external accounts when the user explicitly issues a LOADACCOUNT
# command.  If this value is not set, MailMan will automatically download
# messages from all of a user's accounts when they log in.
#$mailman::bDownloadIndividualAccounts = 1;

# Case Insensitive Accounts
# This variable is used to indicate to MailMan that the POP3 account
# names are case insensitive, so "BOB", "Bob" and "bob" are all considered
# the same POP3 user.  This is important in locating the user's persistent
# information such as the message archive and the user's properties files.
$mailman::bCaseInsensitiveAccounts = 1;

# Location Attachments
# When a user selects an attachment from a message for downloading,
# MailMan generates that attachment on-the-fly and sends it through the
# HTTP server to the user's browser.  MailMan includes the necessary
# HTTP header information for the user's browser to determine the
# file name, but many broswers, most notably Microsoft's Internet
# Explorer, either ignore these headers or just don't handle them
# very well.  The result is that when a user downloads an attachment,
# your browser may present the user with a "Save As" box with the
# file name filled in as the name of this script, a string or random
# characters, or any number of other un-graceful things.  We think that
# the best solution to this problem would be for browser makers to
# pay attention to HTTP headers, but until then we provide a mechanism
# for working around the problem.  If you set up a directory that is
# writable by MailMan and readable by your web server, then MailMan
# will write out the attachment file to that directory temporarily,
# and redirect the user's browser to that file.  When the user logs
# in or out MailMan will ensure that the user's files in this
# temporary directory are removed.  A user that exits MailMan without
# logging out and never logs back in could potentially leave stale
# attachment files on the server, so occasional monitoring of the
# temporary directory for stale files would be appropriate.  Also note
# that this mechanism could be considered a privacy problem since a
# user's attachments are deposited temporarily into a world-readable
# directory rather than generated on-the-fly the way MailMan normally
# would do.  We have left the decision up to each individual
# administrator as to whether or not to use this feature.  Most people
# seem to prefer allowing MailMan to generate attachments on-the-fly
# for simplicity, ease of administration, and security/privacy, but
# some people think that the attachment file name thing is a critical
# issue.  The decision is yours.
# To use this feature, create a directory that is readable by your
# web server and writable by the user that MailMan runs as.  Set
# $mailman::strLocalLocationAttachments to the local path name of 
# this directory, for instance
# $mailman::strLocalLocationAttachments = '/public_html/attachtmp/';
# Then set $mailman::strURLLocationAttachments to the URL location
# of this directory, for instance
# $mailman::strURLLocationAttachments = '/attachtmp/';
# Note the terminal slashes at the end, those are necessary.  Just
# set and uncomment the following lines to use this feature:
#$mailman::strLocalLocationAttachments = 'c:/www/public_html/mailman/tmp/';
#$mailman::strURLLocationAttachments = '/mailman/tmp/';

# Local File Permissions
# Use this if you want to modify the permissions that files and
# directories created by MailMan use.  This will only make much sense
# to Unix and Unix-like operating systems.  If this value is not set,
# nothing will happen.  This should be an octal integer as in the
# example below, not a string.
$mailman::iLocalFilePermissions = 0666;

# Local Directory Permissions
# Same as above, used for directories created by MailMan.
$mailman::iLocalDirectoryPermissions = 0777;

# Outgoing Banner Text
# This is the banner that is appended to the end of any message that
# this MailMan installation sends.  One reason why this is one of the
# first configuration options is because we want to make it very 
# obvious that you can remove or modify this banner.  Endymion places
# no restrictions at all on this banner, so don't worry about leaving
# credit to us in here or anything like that.  Please feel free to 
# change this to whatever you like, or completely remove it.  If this
# value is not defined then it will simply append no banner.
$mailman::strOutgoingBannerText = 
    "\n" .
    "---------------------------------------------\n" .
    "This message was sent using Endymion MailMan.\n" .
    "http://www.endymion.com/products/mailman/\n";

# Incoming Mail Server:
# The way that we originally intended to allow people to 'rig' the server
# names for an installation was through simple template modifications, as
# mentioned in the FAQ.  A lot of people have asked about ways to rig the
# server names in the script itself though, so we added this.  We aim to
# please...  If you want to rig your incoming server name so that it makes
# no difference at all what an incoming form specifies, just un-comment
# this line and specify it.
#$mailman::strIncomingServer = 'mail.endymion.com';

# Outgoing Mail Server:
# Same deal, different server.
#$mailman::strOutgoingServer = 'mail.endymion.com';

# From Domain Name:
# Set this variable to override the domain name that is assumed when a
# user logs in.  For instance, when the user "rap" logs into the POP3
# server "mail5.it.endymion.com", MailMan will assume that his address
# is "rap@mail5.it.endymion.com".  If you set this variable to
# "endymion.com", then it will assume that his address is
# "rap@endymion.com" instead.  If the mapping between POP3 user names
# and email addresses is more complicated then you will need to actually
# build your own routines to do the mapping.  For instance, if the user
# "endy-rap" at the POP3 server "shell1.ba.best.com" actually receives
# mail at the address "rap@endymion.com", then you will need to do make
# your own custom mapping routine to deal with this.
#$mailman::strFromDomainName = "endymion.com";

# From Domain Trim:
# If the above option doesn't work for you, you can set this value to
# instruct MailMan to trim the machine name when it derives the 'from'
# email address.  The number that you set this to represents the total
# number of names to shear off of the left-hand side of the machine
# name.  For instance, if the user's POP3 server name is
# "mail.rex.endymion.com", and you set this value to 0, the default,
# then when the user composes a message MailMan will guess
# "username@mail.rex.endymion.com" as the 'from' address.  If you set
# this value to 1 then it will guess "username@rex.endymion.com", if
# you set it to 2 then it will guess "username@endymion.com", etc.  This
# can be helpful if you have a number of different virtual domains
# and you want the email address to be inferred dynamically, rather
# than by hard-coding it with the "From Domain Name" configuration value.
$mailman::iFromDomainTrim = 0;

# Outgoing Domain Name:
# When a user specifies a recipient name without full domain qualification
# ("rap" instead of "rap@endymion.com", for example) then the SMTP server
# should provide configuration rules for determining how to deal with this
# mail.  It should not be the responsibility of the mail client to fill in
# a complete address.  We have had many requests for a feature to allow 
# an administrator to specify a default domain name, however, and we aim
# to please.  This configuration variable is the result.  If you want
# MailMan to assume a default domain name when it is given an incomplete
# address, uncomment this line and set it to your domain name.  We strongly
# recommend against this, however, you should be looking into your SMTP
# server's configuration options and not using this feature.
#$mailman::strOutgoingDomainName = 'endymion.com';

# Messages Per Page:
# This value controls the number of messages returned per page in a
# message list.  Adjust it if you like.
# The user has the option of overriding this value in the user preferences
# page.  If you don't want them to be able to do this you can hide that
# field in your templates.
$mailman::iMessagesPerPage = 10;

# Local Template Location:
# If you have a web server that sets the current directory to something
# strange, you can set this to an absolute path to make it easier to
# allow MailMan to find the templates.  Just set this variable to an
# absolute path like "C\:\\inetpub\\wwwroot\\mailman\\templates\\"
# or '/usr/home/rap/mailman/' or whatever.  Note the final slash, that's
# important.  If you leave it out then things won't work.  If you need
# to set this value, then un-comment the following line:
#$mailman::strLocalTemplateLocation = "D:/inetpub/wwwroot/Endymion2/products/mailman/demo/";

# Local Script Location:
# If your server is one of the ones that causes problems that require the
# above value to be set, then you might also need to set this value.  In
# most cases your script location and your template location will be 
# identical, but if you move your templates to a different directory than
# your script for whatever reason, then you will need to set this.  If you
# have no idea what I'm talking about, you should probably just leave this.
$mailman::strLocalScriptLocation = $mailman::strLocalTemplateLocation;

# URL Image Location:
# Use this to rig the URLs that will be used to access the images that
# the templates point to.  This value will be prepended to any value in
# the templates of the form ""i_*.gif"" (including the inner quotes).
# If you have customized your templates and your own custom images are
# not showing up in MailMan's output, it is probably because the custom
# images that you are using are not named "i_*.gif".
# To use this variable, set it to the exact value that you want prepended
# to image names in order to make them into URLs that will point to your
# image directory.  For instance, if you bury your images in an "images"
# directory under the directory where MailMan is installed, set this to
# 'images/' (with the slash).  If you put your images in a completely
# different directory, something that is rooted, like '/mailman/images/'
# might be what you are looking for.  In the most extreme cases you can
# do away with relative URLs entirely and provide a complete absolute URL
# like the one below
#$mailman::strURLImageLocation = 'http://www.endymion.com/images/';

# Use Perl 'alarm()' function:
# Set this to true if your Perl interpreter supports "alarm".  As of this
# Writing, NT Perl does not.  If this is not set, MailMan will not be able
# to timeout when a server hangs.  The OSSettings() routine will attempt
# to set this variable, but you can override it here if you want.
# The point of the "alarm" feature as used in MailMan is to allow MailMan
# to detect when a mail server has not responded within a reasonable
# amount of time.  If your server's Perl interpreter does not support
# "alarm", then MailMan will still work, but if a mail server ever does
# not respond then the user will get no feedback to that effect.
#$mailman::bUseAlarm = 1;

# Timeout Duration:
# The aforementioned timeout delay.  Set this to something else to modify
# how long MailMan will sit around waiting for a mail server to respond.
# Only works if $mailman::bUseAlarm is set to something.
$mailman::iTimeoutDurationInSeconds = 180;

# Use Perl 'crypt()' function:
# Some Perl impelentations apparently do not support the crypt() function.
# We have never seen one, and there are plenty of implementations out there
# that you should be able to find a good one, but we try to accomodate
# anyway.  Comment out this line if your Perl implementation is breaking
# on the crypt() function.  Be warned that if you do this your users'
# usernames and passwords will be less obfuscated than they were before,
# which admittedly wasn't much.  This is a good place to repeat the 
# suggestion that MailMan is an excellent candidate for SSL and other
# fancy HTTP security mechanisms.
#$mailman::bUseCrypt = 1;

# Use Hijack Test:
# MailMan performs a test to determine if the current session has been
# hijacked by a different user from a different address.  On a few 
# systems this will not work because of the configuration.  If your
# MailMan installation sits behind a cluster of caching proxy servers
# for load balancing, for instance.  If you want to disable the hijack
# checking functionality, just comment out this line.
#$mailman::bUseHijackTest = 1;

# Kiosk Mode:
# If you are using MailMan in a kiosk environment, it will generally
# be possible for a user to use a combination of "BACK" and "RELOAD" in
# the kiosk web browser to intrude backwards into the mail sessions of
# previous users.  If you set this value then MailMan will operate in
# kiosk mode, which means that when a user logs in, MailMan will create
# a new browser window with that user's session.  If the user logs out
# then that window will close, and the user's history information will
# go with the window so that intrusions with "BACK" and "RELOAD" aren't
# possible.  We recommend against using this feature for installations
# that are not kiosk-based because it relies on Javascript and cookies,
# which does not leave users with older browsers with a way in.  If you
# are in a kiosk environment then you have control over the browser an
# that's not a problem.  We strongly recommend against using the
# Microsoft Internet Explorer for kiosk environments because it does not
# properly respect the "Expires:" and "Cache-control:" HTTP headers, so
# IE will cache user mail to the hard drive whether you want it to or
# not.  Microsoft appears to have no interest in fixing this problem.
# IE 4 SP1 pretty consistently crashed during our tests of the 
# full-screen popup window kiosk mode, too, which is likely not exactly
# the behavior that you are looking for in your kiosk browser.
# The kiosk mode feature primarily activates and deactivates sections
# of outbound templates, so if you have customized your templates before
# you decided to use kiosk mode then it is entirely possible that you
# broke this mode by removing vital Javascript.  Consult the
# out-of-the-box template set for examples of the Javascript snippets
# necessary for this mode.
#$mailman::bKioskMode = 1;

############################################################################
# You should not have to configure any values after this line.
############################################################################

use Socket; use FileHandle; my($mma) = new FileHandle(); use CGI;
my($mmb) = new CGI; {  my(@mmc) = $mmb->param; my($mmd) = 0;
for($mmd=0;$mmd<$#mmc+1;$mmd++) { my($mme) = $mmc[$mmd];;
if($mme =~ /^(.+)\.[xy]$/) { my($mmf) = $1; if($mme =~ /^([^\#]+)\#(.*)\.[xy]$/) {
$mmf = $1; $mmb->param($mmf,mmsw($2)); } else {
$mmb->param($mmf,'MAILMANSPECIALTRUE'); } $mmb->delete("${mmf}.x");
$mmb->delete("${mmf}.y"); } else { if($mme =~ /^([^\#]+)\#(.*)$/) {
$mmb->param($1,mmsw($2)); } } } } if($mmb->param('INTERFACE')) {
my(@mmg) = split(/\&/,$mmb->param('INTERFACE')); my($mmh) = '';
foreach $mmh (@mmg) { if($mmh =~ /^([^\=]+)\=(.*)$/) {
$mmb->param($1,mmsw($2)); } }
unless($mmb->param('INTERFACE') =~ /ALTERNATE_TEMPLATES/) {
$mmb->param('ALTERNATE_TEMPLATES',''); } } {
@mailman::mmi = split(/\;/,$ENV{'HTTP_COOKIE'}); my($mmj) = '';
foreach $mailman::mmj (@mailman::mmi) { $mailman::mmk = 1;
if($mailman::mmj =~ /MailManAuth\=(\S+)/) { my(@mml) = split(/\&/,$1);
my($mmm) = ''; foreach $mmm (@mml) { $mmm =~ /^(.+)\#(.+)$/; unless($mmb->param($1))
{ $mmb->param($1,$2); } } } if($mailman::mmj =~ /MailManDir\=(\S+)/) {
$mailman::mmn = mmsw($1); } } }
$mailman::mmo = mmta($mmb->param('USERNAME'));
$mailman::mmo =~ s/^\s*([^\s]+)\s*$/$1/; 
$mailman::mmp = mmsz($mailman::mmo);
$mailman::mmq = mmta($mmb->param('PASSWORD'));
$mailman::mmq =~ s/^\s*([^\s]+)\s*$/$1/; 
$mailman::mmr = mmsz($mailman::mmq); unless($mailman::strIncomingServer) {
$mailman::strIncomingServer =  mmta($mmb->param('SERVER'));
$mailman::strIncomingServer =~ s/^\s*([^\s]+)\s*$/$1/;  }
$mailman::mms = mmsz($mailman::strIncomingServer);
unless($mailman::strOutgoingServer) {
$mailman::strOutgoingServer = $mmb->param('OUTGOING');
$mailman::strOutgoingServer =~ s/^\s*([^\s]+)\s*$/$1/;  } $mailman::mmt = '';
unless($mailman::strLocalLocationUsers =~ /[\/\\]$/) {
$mailman::strLocalLocationUsers .= '/'; } $mailman::mmu = $mailman::mmo . '@' .
$mailman::strIncomingServer; $mailman::mmu =~ tr/[A-Z]/[a-z]/;
$mailman::mmv = $mailman::strLocalLocationUsers . mmsv($mailman::mmu);
if(defined($mailman::strLocalLocationAttachments) &&
defined($mailman::strURLLocationAttachments)) {
unless($mailman::strLocalLocationAttachments =~ /[\/\\]$/) {
$mailman::strLocalLocationAttachments .= '/'; }
unless($mailman::strURLLocationAttachments =~ /[\/\\]$/) {
$mailman::strURLLocationAttachments .= '/'; } $mailman::mmw =
$mailman::strLocalLocationAttachments . mmsv($mailman::mmo .
'@' . $mailman::strIncomingServer); $mailman::mmx =
$mailman::strURLLocationAttachments . mmsv(
mmsv($mailman::mmo . '@' . $mailman::strIncomingServer));
$mailman::mmy = 1; } $mailman::mmz = mmsu($ENV{SERVER_NAME},42);
$mailman::mmz .= mmsu($ENV{REMOTE_HOST} . $ENV{REMOTE_ADDR},69);
$mailman::mmaa = mmsz($mailman::mmz); mmst();
$mailman::mmab = $ENV{SCRIPT_NAME}; unless($mailman::mmab =~ /^\//) {
$mailman::mmab = "/$mailman::mmab"; } $mailman::mmac = $mailman::mmab;
$mailman::mmac =~ s/^(.*[\\\/])[^\\\/]+$/$1/; if($mailman::mmac eq '/') {
$mailman::mmad = ''; } else { $mailman::mmad = "path=$mailman::mmac; "; }
sub mmpz { if($mmb->param('NOFRAMES')) { $mailman::mmae = 1; }
if($mmb->param('NOCACHE')) { $mailman::mmaf = 1; }
if(defined($mmb->param('ALTERNATE_TEMPLATES'))) { $mailman::mmag = 
$mmb->param('ALTERNATE_TEMPLATES'); } if(!defined($mailman::mmah)) {
$mailman::mmah = mmsw($mmb->param('FOLDER')); }
if(($mailman::mmah eq '') && ($mailman::mmn ne '')) {
$mailman::mmah = $mailman::mmn; } } sub mmqa { my($mmai) = shift;
my(@mmc) = $mmb->param; my($mmd) = 0; for($mmd=0;$mmd<$#mmc+1;$mmd++) {
my($mme) = $mmc[$mmd];; if($mme =~ /^$mmai\:(.*)$/) { return $1; } } return; }
mmpz(); mmqb(); { my($mmj) = '';
@mailman::mmi = split(/\;/,$ENV{'HTTP_COOKIE'});
foreach $mailman::mmj (@mailman::mmi) { if($mailman::mmj =~ /MailManCmds\=(\S+)/) {
my($mmaj) = ''; @mailman::mmak = split(/\&/,$1); foreach $mmaj (@mailman::mmak) {
$mmaj =~ /^(.+)\#(.+)$/; unless($mmb->param($1)) { $mmb->param($1,$2); } } } } }
mmpz(); mmqb(); mmqe();
sub mmqb { my($mmal) = ''; if($mmb->param('BLANK')) {
mmss('t_blank.htm'); } if($mmb->param('MENU')) {
mmss('t_f_menu.htm'); } if($mmb->param('LOGOUT')) { if($mailman::mmy) {
mmtq(); } if($mailman::bKioskMode) {
print "Set-cookie: MailManAuth=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n";
print "Set-cookie: MailManCmds=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n";
print "Set-cookie: MailManDir=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n"; $mailman::mmo = '';
mmss('t_closewindow.htm'); } else { mmqe(); } }
if($mmb->param('START')) { mmqe(); } if($mmb->param('PREFERENCES')) {
mmqv(); } if($mmb->param('SAVEPREFERENCES')) { mmqw();
$mailman::mmam = $mmb->param('PREF_REALNAME');
$mailman::mman = $mmb->param('PREF_EMAIL');
$mailman::mmao = $mmb->param('PREF_SIGNATURE');
$mailman::mmap = $mmb->param('PREF_OUTGOING');
if($mmb->param('PREF_NUMPERPAGE') =~ /^\s*(\d+)\s*$/) { $mailman::mmaq = $1; }
if($mmb->param('PREF_DELETEDOWNLOAD')) { $mailman::mmar = 1; } else {
$mailman::mmar = 0; } if($mmb->param('PREF_DELETEPROXY')) { $mailman::mmas = 1; } else
{ $mailman::mmas = 0; } if($mmb->param('PREF_DELETESAVE')) { $mailman::mmat = 1; } else
{ $mailman::mmat = 0; } if($mmb->param('PREF_SENDSAVE')) { $mailman::mmau = 1; } else {
$mailman::mmau = 0; } if($mmb->param('PREF_STARTUP')) { $mailman::mmav =
$mmb->param('PREF_STARTUP'); } mmqx(); $mmb->param('LOGIN',1); }
if($mmb->param('FOLDERS')) { mmqu(); } if($mmb->param('FOLDERCHANGE')) {
if($mmb->param('FOLDERCHANGE') ne 'MAILMANSPECIALTRUE') {
$mailman::mmah = mmsw( $mmb->param('FOLDERCHANGE')); }
elsif(defined($mmb->param('FOLDERCHANGELIST')) &&
!($mmb->param('FOLDERCHANGELIST') eq 'MAILMANSPECIALSELECT')) { $mailman::mmah =
mmsw($mmb->param('FOLDERCHANGELIST')); }
if($mmb->param('FRAMERELOAD') && !($mailman::mmae)) {
mmss('t_f_frameset.htm'); } else { if($mailman::mmah eq 'INBOX') {
mmql(); } mmrn(); } } if($mmb->param('FOLDERNEW')) {
if($mmb->param('FOLDERNEWNAME')) { $mailman::mmah = $mmb->param('FOLDERNEWNAME');
mmqj(); mmqk(); } mmqu(); }
if($mmb->param('FOLDERDELETE')) { my($mmaw) = $mailman::mmv . '/' .
mmsv($mmb->param('FOLDERDELETE')); if(mmth($mmaw) == 0 &&
-d $mmaw) { opendir(DELETEDIR, $mmaw); my(@mmax) = readdir(DELETEDIR);
closedir(DELETEDIR); my($mmay); foreach $mmay (@mmax) { unlink("${mmaw}/${mmay}"); }
rmdir($mmaw); } $mailman::mmah = 'INBOX'; mmqu(); }
if($mmb->param('ADDRESSES')) { mmqy(); }
if($mmb->param('ADDRESSCOMPOSE')) { my($mmaz) = ''; my($mmba) = '';
$mmba = $mmb->param('ADDRESSCOMPOSE'); mmqz();
if(defined($mailman::mmbb{$mmba})) { my($mmbc) =
$mailman::mmbb{$mmba}->{'FIRSTNAME'}; my($mmbd) =
$mailman::mmbb{$mmba}->{'LASTNAME'}; my($mmbe) =
$mailman::mmbb{$mmba}->{'ADDRESS'}; $mmaz =  "$mmbc $mmbd " .
"&lt;$mmbe&gt;"                } mmra();
if(defined($mailman::mmbf{$mmba})) { $mmaz = $mailman::mmbf{$mmba};
$mmaz =~ s/(\r\n)|(\r\n)/,\ /g;  $mmaz =~ s/[\r\n]/,\ /g;        
$mmaz =~ s/\,\ $//g; } mmsj('NEW',undef,undef,$mmaz); }
if($mmb->param('ADDRESSESNEWINDIVIDUAL')) { mmrb(); }
if($mmb->param('ADDRESSDELETEINDIVIDUAL')) { mmrd(
$mmb->param('ADDRESSDELETEINDIVIDUAL')); mmqy(); }
if($mmb->param('ADDRESSINDIVIDUAL')) { mmrb(); }
if($mmb->param('SAVEADDRESSINDIVIDUAL')) { mmrf();
mmqy(); } if($mmb->param('ADDRESSESNEWGROUP')) {
mmrc(); } if($mmb->param('ADDRESSDELETEGROUP')) {
mmre( $mmb->param('ADDRESSDELETEGROUP')); mmqy(); }
if($mmb->param('ADDRESSGROUP')) { mmrc(); }
if($mmb->param('SAVEADDRESSGROUP')) { mmrg(); mmqy(); }
if($mmb->param('ACCOUNTS')) { mmrh(); } if($mmb->param('ACCOUNTNEW')) {
mmri(); } if($mmb->param('ACCOUNTDELETE')) {
mmrk($mmb->param('ACCOUNTDELETE')); mmrh(); }
if($mmb->param('SAVEACCOUNT')) { mmrj(); mmql();      
mmrh(); } if($mmb->param('ACCOUNT')) { mmri(); }
if($mmb->param('DELETEACCOUNT')) { mmrk( $mmb->param('DELETEACCOUNT'));
mmrh(); } if($mmb->param('LOGIN')) { my($mmbg) = '';
if($mmbg = mmqg()) { if(defined($mmbg)) { $mmbg =~ s/^\-ERR(.*)$/$1/; }
$mailman::bKioskMode = 0; $mailman::mmbh{'GREETING'} = 
"<center><b>Log In Error: </b><i>$mmbg</i></center>";
mmss('t_login.htm',\%mailman::mmbh); }

if(mmrt() <= 0){ mmrq(); exit(0); }
 if($mailman::mmy) {
mmtq(); } mmqw(); if($mailman::mmae) {
mmql(); if($mailman::mmav eq 'FOLDERS') { mmqu(); }
else { mmrn(); } } else { if($mailman::mmav eq 'FOLDERS') {
mmqu(); } else {

print eval(mmrs($mailman::mhaa[0]));
 } } } if($mailman::bUseHijackTest && 
$mmb->param('CHECKSUM') &&  $mmb->param('CHECKSUM') ne '') {
if(mmta($mmb->param('CHECKSUM')) ne $mailman::mmz) { mmqc(
qq|Your MailMan session was initiated from a different network address than\n| .
qq|your current location.  For security reasons, MailMan will not continue.\n| .
qq|You must <a href="MailMan(ME)?LOGOUT=TRUE" target="_top">log in again</a>\n| .
qq|from this location to continue.\n| ); } } if($mmb->param('RELOAD')) {
if($mailman::mmae) { mmql(); mmrn(); } else {
mmss('t_f_frameset.htm'); } } if($mmb->param('LOADACCOUNT')) {
mmqm($mmb->param('LOADACCOUNT')); if($mailman::mmae) {
mmrn(); } else { mmss('t_f_frameset.htm'); } }
if($mmal = mmqa('LIST')) { if($mailman::mmah eq 'INBOX' ||
$mailman::mmah eq '') { mmql(); } mmrn($mmal); }
if($mmb->param('LIST')) { if($mailman::mmah eq 'INBOX' || $mailman::mmah eq '') {
mmqn(); } mmrn(); }
my($mmbi) = $mmb->param('BACKGROUND'); if($mmbi) { if($mailman::mmae) {
print "Location: $mmbi\n\n"; exit(0); } else { mmrm($mmbi); } }
if($mmbi = $mmb->param('BACKGROUNDFRAME')) {
mmss('t_backgroundframe.htm'); } if($mmal = mmqa('SHOW')) {
my($mmbj) = -1; if($mmal =~ /^(.+)mimepart\:(.+)$/) { $mmbj = $1;
$mailman::mmbk = $2; $mailman::mmbk =~ s/%(..)/pack("c",hex($1))/ge; } else {
$mmbj = $mmal; } $mmbj = mmsw($mmbj); mmsb($mmbj,0); }
if($mmal = mmqa('SOURCE')) { my($mmbj) = mmsw($mmal);
mmsc($mmbj); } if($mmal = mmqa('PREV')) {
my($mmbj) = mmsw($mmal); mmsb($mmbj,-1); }
if($mmal = mmqa('NEXT')) { my($mmbj) = mmsw($mmal);
mmsb($mmbj,1); } if($mmal = mmqa('DELETE')) {
my($mmbg) = mmqg(); if($mmbg) { mmqc($mmbg); }
my($mmbj) = mmsw($mmal); mmse($mmbj);
mmqf($mma,"QUIT"); close $mma; $mailman::mmbl = 0; if($mailman::mmae) {
mmrn(); } else { mmss('t_f_frameset.htm'); } }
if($mmb->param('DELETEMARKED')) { my($mmbg) = ''; if($mmbg = mmqg()) {
mmqc($mmbg); } my(@mmc) = $mmb->param; my($mmd) = 0;
for($mmd=0;$mmd<$#mmc;$mmd++) { my($mme) = $mmc[$mmd];; if($mme =~ /^MARK\:(.*)$/) {
mmse(mmsw($1)); } } mmqf($mma,"QUIT"); close $mma;
$mailman::mmbl = 0; if($mailman::mmae) { mmrn(); } else {
mmss('t_f_frameset.htm'); } } if($mmal = mmqa('MOVE')) {
my($mmbm) =  mmsv($mmb->param('FOLDERTRANSFERLIST'));
if($mmbm eq 'MAILMANSPECIALSELECT' || $mmbm eq '') { mmrn(); }
my($mmbg) = ''; if($mmbg = mmqg()) { mmqc($mmbg); }
my($mmbj) = mmsw($mmal); if(mmsh($mmbj,$mmbm)) {
mmsf($mmbj,'MOVED'); } mmqf($mma,"QUIT"); close $mma;
$mailman::mmbl = 0; if($mailman::mmae) { mmrn(); } else {
mmss('t_f_frameset.htm'); } } if($mmb->param('MOVEMARKED')) { my($mmbm) =
mmsv($mmb->param('FOLDERTRANSFERLIST'));
if($mmbm eq 'MAILMANSPECIALSELECT' || $mmbm eq '') { mmrn(); }
my($mmbg) = ''; if($mmbg = mmqg()) { mmqc($mmbg); }
my(@mmc) = $mmb->param; my($mmd) = 0; for($mmd=0;$mmd<$#mmc;$mmd++) {
my($mme) = $mmc[$mmd];; if($mme =~ /^MARK\:(.*)$/) {
my($mmbj) = mmsw($1); if(mmsh($mmbj,$mmbm)) {
mmsf($mmbj,'MOVED'); } } } mmqf($mma,"QUIT"); close $mma;
$mailman::mmbl = 0; if($mailman::mmae) { mmrn(); } else {
mmss('t_f_frameset.htm'); } } if($mmb->param('NEW')) {
$mmb->param('ATTACH',0); mmsj('NEW',0,0);    }
if($mmb->param('USEATTACH')) { $mmb->param('ATTACH',1); mmsk(''); }
if($mmal = mmqa('REPLY')) { my($mmbj) = mmsw($mmal);
mmsj($mmbj,0,0); } if($mmal = mmqa('REPLYALL')) {
my($mmbj) = mmsw($mmal); mmsj($mmbj,1,0); }
if($mmal = mmqa('FORWARD')) { my($mmbj) = mmsw($mmal);
mmsj($mmbj,0,1); } if($mmb->param('SEND')) { mmsm(); }
if($mmb->param('HELP')) { mmss('t_help.htm'); } if($mmb->param('VERIFY')) {
print "Content-type: text/html\n\n"; unless($mmb->param('PASSWORD') eq
$mailman::strManagementPassword) { print "Authentication Error:\n" . 
"To use management features, the supplied password\n" .
"must match the management password for this installation.\n"; exit(0); }
$mailman::mmbn = 0; print "<pre>\n"; mmtl(); print "</pre>\n"; exit(0); }
if($mmb->param('REPAIR')) { my(@mmbo) = (); print "Content-type: text/plain\n\n";
unless($mmb->param('PASSWORD') eq $mailman::strManagementPassword) { print
"Authentication Error:\n" . 
"To use management features, the supplied password\n" .
"must match the management password for this installation.\n"; exit(0); }
$mailman::mmbn = 1; print "<pre>\n"; mmtl(); print "</pre>\n"; exit(0); } }
sub mmqc { my($mmbp,$mmbq) =  @_; my($mmbr) = ''; if($mmbp eq "ALRM") {
if($mailman::bUseAlarm){ alarm(0); } $mmbp = $mailman::mmbs;
mmqf($mma,"QUIT"); close $mma; } if($mailman::mmae) {
$mmbr = 't_nf_error.htm'; } else { $mmbr = 't_f_error.htm'; } my(%mmbh);
$mmbh{'ERROR'} = $mmbp; mmss($mmbr,\%mmbh); unless($mmbq) { exit(1); } }
sub mmqd { my($mmbt) =  @_; my($mmbr) = ''; print CGI->multipart_start();
if($mailman::mmae) { $mmbr = 't_nf_status.htm'; } else { $mmbr = 't_f_status.htm'; }
my(%mmbh); $mmbh{'STATUS'} = $mmbt; mmss($mmbr,\%mmbh);
print CGI->multipart_end(); } sub mmqe {
print "Set-cookie: MailManAuth=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n";
print "Set-cookie: MailManCmds=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n";
print "Set-cookie: MailManDir=;$mailman::mmad" .
"expires=Sun, 03-May-1998 16:00:00 GMT\n";
print "Expires: Sun, 03 May 1998 16:00:00 GMT\n"; $mailman::mmo = '';
$mailman::mmah = ''; if($mailman::bKioskMode) { my($mmbu) = '';
($mailman::mmbh{'GREETING'},$mmbu) = mmsr('t_login.htm',
('GREETING','KIOSKMODESCRIPT')); $mailman::mmbh{'HTMLCOMMENTBEGIN'} = '<!-- ';
$mailman::mmbh{'HTMLCOMMENTEND'} = ' -->'; $mailman::mmbh{'KIOSKMODESCRIPT'} =
mmso($mmbu,\%mailman::mmbh);
$mailman::mmbh{'HTMLCOMMENTBEGIN'} = ''; $mailman::mmbh{'HTMLCOMMENTEND'} = ''; }
else { $mailman::mmbh{'GREETING'} =
mmsq('t_login.htm','GREETING'); }

print eval(mmrs($mailman::mhaa[1]));
 } sub mmqf {
my($mmbx) = "\015\012"; my($mmby, $mmbz) = @_; my($mmca) = length($mmbz . $mmbx);
syswrite($mmby,$mmbz . $mmbx,$mmca); } sub mmqg {
if($mailman::mmbl){ return; } my($mmcb); unless(defined($mailman::mmo) &&
$mailman::mmo ne '') { return("No username provided, cannot proceed."); }
unless(defined($mailman::mmq) && $mailman::mmq ne '') {
return("No password provided, cannot proceed."); }
unless(defined($mailman::strIncomingServer) && $mailman::strIncomingServer ne '')
{ return("No server provided, cannot proceed."); }
retrylogin: if($mailman::bUseAlarm) { $mailman::mmbs =
"Connection to server timed out."; $SIG{'ALRM'} = \&mmqc;
alarm($mailman::iTimeoutDurationInSeconds); } my($mmcc) = 0;
$mmcc = getprotobyname('tcp'); socket($mma,PF_INET,SOCK_STREAM,$mmcc);
my($mmcd) = 0; $mmcd = gethostbyname($mailman::strIncomingServer); unless($mmcd) {
return("Could not find an IP address for the host " .
"\"$mailman::strIncomingServer\"."); } my($mmce) = '';
$mmce = sockaddr_in(110, $mmcd); unless(connect($mma, $mmce)) {
return("Could not connect to server " .
"\"$mailman::strIncomingServer\", \"$!\""); } select($mma); $|=1; select(STDOUT);
binmode($mma); $mailman::mmbs = "The server connected, but will not respond.";
if($mailman::bUseAlarm){ alarm(180); } unless(<$mma> =~ /^\+OK/) {
return("The server does not respond appropriately."); } $mailman::mmbs =
"The server timed out during login."; if($mailman::bUseAlarm){ alarm(180); }
mmqf($mma,"USER $mailman::mmo"); my($mmcf) = ''; $mmcf = <$mma>;
unless($mmcf =~ /^\+OK/) { return($mmcf); } mmqf($mma,"PASS $mailman::mmq");
$mmcf = <$mma>; unless($mmcf =~ /^\+OK/) { if((($mmcf =~ /another session/i) ||
($mmcf =~ /another POP3 session/i) || ($mmcf =~ /mailbox in use/i) ||
($mmcf =~ /mailbox busy/i)) && $mmcb < 12) { mmqf($mma,"QUIT"); close $mma;
$mmcb++; sleep(5); goto retrylogin; } return($mmcf); } mmqf($mma,'STAT');
$mmcf = <$mma>; $mmcf =~ /^\+OK\s+(\d+)\s+/i; $mailman::mmcg = $1;
if($mailman::mmcg == 0) { $mailman::mmbl = 1; return; } mmqf($mma,"LIST");
$mmcf = <$mma>; unless($mmcf =~ /^\+OK/) { return($mmcf); } $mailman::mmcg = 0;
while(<$mma> =~ /(\d+) (\d+)/) { $mailman::mmch[$1] = $2; $mailman::mmcg++; }
$mailman::mmbl = 1; return; } sub mmqh { my($mmci,$mmcj) = @_;
my($mmck) = ''; if(defined($mmci) && defined($mmcj)) { $mmck .= mmsv(
$mmcj . $mailman::mmcl[$mmci]) . '|'; } else { $mmck .= mmsv(
$mailman::mmcm) . '|'; } $mmck .= mmsv($mailman::mmo) . '|';
$mmck .= mmsv($mailman::strIncomingServer) . '|';
$mmck .= mmsv($mailman::mmaz) . '|';
$mmck .= mmsv($mailman::mmcn) . '|';
$mmck .= mmsv($mailman::mmco) . '|';
$mmck .= mmsv($mailman::mmcp) . '|';
$mmck .= mmsv($mailman::mmcq) . '|';
$mmck .= mmsv($mailman::mmcr) . '|';
$mmck .= mmsv($mailman::mmcs) . '|'; if(defined($mmci)) {
$mmck .= $mailman::mmch[$mmci] . '|'; } else { $mmck .= $mailman::mmch . '|'; }
$mmck .= $mailman::mmct . '|'; $mmck .= $mailman::mmcu . '|';
$mmck .= $mailman::mmcv; return $mmck; } sub mmqi { my($mmcw) = @_;
chomp($mmcw); my(@mmcx) = split(/\|/,$mmcw); if($#mmcx < 12) { return 0; }
$mailman::mmcm =             mmsw($mmcx[0]);
$mailman::mmcy = mmsw($mmcx[1]);
$mailman::mmcz=    mmsw($mmcx[2]);
$mailman::mmaz =              mmsw($mmcx[3]);
$mailman::mmcn =              mmsw($mmcx[4]);
$mailman::mmco =            mmsw($mmcx[5]);
$mailman::mmcp =            mmsw($mmcx[6]);
$mailman::mmcq =      mmsw($mmcx[7]);
$mailman::mmcr =         mmsw($mmcx[8]);
$mailman::mmcs =         mmsw($mmcx[9]);
$mailman::mmch =                       $mmcx[10];
$mailman::mmct =                       $mmcx[11]; $mailman::mmct =~ s/\s//g; 
$mailman::mmcu =                $mmcx[12]; $mailman::mmcu =~ s/\s//g; 
$mailman::mmcv =                   $mmcx[13];
unless($mailman::mmaz){ $mailman::mmaz = "Unknown";}
unless($mailman::mmco){ $mailman::mmco = "Unknown";}
unless($mailman::mmcp){ $mailman::mmcp = "Unknown";}
unless($mailman::mmcr){ $mailman::mmcr = "Unspecified";}
$mailman::mmda = mmqt(mmqr($mailman::mmaz));
$mailman::mmdb = mmqt(mmqr($mailman::mmco));
$mailman::mmdc = mmqt(mmqr($mailman::mmcr));
$mailman::mmdd = mmqt(mmqr($mailman::mmcp)); return 1; }
sub mmqj { unless(-d $mailman::strLocalLocationUsers) {
mmqc("Could not locate directory \"" .
"$mailman::strLocalLocationUsers\" for user information."); }
unless(-d $mailman::mmv) { unless(mkdir($mailman::mmv,0755)) { mmqc(
"Could not create user directory \"$mailman::mmv\" " .
"in \"$mailman::strLocalLocationUsers\".  Make sure that " .
"\"$mailman::strLocalLocationUsers\" is writable by the " . "web user."); }
if(defined($mailman::iLocalDirectoryPermissions)) {
mmtb($mailman::mmv, $mailman::iLocalDirectoryPermissions); } } }
sub mmqk { unless($mailman::mmah) { return; } my($mmde) = 
$mailman::mmv . '/' . mmsv($mailman::mmah); unless(-d $mmde) {
unless(mkdir($mmde,0755)) { mmqc("Could not create directory for folder " .
"\"$mailman::mmah\" " . "in \"$mailman::mmv\".  Make sure that " .
"\"$mailman::mmv\" is writable by the " . "web user."); }
if(defined($mailman::iLocalDirectoryPermissions)) { mmtb($mmde,,
$mailman::iLocalDirectoryPermissions); } if($mailman::mmah eq 'INBOX') {
$mailman::mmah = 'SENT'; mmqk(); $mailman::mmah = 'TRASH';
mmqk(); $mailman::mmah = 'INBOX'; } } } sub mmql {
$mailman::mmah = 'INBOX'; mmqn();
if($mailman::bDownloadIndividualAccounts) { return; } mmrl();
my($mmdf,$mmdg,$mmdh) = ('','',''); if($mailman::mmdi) { $mmdf = $mailman::mmo;
$mmdg = $mailman::mmq; $mmdh   = $mailman::strIncomingServer; } my($mmdj) = '';
foreach $mmdj (sort keys %mailman::mmdk) { $mailman::mmo = 
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_USERNAME'}; $mailman::mmq =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_PASSWORD'}; $mailman::strIncomingServer =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_SERVER'}; $mailman::mmah =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_FOLDER'}; mmqn(); }
if($mailman::mmdi) { $mailman::mmo = $mmdf; $mailman::mmq = $mmdg;
$mailman::strIncomingServer = $mmdh; $mailman::mmah = 'INBOX'; } }
sub mmqm { my($mmdl) = shift; mmrl();
my($mmdf,$mmdg,$mmdh) = ('','',''); if($mailman::mmdi) { $mmdf = $mailman::mmo;
$mmdg = $mailman::mmq; $mmdh   = $mailman::strIncomingServer; } my($mmdj) = '';
foreach $mmdj (sort keys %mailman::mmdk) { $mailman::mmo = 
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_USERNAME'}; $mailman::mmq =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_PASSWORD'}; $mailman::strIncomingServer =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_SERVER'}; $mailman::mmah =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_FOLDER'}; if($mmdj =~ /$mmdl/i) {
mmqn(); } } if($mailman::mmdi) { $mailman::mmo = $mmdf;
$mailman::mmq = $mmdg; $mailman::strIncomingServer = $mmdh; } }
sub mmqn { unless(defined($mailman::mmah) && length($mailman::mmah))
{ $mailman::mmah = 'INBOX'; } my($mmbg) = ''; if($mmbg = mmqg()) {
mmqc($mmbg); } if($mailman::iUserDiskQuota) { unless($mailman::mmdm) {
mmtj(); } if($mailman::mmdm >= $mailman::iUserDiskQuota) { return; } }
mmqj(); mmqk(); mmqw(); use Fcntl;
my($mmcj) = $mailman::mmo . '@' .  $mailman::strIncomingServer . '@';
if($mailman::mmcg == 0) { mmqf($mma,"QUIT"); close $mma; $mailman::mmbl = 0;
return; } mmqf($mma,"UIDL"); my($mmcf) = ''; $mmcf = <$mma>;
unless($mmcf =~ /^\+OK/) { mmqc($mmcf); } my $mmd=0;
while(<$mma> =~ /(\d+)\s+(\S+)/) { my($mmcg,$mmdn) = ($1, $2);
if(defined($mailman::mmdo) && $mailman::mmdo) {
$mmdn =~ s/(\w)/sprintf("%02x", ord($1))/eg; } $mailman::mmdp[$mmd] = $mmcg;
$mailman::mmcl[$mmcg] = $mmdn; $mailman::mmdq{$mmcj . $mmdn} = 1; $mmd++; }
my $mmdr = $mmd; my(%mmds); my($mmdt) = ''; my(%mmdu) = (); my(%mmdv) = ();
my($mmci) = my($mmdw) = 0; my($mmdx) = 0; my(%mmdy); my($mmdz) = new FileHandle();
my($mmea) = $mailman::mmv . '/INBOX/msglist'; retry: if(open($mmdz,"<$mmea")) {
flock($mmdz,2); my($mmbz) = ''; $mmbz = <$mmdz>; if($mmbz =~ /^(\d+)\s(\d+)\s/) {
$mmci = $1; } elsif($mmbz =~ /^(\d+)\s/) { $mmci = $1; } else { close($mmdz);
mmto($mailman::mmv . '/INBOX'); goto retry; } $mmdw = 0;
while(defined($_ = <$mmdz>)) { chomp;
if(/^([^\|]+)\|/ && mmqi($_)) { my($mmeb) = mmsw($1);
$mmds{$mmeb} = 1; $mmdw++; unless(defined($mailman::mmcv) &&
$mailman::mmcv =~ /R/i) { $mmdx++; } my($mmec) = $mailman::mmcq; my($mmed) = 0;
while(defined($mmdu{$mmec})) { if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) { $mmed++; }
$mmec .= "_$mmed"; } $mmdu{$mmec} = $_; } elsif(/^DELETED\:\s+(\S+)\s*$/) {
my($mmeb) = mmsw($1); if($mailman::mmdq{$mmeb} || $mmeb !~ /^$mmcj/) {
$mmds{$mmeb} = 1; $mmdy{$mmeb} = 1; $mmdt .= $_ . "\n"; } }
elsif(/^\S+\:\s+(\S+)\s*$/) { my($mmeb) = mmsw($1);
if($mailman::mmdq{$mmeb} || $mmeb !~ /^$mmcj/) { $mmds{$mmeb} = 1;
$mmdt .= $_ . "\n"; } } } if($mmdw != $mmci) { close($mmdz);
mmto($mailman::mmv . '/INBOX'); goto retry; } close($mmdz); } my($mmee);
my($mmef) = ''; my($mmeg) = 0; my($mmeh) = 0;
message: for($mmd=0;$mmd<$mmdr;$mmd++) { $mmee = $mailman::mmdp[$mmd]; my($mmei) =
$mmcj . $mailman::mmcl[$mmee]; if($mailman::mmas) { if($mmdy{$mmei}) {
mmqf($mma,"DELE $mmee"); $mmcf = <$mma>; unless($mmcf =~ /^\+OK/) {
mmqc("While trying to delete a message " .
"that has been deleted from your message " .
"folders, your POP3 server responded " . "\"$mmcf\""); } } } unless($mmds{$mmei}) {
my($mmej) =  mmsv($mmcj . $mailman::mmcl[$mmee]);
mmqo($mmee,$mmej); if($mailman::iUserDiskQuota) { $mailman::mmdm +=
(-s "${mailman::mmv}/" . mmsv($mailman::mmah) . "/$mmej");
if($mailman::mmdm >= $mailman::iUserDiskQuota) { last message; } }
$mailman::mmcv = ''; my($mmek) = mmqh($mmee, $mmcj);
my($mmec) = mmtc($mailman::mmcp); if($mailman::mmah eq 'INBOX') {
my($mmed) = 0; while(defined($mmdu{$mmec})) { if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) {
$mmed++; } $mmec .= "_$mmed"; } $mmdu{$mmec} = $mmek; $mmeg++; } else {
$mmdt .= 'MOVED: ' . mmsv($mmei) . "\n"; my($mmed) = 0;
while(defined($mmdv{$mmec})) { if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) { $mmed++; }
$mmec .= "_$mmed"; } $mmdv{$mmec} = $mmek; $mmeh++; } if($mailman::mmar) {
mmqf($mma, "DELE $mmee"); $mmcf = <$mma>; unless($mmcf =~ /^\+OK/) {
mmqc($mmcf); } } } } unless(open($mmdz,">$mmea")) {
mmqc("Could not create user message list in \"" .
$mmea ."\".  Make sure that the  " . "directory is writable by the web user."); }
flock($mmdz,2); $mailman::mmcg = $mmci + $mmeg;
print {$mmdz} "$mailman::mmcg $mmdx\n"; my($mmek) = '';
foreach $mmek (sort {$a <=> $b} keys %mmdu) { print {$mmdz} $mmdu{$mmek} . "\n"; }
print {$mmdz} "\n" . $mmdt; close($mmdz); if(($mailman::mmah ne 'INBOX') && $mmeh) {
mmsi(mmsv($mailman::mmah), $mmeh, \%mmdv); }
mmqf($mma,"QUIT"); close $mma; $mailman::mmbl = 0; } sub mmqo
{ my($mmee,$mmel) = @_; my($mmem) = new FileHandle(); mmqp($mmee);
$mmel =  "${mailman::mmv}/" . mmsv($mailman::mmah) . "/$mmel";
unless(open($mmem,">$mmel")) {
mmqc("Could not create file to store message " .
"in \"$mmel\".  Make sure that the " . "directory is writable by the web user.");
} my($mmen) = $mmee; mmqf($mma,"RETR $mmen"); my($mmcf) = '';
$mmcf = <$mma>; unless($mmcf =~ /^\+OK/) { mmqc($mmcf); } my($mmbz) = '';
while(defined($mmbz = <$mma>)) { if($mmbz =~ /^\.\r$/){ last; }
print {$mmem} $mmbz; } close $mmem; if(defined($mailman::iLocalFilePermissions)) {
mmtb($mmel,$mailman::iLocalFilePermissions); } }
sub mmqp { my($mmci) =  @_; $mailman::mmbs =
"The server timed out fetching a header."; if($mailman::bUseAlarm){ alarm(10); }
mmqf($mma,"TOP $mmci 0"); my($mmcf) = ''; $mmcf = <$mma>;
unless($mmcf =~ /^\+OK/) { mmqc($mmcf); } mmqq($mma);
$mailman::mmeo = $mmci . 'H' . $mailman::mmep; $mailman::mmeq = $mmci; }
sub mmqq { my($mmby) = shift; $mailman::mmaz = ''; $mailman::mmcn = '';
$mailman::mmco = ''; $mailman::mmcp = ''; $mailman::mmcq = '0';
$mailman::mmcr = ''; $mailman::mmcs = ''; $mailman::mmep = ''; $mailman::mmct = 0;
$mailman::mmcu = 0; my($mmer) = 0; my($mmes) = 0; my($mmet) = 0; my($mmeu) = 1;
my($mmev) = ''; my($mmew) = -1; while(defined($_ = <$mmby>)) {
if(/^[\r\n]+$/){ $mmer = 1; } if(/^\.[\r\n]*$/){ last; }
if(/^Content-type\:\s+([^\;\s]+)[\;\s]/i) { my($mmex) = $1; if(
($mmex !~ /multipart\/alternative/i) && ($mmex !~ /text\//i)) { $mailman::mmcu = 1;
} } if(/^begin \d\d\d (\S+)\s*$/i) { $mailman::mmcu = 1; } unless($mmer) {
$mmew = mmtc($_); if($mmew != -1) { $mailman::mmcq = $mmew; } $mmeu = 1;
if(/^To\: (.+)$/i || ((/^\s(.+)$/) && $mmes)) { $mailman::mmaz .= $1;
$mailman::mmaz =~ s/^(.*)[\r\n]+$/$1/;
$mailman::mmaz = mmqr($mailman::mmaz); $mmev .= $_; $mmes = 1; $mmet = 0;
$mmeu = 0; } if(/^CC\: (.+)$/i || ((/^\s(.+)$/) && $mmet)) { $mailman::mmcn .= $1;
$mailman::mmcn =~ s/^(.*)[\r\n]+$/$1/;
$mailman::mmcn = mmqr($mailman::mmcn); $mmev .= $_; $mmes = 0; $mmet = 1;
$mmeu = 0; } if(/^From\: (.+)$/i) { $mailman::mmco = $1;
$mailman::mmco =~ s/^(.*)[\r\n]+$/$1/;
$mailman::mmco = mmqr($mailman::mmco); $mmev .= $_; }
if(/^Date\: (.+)$/i) { $mailman::mmcp = $1; $mailman::mmcp =~ s/^(.*)[\r\n]+$/$1/;
$mmev .= $_; } if(/^Subject\: (.+)$/i) { $mailman::mmcr = $1;
$mailman::mmcr =~ s/^(.*)[\r\n]+$/$1/;
$mailman::mmcr = mmqr($mailman::mmcr); $mmev .= $_; }
if(/^Reply-To\: (.+)$/i) { $mailman::mmcs = $1;
$mailman::mmcs =~ s/^(.*)[\r\n]+$/$1/; $mmev .= $_; } if(/^Message-ID\: (.+)$/i) {
$mailman::mmep = $1; $mailman::mmep =~ s/^(.*)[\r\n]+$/$1/; }        if($mmeu) {
$mmes = 0; $mmet = 0; } } if(/^MIME-Version\: 1\.0/i) { if(!$mmer) { $mailman::mmct = 1;
} } } if($mailman::mmep eq "") { $mailman::mmep = $mmev;
while(length($mailman::mmep)>20) {
$mailman::mmep = (substr($mailman::mmep,0,20) ^  substr($mailman::mmep,20)); }
$mailman::mmep = pack("u*",$mailman::mmep); }
$mailman::mmep =~ s/(\W)/sprintf("%%%x", ord($1))/eg;
unless($mailman::mmaz){ $mailman::mmaz = "Unknown";}
unless($mailman::mmco){ $mailman::mmco = "Unknown";}
unless($mailman::mmcp){ $mailman::mmcp = "Unknown";}
unless($mailman::mmcr){ $mailman::mmcr = "Unspecified";}
unless($mailman::mmeo){ $mailman::mmeo = "0";}
$mailman::mmda = mmqt($mailman::mmaz);
$mailman::mmdb = mmqt($mailman::mmco);
$mailman::mmey = mmqt($mailman::mmcn);
$mailman::mmdc = mmqt($mailman::mmcr);
$mailman::mmdd = mmqt($mailman::mmcp); } sub mmqr { my $mmez = shift;
$mmez =~ s/\=\?iso-8859-1\?q\?([^\?]+)\?\=/
mmrw(mmrv($1))/xeig; $mmez =~
s/\=\?iso-8859-1\?b\?([^\?]+)\?\=/ mmrx(mmrv($1))/xeig;
return $mmez; } sub mmqs { my($mmbj) = @_; $mmbj =~ /^(\d+)H(.+)$/;
my($mmfa) = $1; my($mmfb) = $2; if($1 eq '' || $2 eq '') {
mmqc('The message ID string "' . $mmbj .  '" is badly formed.'); }
$mmfb =~ s/%(..)/pack("c",hex($1))/ge; $mailman::mmbs =
"The server timed out during message listing.";
if($mailman::bUseAlarm){ alarm(180); } mmqf($mma,"LIST"); my($mmcf) = '';
$mmcf = <$mma>; unless($mmcf =~ /^\+OK/) { mmqc($mmcf); } $mailman::mmfc = 0;
while(<$mma> =~ /(\d+) (\d+)/) { $mailman::mmch[$1] = $2; $mailman::mmfc++; }
my($mmd) = $mmfa; my($mmfd) = 0; while($mmd>0) { mmqp($mmd);
$mailman::mmep =~ s/%(..)/pack("c",hex($1))/ge; if($mailman::mmep eq  $mmfb) {
$mmfd = 1; last; } $mmd--; } if(!$mmfd) { $mailman::mmaz = ''; $mmd = $mmfa;
mmqp($mmd); } if($mailman::mmaz eq '') {
mmqc('Could not find the specified message.'); } return ($mmd); } sub mmqt
{ my($mmfe) = @_; $mmfe =~ s/\&/\&amp\;/g; $mmfe =~ s/\</\&lt\;/g;
$mmfe =~ s/\>/\&gt\;/g; $mmfe =~ s/\%mmff/\</g; $mmfe =~ s/\%mmfg/\>/g;
$mmfe =~ s/(http\:\S+)\s/"\<a target=\"_top\" href\=\"$mailman::mmab?BACKGROUND=".mmsv($1)."\"\>$1\<\/a\>"/eg;
if($mailman::mmae) {
$mmfe =~ s/(href\=\"[^\"]*)(BACKGROUND\=)/${1}NOFRAMES\=TRUE&$2/g; } return $mmfe;
} sub mmqu { mmqg();
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) { $mailman::mmbh{'SERVER'} =
mmts($mailman::strFromDomainName); } else { $mailman::mmbh{'SERVER'} =
mmts($mailman::strIncomingServer); } my($mmfh, $mmfi, $mmfj) =
mmsr('t_folders.htm',
('FOLDER_EVEN','FOLDER_ODD','DELETEFOLDERIMAGE'));
$mailman::mmbh{'AUTHENTICATION'} = 'MailManEscape(AUTHENTICATION)';
$mailman::mmbh{'SETTINGS'} = 'MailManEscape(SETTINGS)';
my(@mmfk) = mmtg(); my($mmfl) = 0; my($mmfm); foreach $mmfm (@mmfk) {
my($mmfn,$mmfo) = mmth($mmfm);
$mailman::mmbh{'FOLDERNAME'} = mmqt($mmfm);
$mailman::mmbh{'FOLDERNAMESAFE'} = mmsv($mmfm);
$mailman::mmbh{'FOLDERNAMESAFESAFE'} =
mmsv($mailman::mmbh{'FOLDERNAMESAFE'});
$mailman::mmbh{'NUMMESSAGES'} = $mmfn;
$mailman::mmbh{'NUMUNREADMESSAGES'} = $mmfo; if($mmfn == 0 &&
$mmfm !~ /^INBOX$/i && $mmfm !~ /^SENT$/i && $mmfm !~ /^TRASH$/i) {
$mailman::mmbh{'DELETEFOLDERIMAGE'} = mmso($mmfj,
\%mailman::mmbh); } else { $mailman::mmbh{'DELETEFOLDERIMAGE'} = ''; } my($mmfp) = '';
if(($mmfl+1)%2==0) { $mmfp = mmso($mmfh, \%mailman::mmbh); } else {
$mmfp = mmso($mmfi, \%mailman::mmbh); } $mmfl++;
$mailman::mmbh{'FOLDERS'} .= $mmfp; }
$mailman::mmbh{'FOLDERS'} =~ s/MailManEscape\(/MailMan\(/gi;
mmss('t_folders.htm',\%mailman::mmbh); } sub mmqv {
mmqg(); $mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa; mmqw();
$mailman::mmbh{'PREF_REALNAME'} = $mailman::mmam;
$mailman::mmbh{'PREF_EMAIL'} = $mailman::mman;
$mailman::mmbh{'PREF_OUTGOING'} = $mailman::mmap;
$mailman::mmbh{'PREF_SIGNATURE'} = $mailman::mmao;
$mailman::mmbh{'PREF_NUMPERPAGE'} = $mailman::mmaq; if($mailman::mmar) {
$mailman::mmbh{'PREF_DELETEDOWNLOAD'} = 'checked'; } else {
$mailman::mmbh{'PREF_DELETEDOWNLOAD'} = ''; } if($mailman::mmas) {
$mailman::mmbh{'PREF_DELETEPROXY'} = 'checked'; } else {
$mailman::mmbh{'PREF_DELETEPROXY'} = ''; } if($mailman::mmat) {
$mailman::mmbh{'PREF_DELETESAVE'} = 'checked'; } else {
$mailman::mmbh{'PREF_DELETESAVE'} = ''; } if($mailman::mmau) {
$mailman::mmbh{'PREF_SENDSAVE'} = 'checked'; } else {
$mailman::mmbh{'PREF_SENDSAVE'} = ''; }
$mailman::mmbh{'PREF_STARTUP_'.$mailman::mmav} = 'checked';
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; }
mmss('t_preferences.htm',\%mailman::mmbh); } sub mmqw {
my($mmfq) = new FileHandle(); $mailman::mmfr = "${mailman::mmv}/preferences";
if(!open($mmfq,"<$mailman::mmfr")) { $mailman::mmam = '';
if(defined($mailman::strFromDomainName)) { $mailman::mman = 
$mailman::mmo . '@' . $mailman::strFromDomainName; } else { $mailman::mman =
$mailman::mmo . '@' . $mailman::strIncomingServer; } $mailman::mmao = '';
$mailman::mmar = 0; $mailman::mmas = 0; $mailman::mmat = 1; $mailman::mmau = 1;
$mailman::mmaq = $mailman::iMessagesPerPage; $mailman::mmap = '';
$mailman::mmav = 'INBOX'; return; } flock($mmfq,2); my($mmbz) = '';
while(defined($mmbz = <$mmfq>)) { if($mmbz =~ /REALNAME\:\s+\"([^\"]*)\"/) {
$mailman::mmam = mmsw($1); } elsif($mmbz =~ /EMAIL\:\s+\"([^\"]*)\"/) {
$mailman::mman = mmsw($1); }
elsif($mmbz =~ /OUTGOING\:\s+\"([^\"]*)\"/) {
$mailman::mmap = mmsw($1); }
elsif($mmbz =~ /SIGNATURE\:\s+\"([^\"]*)\"/) {
$mailman::mmao = mmsw($1); } elsif($mmbz =~ /STARTUP\:\s+\"([^\"]*)\"/)
{ $mailman::mmav = mmsw($1); }
elsif($mmbz =~ /DELETEDOWNLOAD\:\s+\"([^\"]*)\"/) { if($1 eq '1') {
$mailman::mmar = 1; } else { $mailman::mmar = 0; } }
elsif($mmbz =~ /DELETEPROXY\:\s+\"([^\"]*)\"/) { if($1 eq '1') { $mailman::mmas = 1;
} else { $mailman::mmas = 0; } } elsif($mmbz =~ /DELETESAVE\:\s+\"([^\"]*)\"/) {
if($1 eq '1') { $mailman::mmat = 1; } else { $mailman::mmat = 0; } }
elsif($mmbz =~ /SAVESAVE\:\s+\"([^\"]*)\"/) { if($1 eq '1') { $mailman::mmau = 1; }
else { $mailman::mmau = 0; } } elsif($mmbz =~ /NUMPERPAGE\:\s+\"([^\"]*)\"/) {
$mailman::mmaq = $1; } } close($mmfq); } sub mmqx {
my($mmfq) = new FileHandle(); my($mmfs) = $mailman::mmae; $mailman::mmae = 1;
mmqj(); $mailman::mmfr = "${mailman::mmv}/preferences";
if(!open($mmfq,">$mailman::mmfr")) {
mmqc("Could not open the preferences file \"" . $mailman::mmfr .
"\" for storing this user's preferences.  "); } flock($mmfq,2); print {$mmfq}
"REALNAME: \"" . mmsv($mailman::mmam) . "\"\n"; print {$mmfq}
"EMAIL: \"" . mmsv($mailman::mman) . "\"\n"; print {$mmfq}
"OUTGOING: \"" . mmsv($mailman::mmap) . "\"\n"; print {$mmfq}
"STARTUP: \"" . mmsv($mailman::mmav) . "\"\n"; print {$mmfq}
"DELETEDOWNLOAD: \"" . $mailman::mmar . "\"\n"; print {$mmfq}
"DELETEPROXY: \"" . $mailman::mmas . "\"\n"; print {$mmfq}
"DELETESAVE: \"" . $mailman::mmat . "\"\n"; print {$mmfq}
"SAVESAVE: \"" . $mailman::mmau . "\"\n"; print {$mmfq}
"NUMPERPAGE: \"" . $mailman::mmaq . "\"\n"; print {$mmfq} "SIGNATURE: \"" .
mmsv($mailman::mmao) . "\"\n"; close($mmfq); $mailman::mmae = $mmfs; }
sub mmqy { my($mmbr) = 't_addresses.htm';
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; }
mmqz(); if($mailman::mmft) { my($mmfu, $mmfv) =
mmsr($mmbr, ('INDIVIDUAL_EVEN','INDIVIDUAL_ODD'));
my($mmfw) = 0; my($mmba) = ''; foreach $mmba (sort keys %mailman::mmbb) {
$mailman::mmbh{'NICKNAME'} = $mmba;
$mailman::mmbh{'NICKNAMESAFE'} = mmsv($mmba); my($mmbc) =
$mailman::mmbb{$mmba}->{'FIRSTNAME'}; my($mmbd) =
$mailman::mmbb{$mmba}->{'LASTNAME'}; my($mmbe) =
$mailman::mmbb{$mmba}->{'ADDRESS'}; if(($mmbc ne '') || ($mmbd ne '')) {
$mailman::mmbh{'ADDRESS'} = "$mmbc $mmbd " . "&lt;$mmbe&gt;"; } else {
$mailman::mmbh{'ADDRESS'} = "$mmbe"; } if($mmfw%2==0) {
$mailman::mmbh{INDIVIDUALS} .= mmso($mmfu,\%mailman::mmbh); } else {
$mailman::mmbh{INDIVIDUALS} .= mmso($mmfv,\%mailman::mmbh); }
$mmfw++; } } else { $mailman::mmbh{'INDIVIDUALS'} = mmsq($mmbr,
'NOBODY_INDIVIDUAL'); } mmra(); if($mailman::mmfx) {
my($mmfy, $mmfz) = mmsr($mmbr, ('GROUP_EVEN','GROUP_ODD'));
my($mmfw) = 0; my($mmba) = ''; foreach $mmba (sort keys %mailman::mmbf) {
$mailman::mmbh{'NICKNAME'} = $mmba;
$mailman::mmbh{'NICKNAMESAFE'} = mmsv($mmba);
$mailman::mmbh{'ADDRESSES'} = $mailman::mmbf{$mmba};
$mailman::mmbh{'ADDRESSES'} =~ s/(\r\n)|(\r\n)/,\ /g; 
$mailman::mmbh{'ADDRESSES'} =~ s/[\r\n]/,\ /g;        
$mailman::mmbh{'ADDRESSES'} =~ s/\,\ $//g; if($mmfw%2==0) {
$mailman::mmbh{GROUPS} .= mmso($mmfy,\%mailman::mmbh); } else {
$mailman::mmbh{GROUPS} .= mmso($mmfz,\%mailman::mmbh); } $mmfw++; } }
else { $mailman::mmbh{'GROUPS'} = mmsq($mmbr, 'NOBODY_GROUP');
} mmss($mmbr,\%mailman::mmbh); } sub mmqz {
my($mmga) = new FileHandle(); mmqj(); my($mmgb) =
"${mailman::mmv}/individuals"; if(!open($mmga,"<$mmgb")) { return; } flock($mmga,2);
my($mmba) = ''; my($mmgc) = ''; $mailman::mmft = 0; while(defined($_ = <$mmga>)) {
if(/^BEGIN\s+(\S+)\s*/) { $mmba = mmsw($1); $mmgc = $mmba;
$mmgc =~ tr/[A-Z]/[a-z]/; $mailman::mmft++; $mailman::mmbb{$mmgc}->{NICKNAME} =
$mmba; } elsif(/^(\S+)\s+(\S+)\s*$/) { $mailman::mmbb{$mmgc}->{$1} =
mmsw($2); } } close($mmga); } sub mmra {
my($mmga) = new FileHandle(); mmqj();
my($mmgd) = "${mailman::mmv}/groups"; if(!open($mmga,"<$mmgd")) { return; }
flock($mmga,2); my($mmba) = ''; my($mmgc) = ''; $mailman::mmfx = 0;
while(defined($_ = <$mmga>)) { if(/^(\S+)\s+\"(\S+)\"\s*/) {
$mmba = mmsw($1); $mmgc = $mmba; $mmgc =~ tr/[A-Z]/[a-z]/;
$mailman::mmbf{$mmgc} .= mmsw($2); $mailman::mmfx++; } } close($mmga); }
sub mmrb { my($mmbg) = shift;
my($mmga) = new FileHandle(); my($mmbr) = 't_addressesindividual.htm';
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; } my($mmba) = '';
if($mmb->param('ADDRESSINDIVIDUAL')) { $mmba = $mmb->param('ADDRESSINDIVIDUAL');
$mailman::mmbh{'NICKNAME'} = $mmba;
$mailman::mmbh{'NICKNAME'} = mmso(
mmsq($mmbr, 'NICKNAME_FIXED'),\%mailman::mmbh);
mmqj(); my($mmgb) = "${mailman::mmv}/individuals";
if(!open($mmga,"<$mmgb")) { mmqc("Could not open the address file \"" .
$mmgb . "\" for storing this user's addresses.  "); } flock($mmga,2); my($mmge) = 0;
my($mmgf) = 0; my($mmgg) = ''; individualsline: while(defined($_ = <$mmga>)) {
if(/^BEGIN\s+(\S+)\s*/) { $mmgg = mmsw($1); if($mmgg =~ /$mmba/i) {
$mmge = 1; $mmgf = 1; } } elsif(/^END/) { if($mmgf) { close($mmga); last individualsline;
} } elsif($mmgf && /^(\S+)\s+(\S+)\s*$/) { $mailman::mmbh{"ADDRESSITEM_$1"} =
mmsw($2); } } close($mmga); } else { $mailman::mmbh{'NICKNAME'} =
mmsq($mmbr, 'NICKNAME_NEW'); } if($mmbg ne '') {
$mailman::mmbh{'ERROR'} = $mmbg; } my(@mmc) = $mmb->param; my($mmd) = 0;
for($mmd=0;$mmd<$#mmc;$mmd++) { my($mme) = $mmc[$mmd];;
if($mme =~ /^ADDRESSITEM_(.*)$/) { $mailman::mmbh{$mme} = $mmb->param($mme); } }
mmss($mmbr,\%mailman::mmbh); } sub mmrc {
my($mmbg) = shift; my($mmga) = new FileHandle();
my($mmbr) = 't_addressesgroup.htm'; $mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; } my($mmba) = '';
if($mmb->param('ADDRESSGROUP')) { $mmba = $mmb->param('ADDRESSGROUP');
$mailman::mmbh{'NICKNAME'} = $mmba;
$mailman::mmbh{'NICKNAME'} = mmso(
mmsq($mmbr, 'NICKNAME_FIXED'),\%mailman::mmbh);
mmqj(); my($mmgd) = "${mailman::mmv}/groups"; if(!open($mmga,"<$mmgd")) {
mmqc("Could not open the address file \"" . $mmgd .
"\" for storing this user's addresses.  "); } flock($mmga,2); my($mmgh) = '';
groupsline: while(defined($_ = <$mmga>)) { if(/^(\S+)\s+\"(\S+)\"\s*/) {
$mmgh = mmsw($1); my $mmgi = $2; if($mmgh =~ /$mmba/i) {
$mailman::mmbh{'ADDRESSITEM_ADDRESSES'} = mmsw($mmgi); } } } close($mmga);
} else { $mailman::mmbh{'NICKNAME'} = mmsq($mmbr,
'NICKNAME_NEW'); } if($mmbg ne '') { $mailman::mmbh{'ERROR'} = $mmbg; }
my(@mmc) = $mmb->param; my($mmd) = 0; for($mmd=0;$mmd<$#mmc;$mmd++) {
my($mme) = $mmc[$mmd];; if($mme =~ /^ADDRESSITEM_(.*)$/) {
$mailman::mmbh{$mme} = $mmb->param($mme); } }
mmss($mmbr,\%mailman::mmbh); } sub mmrd {
my($mmba) = shift; my($mmga) = new FileHandle(); my($mmgj) = new FileHandle();
my($mmfs) = $mailman::mmae; $mailman::mmae = 1; mmqj(); my($mmgb) =
"${mailman::mmv}/individuals"; if((!open($mmga,"<$mmgb")) ||
(!open($mmgj,">$mmgb.tmp"))) { return; } flock($mmga,2); my($mmge) = 0; my($mmgf) = 0;
my($mmgg) = ''; while(defined($_ = <$mmga>)) { if(/^BEGIN\s+(\S+)\s*/) {
$mmgg = mmsw($1); if($mmgg =~ /$mmba/i) { $mmge = 1; $mmgf = 1; } else {
print {$mmgj} $_; } } elsif(/^END/) { unless($mmgf) { print {$mmgj} $_; } $mmgf = 0; }
elsif(!$mmgf) { print {$mmgj} $_; } } close($mmga); close($mmgj); use File::Copy;
copy("$mmgb.tmp", $mmgb); $mailman::mmae = $mmfs; } sub mmre {
my($mmba) = shift; my($mmga) = new FileHandle(); my($mmgj) = new FileHandle();
my($mmfs) = $mailman::mmae; $mailman::mmae = 1; mmqj(); my($mmgd) =
"${mailman::mmv}/groups"; if((!open($mmga,"<$mmgd")) ||
(!open($mmgj,">$mmgd.tmp"))) { return; } flock($mmga,2); my($mmgh) = '';
while(defined($_ = <$mmga>)) { if(/^(\S+)\s+\"(\S+)\"\s*/) {
$mmgh = mmsw($1); unless($mmgh =~ /$mmba/i) { print {$mmgj} $_; } } else {
print {$mmgj} $_; } } close($mmga); close($mmgj); use File::Copy; copy("$mmgd.tmp",
$mmgd); $mailman::mmae = $mmfs; } sub mmrf {
my($mmfs) = $mailman::mmae; $mailman::mmae = 1; my($mmga) = new FileHandle();
my($mmgj) = new FileHandle(); mmqj(); my($mmgk) = ''; my($mmgl) = '';
my(@mmc) = $mmb->param; my($mmd) = 0; for($mmd=0;$mmd<$#mmc;$mmd++) {
my($mme) = $mmc[$mmd];; if($mme =~ /^ADDRESSITEM_(.*)$/) { my($mmgm) = $1;
if($mmgm eq 'NICKNAME') { $mmgk = $mmb->param($mme); } else { $mmgl .= "$mmgm " .
mmsv($mmb->param($mme)) . "\n"; } } } if($mmgk eq '') {
mmrb("Error: The nickname field is " . "required."); }
if($mmb->param('ADDRESSITEM_ADDRESS') eq '') {
mmrb("Error: The address field is " . "required."); }
my($mmgb) = "${mailman::mmv}/individuals"; if((!open($mmga,"<$mmgb")) ||
(!open($mmgj,">$mmgb.tmp"))) { if(!open($mmga,">$mmgb")) {
mmqc("Could not open the address file \"" . $mmgb .
"\" for storing this user's addresses.  "); } print {$mmga} "BEGIN " .
mmsv($mmgk) . "\n"; print {$mmga} $mmgl; print {$mmga} "END\n";
close($mmga); $mailman::mmae = $mmfs; return; } flock($mmga,2); my($mmge) = 0;
my($mmgf) = 0; my($mmgg) = ''; while(defined($_ = <$mmga>)) {
if(/^BEGIN\s+(\S+)\s*/) { $mmgg = mmsw($1); print {$mmgj} $_;
if($mmgg eq $mmgk) { $mmge = 1; $mmgf = 1; print {$mmgj} $mmgl; } } elsif(/^END/) {
$mmgf = 0; print {$mmgj} $_; } elsif(!$mmgf) { print {$mmgj} $_; } } unless($mmge) {
print {$mmgj} "BEGIN " . mmsv($mmgk) . "\n"; print {$mmgj} $mmgl;
print {$mmgj} "END\n"; } close($mmga); close($mmgj); use File::Copy;
copy("$mmgb.tmp", $mmgb); $mailman::mmae = $mmfs; } sub mmrg {
my($mmfs) = $mailman::mmae; $mailman::mmae = 1; my($mmga) = new FileHandle();
my($mmgj) = new FileHandle(); mmqj(); my($mmgk) =
$mmb->param('ADDRESSITEM_NICKNAME'); my($mmgn) =
mmsv($mmb->param('ADDRESSITEM_NICKNAME')); my($mmgo) = 
mmsv($mmb->param('ADDRESSITEM_ADDRESSES')); if($mmgk eq '') {
mmrc("Error: The nickname field is " . "required."); }
if($mmb->param('ADDRESSITEM_ADDRESSES') eq '') {
mmrc("Error: The address field is " . "required."); }
my($mmgd) = "${mailman::mmv}/groups"; if((!open($mmga,"<$mmgd")) ||
(!open($mmgj,">$mmgd.tmp"))) { if(!open($mmga,">$mmgd")) {
mmqc("Could not open the address file \"" . $mmgd .
"\" for storing this user's addresses.  "); } print {$mmga} "$mmgn \"$mmgo\"\n";
close($mmga); $mailman::mmae = $mmfs; return; } flock($mmga,2); my($mmgp) = 0;
my($mmgh) = ''; while(defined($_ = <$mmga>)) { if(/^(\S+)\s+\"(\S+)\"\s*/) {
$mmgh = mmsw($1); if($mmgh eq $mmgk) { $mmgp = 1; print {$mmgj}
"$mmgn \"$mmgo\"\n"; } else { print {$mmgj} $_; } } } unless($mmgp) { print {$mmgj}
"$mmgn \"$mmgo\"\n"; } close($mmga); close($mmgj); use File::Copy; copy("$mmgd.tmp",
$mmgd); $mailman::mmae = $mmfs; } sub mmrh {
my($mmbr) = 't_accounts.htm'; $mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; } mmrl();
if($mailman::mmdi) { my($mmgq, $mmgr) = mmsr($mmbr,
('ACCOUNT_EVEN','ACCOUNT_ODD')); my($mmfw) = 0; my($mmdj) = '';
foreach $mmdj (sort keys %mailman::mmdk) { my($mmcy) =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_USERNAME'}; my($mmcz) =
$mailman::mmdk{$mmdj}->{'ACCOUNTITEM_SERVER'};
$mailman::mmbh{'ACCOUNTITEM_ID'} = mmsv($mmdj);
$mailman::mmbh{'ACCOUNTITEM_USERNAME'} = $mmcy;
$mailman::mmbh{'ACCOUNTITEM_SERVER'} = $mmcz; if($mmfw%2==0) {
$mailman::mmbh{ACCOUNTS} .= mmso($mmgq,\%mailman::mmbh); } else {
$mailman::mmbh{ACCOUNTS} .= mmso($mmgr,\%mailman::mmbh); } $mmfw++;
} } else { $mailman::mmbh{'ACCOUNTS'} = mmsq($mmbr,
'NO_ACCOUNTS'); } mmss($mmbr,\%mailman::mmbh); } sub mmri {
my($mmbg) = shift; my($mmgs) = new FileHandle(); my($mmbr) = 't_account.htm';
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; } my($mmdj) = '';
if($mmb->param('ACCOUNT')) { $mmdj = $mmb->param('ACCOUNT'); mmqj();
my($mmgt) = "${mailman::mmv}/accounts"; if(!open($mmgs,"<$mmgt")) {
mmqc("Could not open the accounts file \"" . $mmgt .
"\" for storing this user's accounts."); } flock($mmgs,2); my($mmgu) = 0;
my($mmgv) = 0; my($mmgw) = ''; accountline: while(defined($_ = <$mmgs>)) {
if(/^BEGIN\s+(\S+)\s*/) { $mmgw = $1; if($mmgw eq $mmdj) { $mmgu = 1; $mmgv = 1; } }
elsif(/^END/) { if($mmgv) { close($mmgs); last accountline; } }
elsif($mmgv && /^(\S+)\s+(\S+)\s*$/) { $mailman::mmbh{$1} = mmsw($2); } }
close($mmgs); } if($mmbg ne '') { $mailman::mmbh{'ERROR'} = $mmbg; }
if($mailman::mmbh{'ACCOUNTITEM_FOLDER'}) { $mailman::mmbh{'FOLDERDEPOSITLIST'} =
mmti($mailman::mmbh{'ACCOUNTITEM_FOLDER'}); } else {
$mailman::mmbh{'FOLDERDEPOSITLIST'} = mmti('INBOX'); }
my(@mmc) = $mmb->param; my($mmd) = 0; for($mmd=0;$mmd<$#mmc;$mmd++) {
my($mme) = $mmc[$mmd];; if($mme =~ /^ACCOUNTITEM_(.*)$/) {
$mailman::mmbh{$mme} = $mmb->param($mme); } }
mmss($mmbr,\%mailman::mmbh); } sub mmrj { my($mmo) = $mailman::mmo;
my($mmq) = $mailman::mmq; my($strIncomingServer) = $mailman::strIncomingServer;
$mailman::mmbh{'ACCOUNTITEM_FOLDER'} =  $mmb->param('ACCOUNTITEM_FOLDER');
if($mmb->param('ACCOUNTITEM_USERNAME') eq '') {
mmri("Error: The username field is " . "required."); }
if($mmb->param('ACCOUNTITEM_PASSWORD') eq '') {
mmri("Error: The password field is " . "required."); }
if($mmb->param('ACCOUNTITEM_SERVER') eq '') {
mmri("Error: The server field is " . "required."); } $mailman::mmo = 
$mmb->param('ACCOUNTITEM_USERNAME'); $mailman::mmq =
$mmb->param('ACCOUNTITEM_PASSWORD'); $mailman::strIncomingServer =
$mmb->param('ACCOUNTITEM_SERVER'); my($mmbg) = ''; if($mmbg = mmqg()) {
$mailman::mmo = $mmo; $mailman::mmq = $mmq;
$mailman::strIncomingServer = $strIncomingServer; $mmbg =~ s/^\-ERR//i;
mmri('ERROR: ' . $mmbg); } else { mmqf($mma,"QUIT"); close $mma;
$mailman::mmbl = 0; $mailman::mmo = $mmo; $mailman::mmq = $mmq;
$mailman::strIncomingServer = $strIncomingServer; } my($mmfs) = $mailman::mmae;
$mailman::mmae = 1; my($mmgs) = new FileHandle(); my($mmgx) = new FileHandle();
mmqj(); my($mmdj) = ''; my($mmgy) = ''; my($mmgz) = '';
my(@mmc) = $mmb->param; my($mmd) = 0; if($mmb->param('ACCOUNTITEM_ID')) { $mmgy =
$mmgz = $mmb->param('ACCOUNTITEM_ID'); } else { $mmgy =
mmsv($mmb->param('ACCOUNTITEM_USERNAME').'@'.
$mmb->param('ACCOUNTITEM_SERVER')); $mmgz = $mmgy . "\n"; }
for($mmd=0;$mmd<$#mmc;$mmd++) { my($mme) = $mmc[$mmd];;
if($mme =~ /^ACCOUNTITEM_(.*)$/ && $mme ne 'ACCOUNTITEM_ID') { my($mmha) = $1;
$mmgz .= "$mme " . mmsv($mmb->param($mme)) . "\n"; } }
my($mmgt) = "${mailman::mmv}/accounts"; if((!open($mmgs,"<$mmgt")) ||
(!open($mmgx,">$mmgt.tmp"))) { if(!open($mmgs,">$mmgt")) {
mmqc("Could not open the account file \"" . $mmgt .
"\" for storing this user's accounts."); } print {$mmgs} "BEGIN ";
print {$mmgs} $mmgz; print {$mmgs} "END\n"; close($mmgs); $mailman::mmae = $mmfs;
return; } flock($mmgs,2); my($mmgu) = 0; my($mmgv) = 0; my($mmgw) = '';
while(defined($_ = <$mmgs>)) { if(/^BEGIN\s+(\S+)\s*/) { $mmgw = $1;
if($mmgw eq $mmgy) { $mmgu = 1; $mmgv = 1; print {$mmgx} "BEGIN $mmgz"; } else {
print {$mmgx} $_; } } elsif(/^END/) { $mmgv = 0; print {$mmgx} $_; } elsif(!$mmgv) {
print {$mmgx} $_; } } unless($mmgu) { print {$mmgx} "BEGIN "; print {$mmgx} $mmgz;
print {$mmgx} "END\n"; } close($mmgs); close($mmgx); use File::Copy;
copy("$mmgt.tmp", $mmgt); $mailman::mmae = $mmfs; } sub mmrk {
my($mmdj) = shift; my($mmgs) = new FileHandle(); my($mmgx) = new FileHandle();
my($mmfs) = $mailman::mmae; $mailman::mmae = 1; mmqj(); my($mmgt) =
"${mailman::mmv}/accounts"; if((!open($mmgs,"<$mmgt")) ||
(!open($mmgx,">$mmgt.tmp"))) { return; } flock($mmgs,2); my($mmgu) = 0; my($mmgv) = 0;
my($mmgw) = ''; while(defined($_ = <$mmgs>)) { if(/^BEGIN\s+(\S+)\s*/) { $mmgw = $1;
if($mmgw eq $mmdj) { $mmgu = 1; $mmgv = 1; } else { print {$mmgx} $_; } } elsif(/^END/) {
unless($mmgv) { print {$mmgx} $_; } $mmgv = 0; } elsif(!$mmgv) { print {$mmgx} $_; } }
close($mmgs); close($mmgx); use File::Copy; copy("$mmgt.tmp", $mmgt);
$mailman::mmae = $mmfs; } sub mmrl { my($mmhb) = new FileHandle();
mmqj(); my($mmhc) = "${mailman::mmv}/accounts"; if(!open($mmhb,"<$mmhc")) {
return; } flock($mmhb,2); my($mmdj) = ''; $mailman::mmdi = 0;
while(defined($_ = <$mmhb>)) { if(/^BEGIN\s+(\S+)\s*/) { $mmdj = $1;
$mailman::mmdi++; } elsif(/^(\S+)\s+(\S+)\s*$/) { $mailman::mmdk{$mmdj}->{$1} =
mmsw($2); } } close($mmhb); } sub mmrm {
my($mmhd) = shift; $mailman::mmbh{'URL'} = $mmhd;
mmss('t_backgroundframeset.htm',\%mailman::mmbh); }
sub mmrn {  my($mmhe) = @_; unless(defined($mmhe)) { $mmhe = 0; }
my($mmhf, $mmhg) = (0, 0); my($mmbr) = ''; if($mailman::mmae) {
if($mailman::mmah eq 'SENT') { my($mmhh) = 't_nf_messagelistsent.htm';
if(defined($mailman::mmag)) { $mmhh = $mailman::mmag . $mmhh; } if(-e
"${mailman::strLocalTemplateLocation}$mmhh") { $mmbr = 't_nf_messagelistsent.htm';
} else { $mmbr = 't_nf_messagelist.htm'; } } else { $mmbr = 't_nf_messagelist.htm'; } }
else { if($mailman::mmah eq 'SENT') { my($mmhh) = 't_f_messagelistsent.htm';
if(defined($mailman::mmag)) { $mmhh = $mailman::mmag . $mmhh; }
if(-e {$mailman::strLocalTemplateLocation . $mmhh}) {
$mmbr = 't_f_messagelistsent.htm'; } else { $mmbr = 't_f_messagelist.htm'; } } else {
$mmbr = 't_f_messagelist.htm'; } } my($mmhi, $mmhj, $mmhk, $mmhl) = ('','','','');
my($mmhm, $mmhn, $mmho) = ('','',''); if($mailman::iUserDiskQuota) { ($mmhi, $mmhj,
$mmhl, $mmhm, $mmhk, $mmhn, $mmho) = mmsr($mmbr,
('MESSAGE_EVEN', 'MESSAGE_ODD', 'ATTACHMENT_IMAGE', 'READ_IMAGE', 'UNREAD_IMAGE',
'QUOTA_STATUS', 'QUOTA_ERROR')); } else { ($mmhi, $mmhj, $mmhl, $mmhm, $mmhk) =
mmsr($mmbr, ('MESSAGE_EVEN', 'MESSAGE_ODD',
'ATTACHMENT_IMAGE', 'READ_IMAGE', 'UNREAD_IMAGE')); }
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'NUM'} = $mailman::mmcg; if($mailman::iUserDiskQuota) {
unless($mailman::mmdm) { mmtj(); }
$mailman::mmbh{'QUOTA_USAGE_PERCENT'} = sprintf("%2.1f", ($mailman::mmdm/
$mailman::iUserDiskQuota)*100); $mailman::mmbh{'QUOTA_LIMIT_MB'} =
sprintf("%2.1f", ($mailman::iUserDiskQuota / (1024*1024)));
$mailman::mmbh{'QUOTA_STATUS'} = mmso($mmhn,\%mailman::mmbh);
if($mailman::mmdm >=  $mailman::iUserDiskQuota) { $mailman::mmbh{'QUOTA_STATUS'} .=
$mmho; } } if(defined($mailman::strFromDomainName)) {
$mailman::mmbh{'SERVER'} = $mailman::strFromDomainName; } else {
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer; } if($mailman::mmah eq '')
{ $mailman::mmah = 'INBOX'; } $mailman::mmbh{'FOLDERLIST'} = mmti();
$mailman::mmbh{'CURRENTFOLDER'} = mmqt($mailman::mmah); use Fcntl; my($mmde) = 
$mailman::mmv . '/' . mmsv($mailman::mmah);
my($mmdz) = new FileHandle(); my($mmea) = "${mmde}/msglist"; retry:
unless(open($mmdz,$mmea)) { $mailman::mmbh{'NUM'} = 0;
$mailman::mmbh{'MESSAGELIST'} = mmsq($mmbr,'NOMESSAGES');
mmss($mmbr,\%mailman::mmbh); } flock($mmdz,2); if(<$mmdz> =~ /^(\d+)\s/) {
$mailman::mmcg = $1; $mailman::mmbh{'NUM'} = $mailman::mmcg; } else { close($mmdz);
mmto($mmde); goto retry; } mmqw();
$mailman::iMessagesPerPage = $mailman::mmaq; if($mailman::mmcg > 0) {
if($mmhe == 0) { $mmhe = $mailman::mmcg; } my($mmhp); if($mailman::mmcg > 1) {
my($mmfw) = 0; for($mmfw=$mailman::mmcg; $mmfw>0;
$mmfw-=$mailman::iMessagesPerPage) { my($mmhq) = $mmfw;
my($mmhr) = $mmfw-$mailman::iMessagesPerPage+1; my($mmhs) = ''; if($mmhr<1) {
$mmhr = 1; } if($mmhe <= $mmhq && $mmhe >= $mmhr) { $mmhp = 1; $mmhf = $mmhq;
$mmhg = $mmhr; } else { $mmhp = 0; } if($mmhq == $mmhr) { $mmhs = "$mmhq"; } else {
$mmhs = "$mmhq-$mmhr"; } if($mailman::mmae) { if($mmhp) {
$mailman::mmbh{'PAGELINKS'} .=  "<b>[$mmhs]</b> "; } else {
$mailman::mmbh{'PAGELINKS'} .=  qq|<input type="submit" name="LIST:$mmhq" | .
qq|value="$mmhs">|; } } else { if($mmhp) { $mailman::mmbh{'PAGELINKS'} .= 
"<b>[$mmhs]</b> "; } else { $mailman::mmbh{'PAGELINKS'} .=
qq|<a href="$mailman::mmab?LIST:$mmhq=TRUE">| . qq|[$mmhs]</a> |; } } } } else {
$mailman::mmbh{'PAGELINKS'} = ''; $mmhf = 1; $mmhg = 1; } }
$mailman::mmbh{'MESSAGELIST'} = ''; my $mmfw = 0;
nextmessage: while(defined($_ = <$mmdz>)) { if(($mmfw+1) < $mmhg) {
if(mmqi($_)) { $mmfw++; } next nextmessage; } if(($mmfw+1) > $mmhf) {
last nextmessage; } unless(mmqi($_)) { next nextmessage; }
$mailman::mmbh{'FROM'} = $mailman::mmdb; $mailman::mmbh{'TO'} = $mailman::mmda;
$mailman::mmbh{'SUBJECT'} = $mailman::mmdc;
$mailman::mmbh{'DATE'} = $mailman::mmdd;
$mailman::mmbh{'ID'} = mmsv($mailman::mmcm);
$mailman::mmbh{'MESSAGENUM'} = $mmfw+1; $mailman::mmbh{'SIZE'} = $mailman::mmch;
if($mailman::mmcu) { $mailman::mmbh{'ATTACHMENT_IMAGE'} = $mmhl; } else {
$mailman::mmbh{'ATTACHMENT_IMAGE'} = ''; } if(defined($mailman::mmcv) &&
$mailman::mmcv =~ /R/i) { $mailman::mmbh{'OPENIMAGE'} = $mmhm; } else {
$mailman::mmbh{'OPENIMAGE'} = $mmhk; } my($mmht) = ''; if(($mmfw+1)%2==0) { $mmht =
mmso($mmhi,\%mailman::mmbh); } else { $mmht =
mmso($mmhj,\%mailman::mmbh); } $mmfw++;
$mailman::mmbh{'MESSAGELIST'} = $mmht . $mailman::mmbh{'MESSAGELIST'}; }
close($mmdz); if($mailman::mmbh{'MESSAGELIST'} eq '') {
$mailman::mmbh{'MESSAGELIST'} = mmsq($mmbr,'NOMESSAGES'); }

print eval(mmrs($mailman::mhaa[2]));
 }
sub mmro { my($mmbj,$mmif) =  @_; my($mmig) = 0; my($mmbz) = '';
if($mmif != 0) { $mmbj = mmsv( mmrp(
mmsw($mmbj),$mmif)); if($mmbj eq '') { if($mailman::mmae) {
mmrn(); } elsif($mmif == -1) { mmqc("No prev message."); } else {
mmqc("No next message."); } } } my($mmde) =  $mailman::mmv . '/' .
mmsv($mailman::mmah); my($mmej) = "${mmde}/$mmbj";
my($mmem) = new FileHandle(); $mmig = 0; if(open($mmem,"<$mmej")) {
while(defined($mmbz = <$mmem>)) { $mailman::mmih[$mmig++] = $mmbz; }        } else {
mmqc("Could not load the specified message from disk."); } seek($mmem,0,0);
mmqq($mmem); close($mmem); return $mmbj; } sub mmrp {
my($mmbj,$mmif) = @_; my($mmci) = 0; my($mmde) =  $mailman::mmv . '/' .
mmsv($mailman::mmah); my($mmdz) = new FileHandle();
my($mmea) = "${mmde}/msglist"; retry: if(open($mmdz,"<$mmea")) { flock($mmdz,2);
if(<$mmdz> =~ /^(\d+)\s/) { $mmci = $1; } else { close($mmdz); mmto($mmde);
goto retry; } my($mmii) = 0; my($mmij, $mmik) = ('', ''); my($mmil) = 0;
while(defined($_ = <$mmdz>)) { if(/^([^\|]+)\|/) { $mmii++; $mmik = $mmij;
$mmij = mmsw($1); if($mmil) { close($mmdz); return $mmij; }
if($mmij eq $mmbj) { if($mmif == -1) { close($mmdz); return $mmik; } if($mmii < $mmci) {
$mmil = 1; } else { close($mmdz); return ''; } } } } close($mmdz); } return ''; }
 sub mmrq
{ print "Content-type: text/html\n\n"; print unpack('u',
"M5&AI<R!D96UO(&EN<W1A;&QA=&EO;B!O9B!-86EL36%N(&AA<R!E>'!I<F5D!+@``"); exit(0); }

sub mmrr { my($mmim,$mmin) = @_; my($mmht) = ''; my($mmio) = '';
my($mmip) = ''; my($mmiq) = 0; my($mmir) = 0; my($mmis) = 0; my($mmit) = '';
my($mmiu) = ''; my($mmiv) = localtime(time); $mmiv = mmsz($mmiv);
my(@mmiw,@mmix,@mmiy,$mmiz,@mmja); my($mmjb); my(@mmjc,@mmjd,$mmje,@mmjf);
if($mailman::mmct) { my($mmer)=0; $mmiz=0; my($mmez)= '';
headerline: foreach $_ (@$mmim) { $mmez .= $_; if(/^[\r\n]+$/){ last headerline; }
}        $mmez =~ s/[\r\n]/ /g; if($mmez =~
/Content-type\:\s+multipart\/mixed;.*boundary\=\"([^\"\;]+)\"\;?\s/si) {
$mmjb = 'multipart/mixed'; $mmio = $1; $mmiu = mmsx($mmio);
$mailman::mmjg = 1; } elsif($mmez =~
/Content-type\:\s+multipart\/mixed;.*boundary\=\"?([^\"\;\s]+)\"?\;?\s/si) {
$mmjb = 'multipart/mixed'; $mmio = $1; $mmiu = mmsx($mmio);
$mailman::mmjg = 1; } elsif($mmez =~
/Content-type\:\s+multipart\/alternative;.*boundary\=\"?([^\"\;]+)\"?\;?\s/si) {
$mmjb = 'multipart/alternative'; $mmio = $1; $mmiu = mmsx($mmio); }
elsif($mmez =~ /Content-type\:\s+([^\;]+);.*name\=\"?([^\"\;]+)\"?\;?\s/si) {
$mmjb = $mmix[0] = $1; $mmip = $mmja[0] = $2; $mmiq = 0; $mmiw[0][$mmir++] = 
"Content-type: $1; name=\"$2\"\n"; } elsif($mmez =~ /Content-type\:\s+([^\;]+)/si) {
$mmjb = $mmix[0] = $1; $mmip = $mmja[0] = 'messagebody'; $mmiq = 0;
$mmiw[0][$mmir++] =  "Content-type: $1\n"; } if($mmez =~
/Content-transfer-encoding\:\s+(\S+)\s/si) { $mmiw[0][$mmir++] = 
"Content-transfer-encoding: $1\n"; } $mmiw[0][$mmir++] = "\n"; $mmer=0; $mmiz=0;
messageline: foreach $_ (@$mmim) { if($mmer) {  if(/^\-\-$mmiu\-\-/) {
last messageline; } if(/^\-\-$mmiu/) { $mmiz++; $mmir=0; $mmis=0; $mmiy[$mmiz] =
$mmio . 'P' . $mmiz; next messageline; } $mmiw[$mmiz][$mmir++] = $_; if(/^[\r\n]+$/)
{ if(!$mmis) { $mmis = 1; unless(defined($mmja[$mmiz])) { $mmja[$mmiz] = 'Untitled'; } } }
if(!$mmis) { if(/name\=\"?([^\"]+)\"?/i) { $mmja[$mmiz] = $1; }
if(/^Content-type\: ([^\;]+)\;?/i) { $mmit = $1; $mmix[$mmiz] = $mmit; } } }
if(/^[\r\n]+$/) { $mmer = 1; } } } if($mailman::mmbk eq '0') { mmru($mmiw[0]);
} my($mmjh)=1; if($mailman::mmbk ne '') { for(;$mmjh<=$mmiz;$mmjh++) {
if($mmiy[$mmjh] eq $mailman::mmbk) { mmru($mmiw[$mmjh]); } } }
if($mailman::mmct) { if($mmjb =~ /text\/plain/i) {
$mmht = mmrz($mmim, $mmin); }
elsif($mmjb !~ /multipart\/mixed/i && $mmjb !~ /multipart\/alternative/i) {
if($mmin) { $mmht = mmrz($mmim, $mmin); } else { if($mailman::mmae) {
$mmht .=  qq|<p>\n| . qq|<input type="hidden" name="UNIQUE" value="$mmiv">\n| .
qq|<input type="submit" | . qq|name="SHOW:${mailman::mmeo}mimepart:0" | .
qq|value="$mmip">\n| . qq|</p>\n|; } else { if($mmip =~ /\.(jpg)|(gif)|(png)\s*$/i) {
$mmht .= qq|<p>\n| . qq|<center>\n| .
qq|<table cellspacing=0 cellpadding=0 border=0>\n| .
qq|<tr><td align="center"><b>Attachment 1:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:0=TRUE">\n| .
qq|$mmip</a></td></tr>\n| . qq|<tr><td>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:0=TRUE">\n| .
qq|<img src="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:0=TRUE"></a>\n| .
qq|</td></tr>\n| . qq|</table></center></p>\n|; } else { $mmht .=
qq|<p><b>Attachment 1:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:0=TRUE">\n| .
qq|$mmip</a></p>\n|; } } } return $mmht; } my($mmjh)=1;
if($mmjb =~ /multipart\/mixed/i) { if($mmix[1] =~ /multipart\/alternative/i ||
$mmix[1] =~ /multipart\/mixed/i) { $mmht = mmrr($mmiw[1], $mmin); }
elsif($mmix[1] =~ /text\/plain/i) { $mmht = mmrz($mmiw[1],
$mmin); } elsif($mmix[1] =~ /text\/html/i) { if($mmin) {
$mmht = mmrz($mmiw[1], $mmin); } else {
$mmht = mmsa($mmiw[1]); } } else { $mmjh = 0; } }
elsif($mmjb eq 'multipart/alternative') { my($mmji) = 1; for(;$mmji<=$mmiz;$mmji++)
{ if($mmix[$mmji] =~ /text\/html/i && !$mmin) { $mmht = 
mmsa($mmiw[$mmji]); return $mmht; } } $mmji = 1;
for(;$mmji<=$mmiz;$mmji++) { if($mmix[$mmji] =~ /text\/plain/i) { $mmht =
mmrz($mmiw[$mmji], $mmin); return $mmht; } } } else {
$mmht = mmrz($mmim, $mmin); return($mmht); } if($mmin) {
return($mmht); } if($mmjb eq 'multipart/mixed') { for(;$mmjh<$mmiz;$mmjh++) {
my($mmjj) = $mmiy[$mmjh+1]; $mmjj =  mmsv($mmjj); if($mailman::mmae) {
$mmht .=  qq|<p>\n| . qq|<input type="hidden" name="UNIQUE" value="$mmiv">\n| .
qq|<input type="submit" | . qq|name="SHOW:${mailman::mmeo}mimepart:$mmjj" | .
qq|value="$mmja[$mmjh+1]">\n| . qq|</p>\n|; } else { if($mmja[$mmjh+1] =~
/\.(jpg)|(gif)|(png)\s*$/i) { $mmht .= qq|<p>\n| . qq|<center>\n| .
qq|<table cellspacing=0 cellpadding=0 border=0>\n| .
qq|<tr><td align="center"><b>Attachment #$mmjh:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjj=TRUE">\n| .
qq|$mmja[$mmjh+1]</a></td></tr>\n| . qq|<tr><td align="center">\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjj=TRUE">\n| .
qq|<img src="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjj=TRUE"></a>\n| .
qq|</td></tr>\n| . qq|</table></center></p>\n|; } else { $mmht .=
qq|<p><b>Attachment #$mmjh:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjj=TRUE">\n| .
qq|$mmja[$mmjh+1]</a></p>\n|; } } } } } else { $mmje=0;
plaintextline: foreach $_ (@$mmim) { if(/^begin \d\d\d (\S+)\s*$/i) { $mmje++;
$mmir=0; $mmjf[$mmje] = $1; $mmjd[$mmje] = $1 . 'P' . $mmje; next plaintextline; }
elsif($mmje>0 && /^end\s*$/i) { $mmje++; $mmir=0; $mmjc[$mmje] .= "Fake Header\n\n";
next plaintextline; } $mmjc[$mmje][$mmir++] = $_; } if($mailman::mmbk ne '') {
my($mmjk) = 0; for(;$mmjk<=$mmje;$mmjk++) { if($mmjd[$mmjk] eq $mailman::mmbk) {
if($mmjf[$mmjk] eq '') { $mmht = mmrz($mmjc[$mmjk], $mmin);
return $mmht; } else { mmry($mmjc[$mmjk],$mmjf[$mmjk]); } } } } else {
my($mmjk) = 0; for(;$mmjk<=$mmje;$mmjk++) {
if(!defined($mmjf[$mmjk]) || $mmjf[$mmjk] eq '') {
$mmht .= mmrz($mmjc[$mmjk], $mmin); } elsif(!$mmin) {
my($mmjl) = $mmjd[$mmjk]; $mmjl =  mmsv($mmjl); if($mailman::mmae) {
$mmht .= '<form method="post" action="' . $mailman::mmab .
'"><input type="submit" name="' . 'SHOW:' . $mailman::mmeo . 'mimepart:' . $mmjl . 
"\" value=\"$mmjf[$mmjk]\"></form><br>\n"; } else { if($mmjf[$mmjk] =~
/\.(jpg)|(gif)|(png)\s*$/i) { $mmht .= qq|<p>\n| . qq|<center>\n| .
qq|<table cellspacing=0 cellpadding=0 border=0>\n| .
qq|<tr><td align="center"><b>Attachment #$mmjk:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjl=TRUE">\n| .
qq|$mmjf[$mmjk]</a></td></tr>\n| . qq|<tr><td align="center">\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjl=TRUE">\n| .
qq|<img src="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjl=TRUE"></a>\n| .
qq|</td></tr>\n| . qq|</table></center></p>\n|; } else { $mmht .=
qq|<p><b>Attachment #$mmjk:</b>\n| .
qq|<a href="$mailman::mmab?SHOW:${mailman::mmeo}mimepart:$mmjl=TRUE">\n| .
qq|$mmjf[$mmjk]</a></p>\n|; } } } } } return($mmht); } return($mmht); }

 sub mmrs {
my($mmjm) = shift; $mmjm =~ s/([a-fA-F0-9]{2})/pack("C",hex($1))/eg; return $mmjm;
} sub mmrt { my($mmhu) = ''; {
my($mmhv,$mmhw,$mmhx,$mmhy,$mmhz,$mmia,$mmib,$mmic,$mmid) = gmtime(time);
my(@mmie) = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',
'Oct','Nov','Dec'); $mmhu = "$mmhy $mmie[$mmhz] " . ($mmia + 1900) . 
" $mmhx:$mmhw:$mmhv +0000"; } return ( ( 129639611 - mmtc($mmhu) ) /
86400  ); }
 sub mmru { my($mmjn) = @_; my($mmjo,$mmjp) = (0, 0);
my($mmis) = 0; my($mmbz) = ''; my($mmjq) = ''; my($mmez) = ''; my($mmjr) = '';
my($mmel) = 'Untitled'; foreach $mmbz (@$mmjn) {
if($mmbz =~ /^Content-transfer-encoding\: base64/i) { $mmjo = 1; }
elsif($mmbz =~ /^Content-transfer-encoding\: quoted-printable/i) { $mmjp = 1; }
elsif($mmbz =~ /^Content-Disposition\:/i) { } else { if($mmis && $mmjo) {
$mmjq .= $mmbz; } elsif($mmis && $mmjp) { $mmjq .= $mmbz; } elsif($mmis) {
$mmjq .= $mmbz; } else { $mmez .= $mmbz; } } if($mmbz =~ /^[\r\n]+$/) { $mmis = 1;
$mmez =~ s/[\r\n]+[ \t]+(\S)/ $1/gs; } if(!$mmis &&
$mmbz =~ /name\=\"?([^\"\;]+)\"?\;?\s/si) { $mmel = $1; } } if($mmjo) {
$mmjr = mmrx($mmjq); } elsif($mmjp) { $mmjr = mmrw($mmjq); }
else { $mmjr = $mmjq; } print "Expires: Sun, 03 May 1998 16:00:00 GMT\n"; 
my($mmjs,$mmjt,$mmju) = mmsy(); if($mmjs !~ /MSIE/i) {
print "Cache-control: no-cache\n"; } unless($mailman::mmy) { print $mmez;
print $mmjr; exit(0); } else { unless(-d $mailman::mmw) {
unless(mkdir($mailman::mmw,0755)) {
mmqc("Could not create temporary directory for " .
"storing the attachment file.  Make sure that " . "the directory " .
"\"$mailman::mmw\" exists " . "and is writable by the web user."); }
if(defined($mailman::iLocalDirectoryPermissions)) {
mmtb($mailman::mmw, $mailman::iLocalDirectoryPermissions); } }
my $mmjv = $mmel; if($mmel =~ /^(.+)(\.[^\.]+)$/) { my $mmjw = $1; my $mmjx = $2;
$mmel = mmsv(mmsv($mmjw)) . $mmjx; } else {
$mmel = mmsv(mmsv($mmel)); } my($mmjy) = new FileHandle();
my($mmjz) = $mailman::mmw . '/' . $mmel; unless(open($mmjy,">$mmjz")) {
mmqc("Could not create temporary attachment file in \"" .
$mmjz ."\".  Make sure that the  " . "directory is writable by the web user."); }
binmode($mmjy); print {$mmjy} $mmjr; close($mmjy); if ($mmjv =~ /^(.+)(\.[^\.]+)$/)
{ my($mmka) = $mailman::mmx . '/' .
mmsv(mmsv(mmsv($1))) . $2;
print $mmb->redirect($mmka); } else { my($mmka) = $mailman::mmx . '/' . $mmel;
print $mmb->redirect($mmka); } exit(0); } } sub mmrv { my $mmjq = shift;
$mmjq =~ tr/\_/\ /; return $mmjq; } sub mmrw { my($mmjq) = @_;
my($mmkb); $mmjq =~ s/\s+(\r?\n)/$1/g; $mmjq =~ s/=\r?\n//g; $mmkb = $mmjq;
$mmkb =~ s/=([\da-fA-F]{2})/pack("C", hex($1))/ge; return($mmkb); }
sub mmrx { my($mmjq) = @_; my($mmkb);
$mmjq =~ tr|A-Za-z0-9+=/||cd;             if(length($mmjq)%4) { return($mmjq); }
$mmjq =~ s/=+$//; $mmjq =~ tr|A-Za-z0-9+/| -_|; while($mmjq =~ /(.{1,60})/gs) {
my($mmkc) = chr(32+length($1)*3/4); $mmkb .= unpack("u",$mmkc . $1 ); }
return($mmkb); } sub mmry { my($mmkd,$mmke) = @_;
print "Expires: Sun, 03 May 1998 16:00:00 GMT\n";  my($mmjs,$mmjt,$mmju) =
mmsy(); if($mmjs !~ /MSIE/i) { print "Cache-control: no-cache\n";  }
unless($mailman::mmy) { print
qq|Content-Type: application\/octet-stream; name="$mmke"\n\n|; my($mmht) = '';
my($mmbz) = ''; foreach $mmbz (@$mmkd) { $mmht .= unpack('u',$mmbz); } print $mmht;
exit(0); } else { unless(-d $mailman::mmw) { unless(mkdir($mailman::mmw,0755)) {
mmqc("Could not create temporary directory for " .
"storing the attachment file.  Make sure that " . "the directory " .
"\"$mailman::mmw\" exists " . "and is writable by the web user."); }
if(defined($mailman::iLocalDirectoryPermissions)) {
mmtb($mailman::mmw, $mailman::iLocalDirectoryPermissions); } }
my($mmjy) = new FileHandle(); my($mmjz) = $mailman::mmw . '/' . $mmke;
unless(open($mmjy,">$mmjz")) {
mmqc("Could not temporary attachment file in \"" .
$mmjz ."\".  Make sure that the  " . "directory is writable by the web user."); }
binmode($mmjy); my($mmbz) = ''; foreach $mmbz (@$mmkd) {
print {$mmjy} unpack('u',$mmbz); } close($mmjy); my($mmka) =
$mailman::mmx . '/' . $mmke; print $mmb->redirect($mmka); exit(0); } }
sub mmrz { my($mmim,$mmin) = @_; my($mmjo,$mmjp); my($mmht) = '';
my($mmer) = 0; my($mmjq) = ''; if(!$mmin) { $mmht = "<pre>\n"; } $mmer=0;
foreach $_ (@$mmim) { if(!$mmer) { if(/^Content-transfer-encoding\: base64/i) {
$mmjo = 1; } elsif(/^Content-transfer-encoding\: quoted-printable/i) { $mmjp = 1; } }
if($mmer) { my($mmkf) = ''; if($mmjp || $mmjo) { $mmjq = $_; if($mmjo) {
$mmkf = mmrx($mmjq); } elsif($mmjp) { $mmkf = mmrw($mmjq); }
} else { $mmkf = $_; } my($mmkg) = length($mmkf); my($mmkh) = ''; if($mmin) {
$mmkh = $mmkf; } else { $mmkh = mmqt($mmkf); } my($mmki) = 90 +
(length($mmkh) - $mmkg); $mmkh =~ s/([^\n]{1,$mmki})\s/$1\n/g; $mmkh =~ s/\015//g;
if($mmin) { $mmkh = '> ' . $mmkh; } $mmht .= $mmkh ; } if(/^[\r\n]+$/){ $mmer = 1; } }
if($mmjo) { $mmht .= mmrx($mmjq); } elsif($mmjp) {
$mmht .= mmrw($mmjq); } if(!$mmin) { $mmht .= "</pre>\n"; }
return $mmht; } sub mmsa { my($mmim) = @_; my($mmjo,$mmjp);
my($mmjq) = ''; my($mmht) = ''; my($mmer) = 0; foreach $_ (@$mmim) { if(!$mmer) {
if(/^Content-transfer-encoding\: base64/i) { $mmjo = 1; }
elsif(/^Content-transfer-encoding\: quoted-printable/i) { $mmjp = 1; } } if($mmer) { 
if($mmjp || $mmjo) { $mmjq .= $_; } else { my($mmkh) = $_; $mmkh =~ s/\r//g;
$mmht .= $mmkh; } } if(/^[\r\n]+$/){ $mmer = 1; } } if($mmjo) {
$mmht .= mmrx($mmjq); } elsif($mmjp) {
$mmht .= mmrw($mmjq); }
$mmht =~ s/\<\/?(html|head|body|title)[^\>]*\>//sig; return $mmht; }
sub mmsb { my($mmbj,$mmif) =  @_; my($mmci) = 0; my($mmkj) = 0; my($mmde) = 
$mailman::mmv . '/' . mmsv($mailman::mmah);
my($mmdz) = new FileHandle(); my($mmdt) = ''; my(%mmdu) = (); my($mmkk) = '';
my($mmkl) = ''; my($mmkm) = 0; my($mmii) = 0; my($mmdx) = 0;
my($mmea) = "${mmde}/msglist"; retry: if(open($mmdz,"<$mmea")) { flock($mmdz,2);
if(<$mmdz> =~ /^(\d+)\s/) { $mailman::mmfc = $1; } else { close($mmdz);
mmto($mmde); goto retry; } messageloop: while(defined($_ = <$mmdz>)) { chomp;
if(/^([^\|]+)\|/ && mmqi($_)) { $mmii++;
my($mmij) = $mailman::mmcm; unless($mmkj) { $mmci++; }
unless(defined($mailman::mmcv) && $mailman::mmcv =~ /R/i) { $mmdx++; }
my($mmec) = $mailman::mmcq; my($mmed) = 0; while(defined($mmdu{$mmec})) {
if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) { $mmed++; } $mmec .= "_$mmed"; }
$mmdu{$mmec} = $_; if($mmij eq $mmbj) { $mmkj = 1; $mailman::mmeq = $mmii;
if($mailman::mmcv !~ /R/i) { $mmdx--; $mmkk = $_; $mmkl = $mmec; $mmkm = 1; } } }
elsif(/^DELETED\:\s+(\S+)\s*$/) { my($mmeb) = mmsw($1);
$mmdt .= $_ . "\n"; } elsif(/^\S+\:\s+(\S+)\s*$/) { my($mmeb) = mmsw($1);
$mmdt .= $_ . "\n"; } } close($mmdz); }
$mailman::mmeo = mmro(mmsv($mmbj),$mmif); my($mmbr) = '';
if($mailman::mmae) { $mmbr = 't_nf_message.htm'; } else { $mmbr = 't_f_message.htm'; }
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'NUM'} = $mailman::mmfc; $mailman::mmbh{'ID'} = $mailman::mmeo;
$mailman::mmbh{'TO'} = $mailman::mmda; $mailman::mmbh{'FROM'} = $mailman::mmdb;
$mailman::mmbh{'DATE'} = $mailman::mmcp;
$mailman::mmbh{'SUBJECT'} = $mailman::mmdc;
$mailman::mmbh{'MESSAGENUM'} = $mailman::mmeq;
$mailman::mmbh{'MESSAGE'} = mmrr(\@mailman::mmih);
$mailman::mmbh{'MESSAGENUM'} = $mmci + $mmif;
$mailman::mmbh{'FOLDERLIST'} = mmti();
$mailman::mmbh{'CC'} = $mailman::mmey; $mailman::mmkn = 
mmsq($mmbr,'CCLINE'); if($mailman::mmcn eq '') {
$mailman::mmkn = ''; } else { $mailman::mmkn =
mmso($mailman::mmkn,\%mailman::mmbh); }
$mailman::mmbh{'CCLINE'} = $mailman::mmkn;
mmss($mmbr,\%mailman::mmbh,1); if($mmkm) { mmqi($mmkk);
$mailman::mmcv .= 'R'; $mmkk = mmqh(undef,undef);
$mmdu{$mmkl} = $mmkk; unless(open($mmdz,">$mmea")) {
mmqc("Could not create user message list in \"" .
$mmea ."\".  Make sure that the  " . "directory is writable by the web user."); }
flock($mmdz,2); $mailman::mmcg = $mmci; print {$mmdz} "$mmii $mmdx\n";
my($mmek) = ''; foreach $mmek (sort {$a <=> $b} keys %mmdu) {
print {$mmdz} $mmdu{$mmek} . "\n"; } print {$mmdz} "\n" . $mmdt; close($mmdz); }
exit(1); } sub mmsc { my($mmbj,$mmif) =  @_;
$mailman::mmeo = mmro(mmsv($mmbj),$mmif); my($mmbr) = '';
if($mailman::mmae) { $mmbr = 't_nf_message.htm'; } else { $mmbr = 't_f_message.htm'; }
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'NUM'} = $mailman::mmfc; $mailman::mmbh{'ID'} = $mailman::mmeo;
$mailman::mmbh{'MESSAGENUM'} = $mailman::mmeq;
$mailman::mmbh{'TO'} = $mailman::mmda; $mailman::mmbh{'FROM'} = $mailman::mmdb;
$mailman::mmbh{'DATE'} = $mailman::mmcp;
$mailman::mmbh{'SUBJECT'} = $mailman::mmdc;
$mailman::mmbh{'FOLDERLIST'} = mmti();
$mailman::mmbh{'CC'} = $mailman::mmey; $mailman::mmkn = 
mmsq($mmbr,'CCLINE'); if($mailman::mmcn eq '') {
$mailman::mmkn = ''; } else {
$mailman::mmkn = mmso($mailman::mmkn,\%mailman::mmbh); }
$mailman::mmbh{'CCLINE'} = $mailman::mmkn; $mailman::mmbh{'MESSAGE'} = "<pre>\n";
my($mmbz) = ''; foreach $mmbz (@mailman::mmih) { $mmbz =~ s/\015//g;
$mmbz =~ s/\&/\&amp\;/g; $mmbz =~ s/\</\&lt\;/g; $mmbz =~ s/\>/\&gt\;/g;
$mailman::mmbh{'MESSAGE'} .= $mmbz; } $mailman::mmbh{'MESSAGE'} .= "</pre>\n";
mmss($mmbr,\%mailman::mmbh); } sub mmsd { my($mmbj) =  @_;
$mailman::mmcg = mmqs($mmbj); mmqf($mma,"DELE $mailman::mmcg");
my($mmcf) = ''; $mmcf = <$mma>; unless($mmcf =~ /^\+OK/) { mmqc($mmcf); } }
sub mmse { my($mmbj) =  @_; mmqw(); if($mailman::mmat &&
$mailman::mmah !~ /^TRASH$/i) { unless(mmsh($mmbj,'TRASH')) {
mmqc("There was an unknown error copying this message " .
"into the 'TRASH' folder.  The deletion was " . "aborted."); } }
mmsf($mmbj); if($mailman::mmah ne 'INBOX') {
mmsg($mmbj); } } sub mmsf { my($mmbj,$mmko) = @_;
unless($mmko) { $mmko = 'DELETED'; } my($mmde) =  $mailman::mmv . '/' .
mmsv($mailman::mmah); my($mmea) = "${mmde}/msglist";
my($mmdz) = new FileHandle(); my($mmkp) = new FileHandle(); retry:
if(!open($mmdz,"+<$mmea")) {
mmqc("Could not open message index for deletion."); return; }
if(!open($mmkp,">$mmea.tmp")) {
mmqc("Could not create backup message index."); return; } flock($mmdz,2);
my($mmbz) = ''; $mmbz = <$mmdz>; if($mmbz =~ /^(\d+)\s(\d+)\s/) {
$mailman::mmfc = $1; $mailman::mmfc--; my($mmkq) = ($2 - 1);
print {$mmkp} "$mailman::mmfc $mmkq\n"; } elsif($mmbz =~ /^(\d+)\s/) {
$mailman::mmfc = $1; $mailman::mmfc--; print {$mmkp} "$mailman::mmfc\n"; } else {
close($mmdz); close($mmkp); mmto($mmde); goto retry; } my($mmkr) = 0;
while(defined($_ = <$mmdz>)) { if((/^([^\|]+)\|/)||(/^\S+\:\s+(\S+)\s*$/)) {
my($mmks) = mmsw($1); if($mmks eq $mmbj) { if($mailman::mmah eq 'INBOX')
{ print {$mmkp} "$mmko: " . mmsv($mmks) . "\n"; } $mmkr = 1; } else {
print {$mmkp} $_; } } } close($mmkp); if($mmkr) { if(!open($mmkp,"<$mmea.tmp")) {
mmqc("Could not open backup message index."); return; } seek($mmdz,0,0);
truncate($mmdz,0); while(defined($_ = <$mmkp>)) { print {$mmdz} $_; } close($mmkp);
unlink($mmde . '/' . mmsv($mmbj)); } close($mmdz); } sub mmsg {
my($mmbj) = shift; my($mmdz) = new FileHandle(); my($mmkp) = new FileHandle();
my($mmea) = "${mailman::mmv}/INBOX/msglist"; retry: if(open($mmdz,"<$mmea") &&
open($mmkp,">$mmea.tmp")) { flock($mmdz,2); if(<$mmdz> =~ /^(\d+)\s/) {
print {$mmkp} "$1\n"; } else { close($mmdz); close($mmkp);
mmto("${mailman::mmv}/INBOX"); goto retry; } while(defined($_ = <$mmdz>)) {
if(/^\S+\:\s+(\S+)\s*$/) { my($mmeb) = mmsw($1); unless($mmeb eq $mmbj) {
print {$mmkp} $_; } } else { print {$mmkp} $_; } } print {$mmkp} "DELETED: " . 
mmsv($mmbj) . "\n"; close($mmdz); close($mmkp); use File::Copy;
copy("$mmea.tmp", $mmea); } } sub mmsh { my($mmbj, $mmbm) = @_;
my($mmde) =  $mailman::mmv . '/' . mmsv($mailman::mmah);
my($mmkt) = mmsv($mmbj); my($mmea) = "${mmde}/msglist";
my($mmdz) = new FileHandle(); retry: if(!open($mmdz,"+<$mmea")) {
mmqc("Could not open message index."); return 0; } flock($mmdz,2);
if(<$mmdz> =~ /^(\d+)\s/) { $mailman::mmfc = $1; } else { close($mmdz);
mmto($mmde); goto retry; } my($mmcq) = ''; my($mmcw) = '';
while(defined($_ = <$mmdz>)) { if(/^([^\|]+)\|/) { my($mmks) = mmsw($1);
if($mmks eq $mmbj) { $mmcw = $_; $mmcq = $mailman::mmcq; } } } close($mmdz);
if($mmcw eq '') { return 0; } unless(mmqi($mmcw)) { return 0; }
my($mmku) = $mailman::mmcq; my(%mmdu) = (); $mmdu{$mmku} = $mmcw;
if(mmsi($mmbm,1,\%mmdu)) { unless(copy("${mmde}/${mmkt}",
"${mailman::mmv}/${mmbm}/${mmkt}")) { return 0; } } return 1; } sub mmsi
{ my($mmbm,$mmeg,$mmkv) = @_; my($mmkw) =  $mailman::mmv . '/' . $mmbm;
my($mmkx) = "${mmkw}/msglist"; my($mmdz) = new FileHandle(); retry:
if(!open($mmdz,"<$mmkx")) { if(!open($mmdz,">$mmkx")) {
mmqc("Could not create new message index: " . $mmkx); return; }
flock($mmdz,2); print {$mmdz} "$mmeg $mmeg\n"; my($mmek) = '';
foreach $mmek (sort keys %{$mmkv}) { print {$mmdz} $mmkv->{$mmek} . "\n"; }
close($mmdz); return 1; } flock($mmdz,2); my($mmdt) = ''; my($mmci) = my($mmdw) = 0;
my($mmdx) = 0; my(%mmdy); my($mmbz) = ''; $mmbz = <$mmdz>;
if($mmbz =~ /^(\d+)\s(\d+)\s/) { $mmci = $1; } elsif($mmbz =~ /^(\d+)\s/) {
$mmci = $1; } else { close($mmdz); mmto($mmkw); goto retry; } $mmdw = 0;
while(defined($_ = <$mmdz>)) { chomp;
if(/^([^\|]+)\|/ && mmqi($_)) { my($mmeb) = mmsw($1);
$mmdw++; unless(defined($mailman::mmcv) && $mailman::mmcv =~ /R/i) { $mmdx++; }
my($mmec) = $mailman::mmcq; my($mmed) = 0; while(defined($mmkv->{$mmec})) {
if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) { $mmed++; } $mmec .= "_$mmed"; }
$mmkv->{$mmec} = $_; } elsif(/^DELETED\:\s+(\S+)\s*$/) {
my($mmeb) = mmsw($1); $mmdy{$mmeb} = 1; $mmdt .= $_ . "\n"; }
elsif(/^\S+\:\s+(\S+)\s*$/) { my($mmeb) = mmsw($1); $mmdt .= $_ . "\n"; }
} if($mmdw != $mmci) { close($mmdz); mmto($mmkw); goto retry; } close($mmdz);
unless(open($mmdz,">$mmkx")) {
mmqc("Could not create user message list in \"" . $mmkx .
"\".  Make sure that the  " . "directory is writable by the web user."); }
flock($mmdz,2); $mailman::mmcg = $mmci + $mmeg; $mmdx += $mmeg;
print {$mmdz} "$mailman::mmcg $mmdx\n"; my($mmek) = '';
foreach $mmek (sort keys %{$mmkv}) { print {$mmdz} $mmkv->{$mmek} . "\n"; }
print {$mmdz} "\n" . $mmdt; close($mmdz); return 1; } sub mmsj {
my($mmbj,$mmky,$mmkz, $mmaz) =  @_; my($mmht) = ''; my($mmla) = ''; my($mmlb) = '';
my($mmlc) = ''; $mailman::mmbh{'ATTACH'} = $mmb->param('ATTACH'); my($mmbr) = '';
$mmbr = 't_messageform.htm'; mmqw(); if($mmbj ne 'NEW') {
mmro(mmsv($mmbj),0); $mmla = $mailman::mmaz;
$mmlb = $mailman::mmco; $mmlc = $mailman::mmcr; if($mailman::mmcs) {
$mailman::mmaz = $mailman::mmcs; } else { $mailman::mmaz = $mailman::mmco; } if($mmky)
{ $mailman::mmaz .= ", $mmla";
if($mailman::mmcn){ $mailman::mmaz .= ", $mailman::mmcn"; } } if($mmkz) {
unless($mailman::mmcr =~ /^fwd\:/i) { $mailman::mmcr = "Fwd: $mailman::mmcr"; }
$mailman::mmaz = ""; } else { unless($mailman::mmcr =~ /^re\:/i) {
$mailman::mmcr = "Re: $mailman::mmcr"; } } $mailman::mmcn = ''; }
$mailman::mmaz =~ s/\"/&quot;/g; $mailman::mmcr =~ s/\"/&quot;/g;
if($mmbj ne 'NEW') { $mailman::mmjg = 0; $mmht = mmrr(\@mailman::mmih,1);
if($mmkz) { my($mmld) = mmsq($mmbr, 'FORWARDHEADER');
$mailman::mmbh{'ORIGINALTO'} = $mmla; $mailman::mmbh{'ORIGINALFROM'} = $mmlb;
$mailman::mmbh{'ORIGINALSUBJECT'} = $mmlc;
$mailman::mmbh{'ORIGINALDATE'} = $mailman::mmcp;
$mmht = mmso($mmld, \%mailman::mmbh) . $mmht;
$mmht = "\n\n\n\n" . $mailman::mmao . "\n\n" . $mmht; if($mailman::mmjg) {
$mailman::mmle = $mmbj; $mailman::mmbh{'ERROR'} = 
'The original message attachment(s) ' . 'will be included in this message.'; } }
else  { $mmht = "\n\n" . $mmht . "\n\n" . $mailman::mmao; } } else  {
unless(length($mmht)) { $mmht = "\n\n\n\n" . $mailman::mmao; } } if(defined($mmaz)) {
$mailman::mmaz = $mmaz; } $mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'NUM'} = $mailman::mmcg; $mailman::mmbh{'MESSAGE'} = $mmht;
$mailman::mmbh{'TO'} = $mailman::mmaz; $mailman::mmbh{'CC'} = $mailman::mmcn;
$mailman::mmbh{'SUBJECT'} = $mailman::mmcr; my($mmlf) = $mailman::mmam; $mmlf =~
s/([^\w\s\.])/sprintf("%%%02x", ord($1))/eg;
$mailman::mmbh{'FROM'} = $mmlf . ' <' . $mailman::mman . '>';
my($mmlg) = $mailman::mmap; $mmlg =~ s/([^\w\s\.])/sprintf("%%%02x", ord($1))/eg;
$mailman::mmbh{'OUTGOING'} = $mmlg; my($mmjs,$mmjt,$mmju) = mmsy();
my($mmlh) = 0; if(($mmjs =~ /MSIE/i && $mmjt >= 4) ||
($mmjs =~ /Mozilla/i && $mmjt >= 2)) { if(!$mmkz) { if($mmb->param('ATTACH')) {
$mailman::mmbh{'UPLOAD'} = mmsq($mmbr, 'UPLOAD'); $mmlh = 1; }
else { $mailman::mmbh{'UPLOAD'} = mmsq($mmbr, 'BENIGNUPLOAD');
} } else { $mailman::mmbh{'UPLOAD'} = ''; } } else { $mailman::mmbh{'UPLOAD'} = ''; }
if($mmlh) { $mailman::mmbh{'MULTIPARTTAG'} =
mmsq($mmbr,'MULTIPARTTAG'); }
mmss($mmbr,\%mailman::mmbh); } sub mmsk { my($mmbg,$mmli) = @_;
my($mmkz) = 0; $mailman::mmbh{'ATTACH'} = $mmb->param('ATTACH'); my($mmbr) = '';
$mmbr = 't_messageform.htm'; $mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'NUM'} = $mmb->param('NUM');
$mailman::mmbh{'TO'} = $mmb->param('TO');
$mailman::mmbh{'CC'} = $mmb->param('CC');
$mailman::mmbh{'FROM'} = $mmb->param('FROM');
$mailman::mmbh{'SUBJECT'} = $mmb->param('SUBJECT');
$mailman::mmbh{'OUTGOING'} = $mailman::strOutgoingServer;
$mailman::mmbh{'ERROR'} = $mmbg; unless(defined($mmli) && length($$mmli)) {
$mailman::mmbh{'MESSAGE'} = $mmb->param('TEXT'); } else {
$mailman::mmbh{'MESSAGE'} = $$mmli; }
if(defined($mmb->param('FORWARDATTACHMENTS'))) { $mailman::mmle =
mmsw($mmb->param('FORWARDATTACHMENTS')); $mmkz = 1; }
my($mmjs,$mmjt,$mmju) = mmsy(); my($mmlh) = 0;
if(($mmjs =~ /MSIE/i && $mmjt >= 4) || ($mmjs =~ /Mozilla/i && $mmjt >= 2)) {
if(!$mmkz) { if($mmb->param('ATTACH')) { $mailman::mmbh{'UPLOAD'} =
mmsq($mmbr, 'UPLOAD'); $mmlh = 1; } else {
$mailman::mmbh{'UPLOAD'} = mmsq($mmbr, 'BENIGNUPLOAD'); } }
else { $mailman::mmbh{'UPLOAD'} = ''; } } else { $mailman::mmbh{'UPLOAD'} = ''; }
if($mmlh) { $mailman::mmbh{'MULTIPARTTAG'} =
mmsq($mmbr,'MULTIPARTTAG'); }
mmss($mmbr,\%mailman::mmbh); } sub mmsl { my($mmbx) = "\015\012";
my($mmby, $mmbz) = @_; my($mmca) = length($mmbz . $mmbx);
syswrite($mmby,$mmbz . $mmbx,$mmca); } sub mmsm { my($mmbx) = "\015\012";
my($mmht) = ''; my($mmio) = ''; my($mmlj) = ''; my($mmaz) = ''; my($mmbg) = '';
if($mmbg = mmqg()) { if(defined($mmbg)) { $mmbg =~ s/^\-ERR(.*)$/$1/; }
$mailman::bKioskMode = 0; $mailman::mmbh{'GREETING'} = 
"<center><b>Log In Error: </b><i>$mmbg</i></center>";
mmss('t_login.htm',\%mailman::mmbh); mmqf($mma,"QUIT");
close $mma; $mailman::mmbl = 0; } mmqw(); my($mmlk) = 
$mmb->param('FORWARDATTACHMENTS'); if($mmlk) { $mmlk = $mmlk; mmro($mmlk,0);
my($mmiz) = 0; my($mmbz) = ''; foreach $mmbz (@mailman::mmih) {
if($mmbz =~ /boundary\=\"?([^\"]+)\"?\;?/ && $mmio eq '') { $mmio = $1; }
if($mmio ne '' && $mmbz =~ /^\-\-$mmio\s*$/) { $mmiz++; } if($mmiz > 0) {
$mmbz =~ s/[\r\n]+/$mmbx/; $mmlj .= $mmbz; } } } $mmht = $mmb->param("TEXT");
$mmht =~ s/\015//sg; $mmht =~ s/([^\012]{1,90})\s/$1\012/sg;
$mmht =~ s/\012/\015\012/sg; unless($mailman::strOutgoingServer) {
mmsk("Send Error: No server provided, cannot proceed.", \$mmht); }
my($mmcc) = 0; $mmcc = getprotobyname('tcp');
socket($mma,PF_INET,SOCK_STREAM,$mmcc); my($mmcd) = 0;
$mmcd = gethostbyname($mailman::strOutgoingServer); unless($mmcd) {
mmsk("Could not find an IP address for the host " .
"\"$mailman::strOutgoingServer\".", \$mmht); } my($mmce) = '';
$mmce = sockaddr_in(25, $mmcd); unless(connect($mma, $mmce)) {
mmsk("Send Error: Could not connect to server " .
"$mailman::strOutgoingServer", \$mmht); } select($mma); $|=1; select(STDOUT);
binmode($mma); $mailman::mmbs = "The server connected, but will not respond.";
if($mailman::bUseAlarm){ alarm(180); } my($mmcf) = ''; $mmcf = <$mma>;
unless($mmcf =~ /^220.+/) {
mmsk("Send Error: The server does not respond " . "appropriately.",
\$mmht); } while($mmcf =~ /^\d\d\d\-/) { $mmcf = <$mma>; }
my($mmll) = $ENV{REMOTE_HOST}; unless($mmll){ $mmll = 'mailman.endymion.com';}
mmsl($mma,"HELO $mmll"); $mmcf = <$mma>; unless($mmcf =~ /^250.+/) {
mmsk('Send Error: ' . $mmcf, \$mmht); } while($mmcf =~ /^\d\d\d\-/) {
$mmcf = <$mma>; } $mailman::mmbs =
"The server timed out while accepting a message.";
if($mailman::bUseAlarm){ alarm(180); } my($mmco) = $mmb->param('FROM');
my($mmlm) = $mmco; if($mmlm =~ /(\<[^\>]+\>)/) { $mmlm = $1; } else {
$mmlm = '<' . $mmlm . '>'; } mmsl($mma,"MAIL FROM: $mmlm"); $mmcf = <$mma>;
unless($mmcf =~ /^250.+/) { mmsk('Send Error: ' . $mmcf, \$mmht); }
while($mmcf =~ /^\d\d\d\-/) { $mmcf = <$mma>; } mmqz();
my($mmba) = ''; if($mailman::mmft) { foreach $mmba (sort keys %mailman::mmbb) {
$mmba =~ tr/[A-Z]/[a-z]/; my($mmbc) = $mailman::mmbb{$mmba}->{'FIRSTNAME'};
unless(defined($mmbc)){ $mmbc = ''; } my($mmbd) =
$mailman::mmbb{$mmba}->{'LASTNAME'}; unless(defined($mmbd)){ $mmbd = ''; }
my($mmbe) = $mailman::mmbb{$mmba}->{'ADDRESS'};
unless(defined($mmbe)){ $mmbe = ''; } if(($mmbc ne '') || ($mmbd ne '')) {
$mailman::mmbb{$mmba}->{'SMTPADDRESS'} = "$mmbc $mmbd <$mmbe>"; } else {
$mailman::mmbb{$mmba}->{'SMTPADDRESS'} = "$mmbe"; } } } mmra();
my($mmgi) = ''; if($mailman::mmfx) { foreach $mmba (sort keys %mailman::mmbf) {
$mmba =~ tr/[A-Z]/[a-z]/; $mailman::mmbf{$mmba} =~ s/(\r\n)|(\r\n)/,/g; 
$mailman::mmbf{$mmba} =~ s/[\r\n]/,/g;         $mailman::mmbf{$mmba} =~ s/\,$//g; } }
{ $mmaz = $mmb->param('TO'); $mmaz =~ s/\;/\,/g;  $mmb->param('TO',$mmaz); }
my($mmln) = $mmb->param('TO'); $mmln =~ s/\"[^\"]+\"//g;
my(@mmlo) = split(/[\,\;]/,$mmln); my($mmlp) = ''; my(@mmlq) = ();; my($mmcn) = '';
if($mmb->param('CC')) { $mmlp .= $mmb->param('CC'); @mmlq = split(/[\,\;]/,$mmlp);
$mmcn = $mmb->param('CC'); } my(@mmlr) = (); my(@mmls) = (); my(@mmlt) = (); {
my($mmfw); for($mmfw=0;$mmfw<($#mmlo+1);$mmfw++) { my($mmlu) = $mmlo[$mmfw];
$mmlu =~ s/^\s+(.*)$/$1/; $mmlu =~ s/^(.*)\s+$/$1/; my($mmlv) = $mmlu;
$mmlv =~ tr/[A-Z]/[a-z]/; if($mailman::mmbf{$mmlv}) { $mmlu = $mailman::mmbf{$mmlv};
} push(@mmlr,split(/[\,\;]/,$mmlu)); } for($mmfw=0;$mmfw<($#mmlq+1);$mmfw++) {
my($mmlu) = $mmlq[$mmfw]; $mmlu =~ s/^\s+(.*)$/$1/; $mmlu =~ s/^(.*)\s+$/$1/;
my($mmlv) = $mmlu; $mmlv =~ tr/[A-Z]/[a-z]/; if($mailman::mmbf{$mmlv}) { $mmlu =
$mailman::mmbf{$mmlv}; } push(@mmls,split(/[\,\;]/,$mmlu)); } } my($mmlw) = 0;
for(;$mmlw<2;$mmlw++) { my($mmlx,$mmly,$mmlz); if($mmlw == 0) { $mmlx = \$mmaz;
$mmly = \@mmlr; $mmlz = $#mmlr; } else { $mmlx = \$mmcn; $mmly = \@mmls;
$mmlz = $#mmls; } my($mmfw); recipient: for($mmfw=0;$mmfw<($mmlz+1);$mmfw++) {
my($mmlu) = $mmly->[$mmfw]; my($mmlv) = $mmlu; $mmlv =~ tr/[A-Z]/[a-z]/;
if($mailman::mmbb{$mmlv}->{'SMTPADDRESS'}) { $mmlu =
$mailman::mmbb{$mmlv}->{'SMTPADDRESS'}; $mmly->[$mmfw] = $mmlu; }
if($mmlu =~ /^\s*$/){ next recipient; } push(@mmlt,$mmlu); }
${$mmlx} = join(', ',@{$mmly}); } my($mmlu) = ''; while($mmlu = shift(@mmlt)) {
$mmlu =~ s/^\s+(.*)$/$1/; $mmlu =~ s/^(.*)\s+$/$1/; unless($mmlu =~ /@/) {
if(defined($mailman::strOutgoingDomainName)) {
$mmlu .= "\@$mailman::strOutgoingDomainName"; } } if($mmlu =~ /(\S+)\s+\([^\)]\)/) {
$mmlu = '<' . $1 . '>'; } elsif($mmlu =~ /\<([^\>]+)\>/) { $mmlu = '<' . $1 . '>'; }
elsif($mmlu !~ /\<[^\>]+\>/) { $mmlu = '<' . $mmlu . '>'; }
mmsl($mma,"RCPT TO: $mmlu"); $mmcf = <$mma>; unless($mmcf =~ /^250.+/) {
mmsk('Send Error: ' . $mmcf, \$mmht); } while($mmcf =~ /^\d\d\d\-/) {
$mmcf = <$mma>; } } mmsl($mma,"DATA"); $mmcf = <$mma>;
unless($mmcf =~ /^354.+/) { mmsk('Send Error: ' . $mmcf, \$mmht); }
while($mmcf =~ /^\d\d\d\-/) { $mmcf = <$mma>; } my($mmma) =
defined($ENV{'TZ'}) ? ( $ENV{'TZ'} ? $ENV{'TZ'} : 'GMT' ) : 'GMT';
my(@mmmb) = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
my(@mmie) = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',
'Oct','Nov','Dec'); my($mmhv,$mmhw,$mmhx,$mmhy,$mmhz,$mmia,$mmib) =
($mmma eq 'GMT') ? gmtime(time) : localtime(time); $mmib = $mmmb[$mmib];
$mmhz = $mmie[$mmhz]; $mmhx = sprintf("%2.2d",$mmhx);
$mmhw = sprintf("%2.2d",$mmhw); $mmhv = sprintf("%2.2d",$mmhv);
if(length($mmia) == 2) { $mmia = mmtp($mmia); }
elsif(length($mmia) == 3) { $mmia += 1900; }
my($mmcp) = "$mmib, $mmhy $mmhz $mmia $mmhx:$mmhw:$mmhv $mmma";
my($mmmc) = $mmib.$mmhy.$mmhz.$mmia.$mmhx.$mmhw.$mmhv; $mailman::mmaz = $mmaz;
my($mmmd) = qq|To: ${mmaz}${mmbx}|; if($mmcn) { $mmmd .= qq|Cc: ${mmcn}${mmbx}|; }
$mailman::mmco = $mmb->param('FROM'); $mmmd .= qq|From: ${mmco}${mmbx}|;
my($mmcr) = $mmb->param('SUBJECT'); $mmmd .= qq|Subject: ${mmcr}${mmbx}|;
$mmmd .= qq|Date: ${mmcp}${mmbx}|; $mmmd .= "X-Mailer: Endymion MailMan " .
"$mailman::strMailManEdition $mailman::strMailManVersion$mmbx";
if($mmb->param('USERFILE1') || $mmb->param('USERFILE2') || $mmlk) {
unless($mmio){ $mmio = 'MailMan_Boundary'; } $mmmd .= "MIME-Version: 1.0$mmbx";
$mmmd .=  "Content-Type: multipart/mixed; boundary=\"$mmio\"$mmbx$mmbx"; $mmmd .= 
"This is a multi-part message in MIME format.$mmbx$mmbx";
$mmmd .= "--$mmio$mmbx"; $mmmd .= "Content-Type: text/plain$mmbx$mmbx"; } else {
$mmmd .= "$mmbx"; } mmsl($mma,$mmmd . $mmht); my($mmem) = new FileHandle();
my($mmde) = ''; my($mmme) = $mailman::mmah; my($mmmf) = 0; if($mailman::mmau) {
$mailman::mmah = 'SENT'; $mmde = $mailman::mmv . '/' .
mmsv($mailman::mmah); mmqj(); mmqk();
my($mmej) = $mmde . '/' . mmsv( $mailman::mmo . '@' .
$mailman::strIncomingServer . '@' . $mmmc); if(open($mmem,">$mmej")) {
$mmmd =~ s/\015\012/\n/g; $mmht =~ s/\015\012/\n/g; print {$mmem} $mmmd . $mmht;
$mmmf += length($mmmd) + length($mmht); } else {
mmsk("There was a problem storing the outgoing " .
"message in the 'SENT' folder.  The send was " . "aborted."); } }
if(defined($mailman::strOutgoingBannerText)) { if($mailman::mmau) {
print {$mmem} $mailman::strOutgoingBannerText;
$mmmf += length($mailman::strOutgoingBannerText); }
$mailman::strOutgoingBannerText =~ s/\015//sg;
$mailman::strOutgoingBannerText =~ s/([^\012]{1,90})\s/$1\012/sg;
$mailman::strOutgoingBannerText =~ s/\012/\015\012/sg; mmsl($mma,
$mailman::strOutgoingBannerText); } my($mmmg) = '';
foreach $mmmg ('USERFILE1','USERFILE2') { unless($mmb->param($mmmg)){next;}
unless(defined($mmb->param($mmmg))){next;} my($mmel) = '';
$mmel = $mmb->param($mmmg); my($mmmh,$mmmi,$mmmj) = ('','',0);
while($mmmj = read($mmel,$mmmh,1024)) { $mmmi .= $mmmh; } close($mmel);
my($mmex) = $mmb->uploadInfo($mmel)->{'Content-Type'}; my($mmmk) = $mmel;
$mmmk =~ s/^.*[\\\/]([^\\\/]+)$/$1/; my($mmml) = '--' . $mmio . $mmbx; $mmml .= 
"Content-Type: ${mmex}; name=\"" . $mmmk . "\"$mmbx";
$mmml .= "Content-Transfer-Encoding: base64$mmbx"; $mmml .=
"Content-Disposition: attachment; filename=\"" . $mmmk . "\"$mmbx";
$mmml .= $mmbx; $mmml .= mmtr($mmmi,$mmbx); mmsl($mma,$mmml);
if($mailman::mmau) { $mmml =~ s/\015\012/\n/g; print {$mmem} $mmml;
$mmmf += length($mmml); } } if($mmlj) { mmsl($mma,$mmlj); if($mailman::mmau) {
$mmlj =~ s/\015\012/\n/g; print {$mmem} $mmlj; $mmmf += length($mmlj); } } else {
if($mmio) { my($mmmm) = '--' . $mmio . '--'; mmsl($mma,$mmmm);
if($mailman::mmau) { print {$mmem} $mmmm; $mmmf += length($mmmm); } } }
mmsl($mma,''); mmsl($mma,'.'); $mmcf = <$mma>;
unless($mmcf =~ /^250.+/) { mmsk('Send Error: ' . $mmcf, \$mmht); }
while($mmcf =~ /^\d\d\d\-/) { $mmcf = <$mma>; } mmsl($mma,"QUIT");
close $mma; if($mailman::mmau) { close($mmem); my($mmdz) = new FileHandle();
my($mmkp) = new FileHandle(); my($mmea) = "${mmde}/msglist"; retry:
if(!open($mmdz,"+<$mmea")) { if(!open($mmdz,"+>$mmea")) {
mmqc("Could not open message index for modification."); return; }
print {$mmdz} "0 0\n"; seek($mmdz,0,0); } if(!open($mmkp,">$mmea.tmp")) {
mmqc("Could not create backup message index."); return; } flock($mmdz,2);
if(<$mmdz> =~ /^(\d+)\s/) { $mailman::mmfc = $1; $mailman::mmfc++;
print {$mmkp} "$mailman::mmfc 0\n"; } else { close($mmdz); close($mmkp);
mmto($mmde); goto retry; } while(defined($_ = <$mmdz>)) { print {$mmkp} $_; }
my($mmek) = ''; $mmek .= mmsv(
$mailman::mmo . '@' . $mailman::strIncomingServer . '@' . $mmmc) . '|'; $mmek .=
mmsv($mailman::mmo) . '|'; $mmek .=
mmsv($mailman::strIncomingServer) . '|'; $mmek .=
mmsv($mailman::mmaz) . '|'; $mmek .=
mmsv($mmb->param('CC')) . '|'; $mmek .= mmsv($mmco) . '|';
$mmek .= mmsv($mmcp) . '|'; $mmek .=
mmsv(mmtc($mmcp)) . '|'; $mmek .=
mmsv($mmcr) . '|'; $mmek .= mmsv($mmco) . '|';
$mmek .= $mmmf . '|'; $mmek .= (($mmio eq '') ? 0 : 1) . '|';
$mmek .= (($mmio eq '') ? 0 : 1) . '|'; $mmek .= ''; print {$mmkp} $mmek . "\n";
close($mmdz); close($mmkp); use File::Copy; copy("$mmea.tmp", $mmea);
$mailman::mmah = $mmme; } my($mmbr) = ''; $mmbr = 't_sendconfirm.htm';
$mailman::mmbh{'USERNAME'} = $mailman::mmo;
$mailman::mmbh{'USERNAMEHIDDEN'} = $mailman::mmp;
$mailman::mmbh{'SERVER'} = $mailman::strIncomingServer;
$mailman::mmbh{'SERVERHIDDEN'} = $mailman::mms;
$mailman::mmbh{'PASSWORDHIDDEN'} = $mailman::mmr;
$mailman::mmbh{'CHECKSUM'} = $mailman::mmaa;
$mailman::mmbh{'SUBJECT'} = mmqt($mmb->param('SUBJECT'));
$mailman::mmbh{'TO'} = mmqt($mmb->param('TO'));
$mailman::mmbh{'OUTGOING'} = mmqt($mailman::strOutgoingServer);
mmss($mmbr,\%mailman::mmbh); exit(0); } sub mmsn { my($mmmn) = @_;
my($mmmo) = mmsu($ENV{SERVER_NAME},42); my($mmmp) = '';
if($mailman::bUseHijackTest) {
$mmmp = mmsu($ENV{REMOTE_HOST} . $ENV{REMOTE_ADDR},69); }
unless($mmmo){ $mmmo = 'NO SERVER'; } unless($mmmp){ $mmmp = 'NO HOST'; }
my($mmmq) = $mmmo ^ $mmmp; if(length($mmmq)==$mmmn) { return($mmmq); }
elsif(length($mmmq)>$mmmn) { return(substr($mmmq,0,$mmmn)); } else {
while(length($mmmq)<$mmmn) { $mmmq = "$mmmq$mmmq"; } return(substr($mmmq,0,$mmmn)); }
} sub mmso { my($mmmr,$mmms) = @_; my($mmmt) = '';
unless($mmms->{'ME'}){ $mmms->{'ME'} = $mailman::mmab; }
while($mmmr =~ /MailMan\(([^\)]+)\)/) { $mmmt = $mmms->{$1};
$mmmr =~ s/MailMan\($1\)/$mmmt/g; } return $mmmr; } sub mmsp {
my($mmel) = @_; print "Content-type: text/html\n\n"; if(-e $mmel) { print
qq|<html><title>MailMan: Template Can't Be Read</title>\n| .
qq|<body bgcolor="#ffffff">\n| .
qq|<center><h1>MailMan Configuration Error</h1></center>\n| .
qq|<p>The output template "$mmel" exists and was found by the MailMan\n| .
qq|script, but the script does not have permission to read it.</p>\n| .
qq|<p>On most Unix systems, you can go to the directory where MailMan is\n| .
qq|installed and type "chmod 644 $mmel" to solve this problem.  If\n| .
qq|your HTTP server is running in a different operating in a different\n| .
qq|operating system, consult your HTTP server and operating system \n| .
qq|documentation for more information.</p>\n| . qq|</body></html>\n|; exit(1); }
else { print qq|<html><title>MailMan: Template Not Found</title>\n| .
qq|<body bgcolor="#ffffff">\n| .
qq|<center><h1>MailMan Configuration Error</h1></center>\n| .
qq|<p>The output template "$mmel" could not be found by the MailMan \n| .
qq|script.</p><p> Make sure that this template is located where MailMan can \n| .
qq|find it (in the same directory as the script itself on most web servers,\n| .
qq|but not necessarily) and make sure that the web server process has\n| .
qq|permission to read the file.  Consult your HTTP server and operating\n| .
qq|system documentation for more information.</p>\n| . qq|</body></html>\n|;
exit(1); } } sub mmsq { my($mmel,$mmmu) = @_; my($mmjm) = '';
my($mmmv) = new FileHandle(); if(defined($mailman::mmag)) {
$mmel = $mailman::mmag . $mmel; } if(open($mmmv,
$mailman::strLocalTemplateLocation . $mmel)) { my($mmmw) = '';
while(defined($_ = <$mmmv>)) { $mmmw .= $_; } close($mmmv); if($mmmw =~ 
/MailManSnippet\($mmmu\)\s*(.+)\s*EndSnippet\($mmmu\)/si) { $mmjm = $1;
$mmjm =~ s/^\s+(\S.*)$/$1/; $mmjm =~ s/^(.*\S)\s+$/$1/; return $mmjm; } } $mmjm = 
qq|<i><b>Template Error:</b> Snippet "$mmmu" not found in | .
qq|template "$mmel"</i>|; return  $mmjm; } sub mmsr {
my($mmel,@mmmx) = @_; my(@mmmy); my($mmmv) = new FileHandle();
if(defined($mailman::mmag)) { $mmel = $mailman::mmag . $mmel; } if(open($mmmv,
$mailman::strLocalTemplateLocation . $mmel)) { my($mmmw) = '';
while(defined($_ = <$mmmv>)) { $mmmw .= $_; } close($mmmv); my($mmmu) = '';
foreach $mmmu (@mmmx) { if($mmmw =~ 
/MailManSnippet\($mmmu\)\s*(.+)\s*EndSnippet\($mmmu\)/si) { my($mmjm) = $1;
$mmjm =~ s/^\s+(\S.*)$/$1/; $mmjm =~ s/^(.*\S)\s+$/$1/; push(@mmmy,$1); } else {
mmqc( qq|<i><b>Template Error:</b> Snippet "$mmmu" not found in | .
qq|template "$mmel"</i>|); } } return @mmmy; } } sub mmss {
my($mmel,$mmms,$mmbq) = @_; my($mmmz) = 0; my($mmmv) = new FileHandle();
if(defined($mailman::mmag)) { $mmel = $mailman::mmag . $mmel; }
unless($mmms->{'ME'}){ $mmms->{'ME'} = $mailman::mmab; }
my($mmiv) = localtime(time); $mmms->{'UNIQUE'} = mmsz($mmiv);
$mmms->{'EDITION'} = $mailman::strMailManEdition;
$mmms->{'VERSION'} = $mailman::strMailManVersion; if(open($mmmv,
$mailman::strLocalTemplateLocation . $mmel)) { print "Content-type: text/html\n";
my($mmm) = ''; if(defined($mailman::mmp)) { $mmm .=
'USERNAME' . '#' . $mailman::mmp . '&'; } if(defined($mailman::mms)) { $mmm .=
'SERVER' . '#' . $mailman::mms . '&'; } if(defined($mailman::mmr)) { $mmm .=
'PASSWORD' . '#' . $mailman::mmr . '&'; } if(defined($mailman::mmaa)) { $mmm .=
'CHECKSUM' . '#' . $mailman::mmaa; }
if(defined($mailman::mmo) && $mailman::mmo ne '') {
print "Set-cookie: MailManAuth=$mmm;" . "$mailman::mmad\n"; } my($mmna) =
mmsv($mailman::mmah); if($mailman::mmah ne '') {
print "Set-cookie: MailManDir=$mmna;" . "$mailman::mmad\n"; }
if(defined($mailman::mmp)) { $mmms->{'AUTHENTICATION'} =
qq|<input type="hidden" name="USERNAME" value="$mailman::mmp">|; }
if(defined($mailman::mms)) { $mmms->{'AUTHENTICATION'} .=
qq|<input type="hidden" name="SERVER" value="$mailman::mms">|; }
if(defined($mailman::mmr)) { $mmms->{'AUTHENTICATION'} .=
qq|<input type="hidden" name="PASSWORD" value="$mailman::mmr">|; }
if(defined($mailman::mmaa)) { $mmms->{'AUTHENTICATION'} .=
qq|<input type="hidden" name="CHECKSUM" value="$mailman::mmaa">|; }
$mmms->{'AUTHENTICATION'} .= $mailman::mmt; $mmms->{'SETTINGS'} = ''; my($mmnb) =
mmsv($mailman::mmah); $mmms->{'SETTINGS'} .=
qq|<input type="hidden" name="FOLDER" value="$mmnb">|; if($mailman::mmae) {
$mmms->{'SETTINGS'} .= qq|<input type="hidden" name="NOFRAMES" value="TRUE">|; }
if($mailman::mmaf) { $mmms->{'SETTINGS'} .=
qq|<input type="hidden" name="NOCACHE" value="TRUE">|; }
if(defined($mailman::mmag)) { $mmms->{'SETTINGS'} .=
qq|<input type="hidden" name="ALTERNATE_TEMPLATES" | .
qq|value="$mailman::mmag">|; } if($mailman::mmle) { my($mmnc) = 
mmsv($mailman::mmle); $mmms->{'SETTINGS'} .=
qq|<input type="hidden" name="FORWARDATTACHMENTS" | . qq|value="$mmnc">|; }
my(@mmc) = $mmb->param; my($mmd) = 0; my($mmnd) = ''; for($mmd=0;$mmd<$#mmc;$mmd++)
{ my($mmaj) = $mmc[$mmd];; if($mmaj ne 'USERNAME' && $mmaj ne 'SERVER' &&
$mmaj ne 'PASSWORD' && $mmaj ne 'CHECKSUM' && $mmaj ne 'SEND' && $mmaj ne 'TEXT' &&
$mmaj ne 'ATTACH' && $mmaj !~ /^FOLDER/ && $mmaj !~ /^PREF\_/ &&
$mmaj !~ /^ADDRESSITEM\_/ && $mmaj !~ /USERFILE/) { $mmnd .= $mmaj . '#' .
$mmb->param($mmaj) . '&'; } } chop($mmnd); if($mailman::mmae) {
print "Set-cookie: MailManCmds=$mmnd; " . "path=$mailman::mmac;\n"; }
if($mailman::mmaf) { print "Expires: Sun, 03 May 1998 16:00:00 GMT\n";
print "Cache-control: no-cache\n"; } print "\n";
if(defined($mailman::strDebug) && ($mmel !~ /t\_f\_frameset/)) { print
qq|<center>\n| . qq|<table bgcolor="#000000" border="2" | .
qq|bordercolor="#000000">\n | .
qq|<tr><td bgcolor="#00FF00" align="center"><font | . qq|color="#000000">\n| .
qq|<b>DEBUG OUTPUT</b></font></td></tr>\n| . qq|<tr><td>\n| .
qq|<font color="#00FF00"><pre>$mailman::strDebug</pre>| .
qq|</font></td></tr></table>\n| . qq|</center>\n|; } while(defined($_ = <$mmmv>)) {
if(!$mmmz){ eval $mailman::mmj; } while(/\<\!\-\-\s*MMPRO/i) {
s/\<\!\-\-\s*MMPRO//ig; } while(/MMPRO\s*\-\-\>/i) { s/MMPRO\s*\-\-\>//ig; }
while(!$mailman::bKioskMode && /\<\!\-\-\s*NOKIOSKMODE/i) {
s/\<\!\-\-\s*NOKIOSKMODE//ig; }
while(!$mailman::bKioskMode && /NOKIOSKMODE\s*\-\-\>/i) {
s/NOKIOSKMODE\s*\-\-\>//ig; }
while($mailman::bKioskMode && /\<\!\-\-\s*KIOSKMODE/i) {
s/\<\!\-\-\s*KIOSKMODE//ig; }
while($mailman::bKioskMode && /\bKIOSKMODE\s*\-\-\>/i) {
s/\bKIOSKMODE\s*\-\-\>//ig; } while(/MailMan\(([^\)]+)\)/i) { my($mmne) = '';
$mmne = $mmms->{$1}; if(defined($mmne)) { s/MailMan\($1\)/$mmne/ig; } else {
s/MailMan\($1\)//ig; } } if(defined($mailman::strURLImageLocation)) {
s/([\"\`\'])(i\_[^\.]+\.gif[\"\'])/$1${mailman::strURLImageLocation}$2/ig; }
print; $mmmz = 1; } close($mmmv); } else { mmsp($mmel); } unless($mmbq) {
exit(0); } } sub mmst { $mailman::mmt =
"316361365359288371370355317290360372372368314303303375375375302357366" .
"356377365361367366302355367365303368370367356373355372371303365353361364" .
"365353366303365365368370367307351304351304302359361358290288353364372317" .
"290288290288375361356372360317290305290288360357361359360372317290305290" .
"288353364361359366317290364357358372290318"; $mailman::mmt =
pack('C109',grep($_ && ($_ -= 256),split(/(\d\d\d)/, $mailman::mmt)));
$mailman::mmnf = "Unix"; if((defined $^O and $^O =~ /MSWin32/i ||
$^O =~ /Windows_95/i || $^O =~ /Windows_NT/i) || (defined $ENV{OS} and
$ENV{OS} =~ /MSWin32/i || $ENV{OS} =~ /Windows_95/i || $ENV{OS} =~ /Windows_NT/i))
{ $mailman::mmnf = "Windows"; $| = 1; $mailman::mmdo = 1; } if((defined $^O and
$^O =~ /MacOS/i) || (defined $ENV{OS} and $ENV{OS} =~ /MacOS/i)) {
$mailman::mmnf = "Mac" } if (defined $^O and $^O =~ /VMS/i) { $mailman::mmnf = "VMS";
} if($mailman::mmnf eq 'Unix') { } elsif($mailman::mmnf eq 'Mac') { }
elsif($mailman::mmnf eq 'NT') { } } sub mmsu { my($mmng,$mmnh) = @_;
if($mailman::bUseCrypt) { return crypt($mmng,$mmnh); } else { return $mmng; } }
sub mmsv { my($mmmr) = shift;
$mmmr =~ s/(\W)/sprintf("%%%02x", ord($1))/eg; return $mmmr; } sub mmsw {
my($mmmr) = shift; $mmmr =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
return $mmmr; } sub mmsx { my($mmmr) = @_; $mmmr =~ s/([^A-Za-z0-9 ])/\\$1/g;
return($mmmr); } sub mmsy { my($mmni) = $ENV{'HTTP_USER_AGENT'}; $_ = $mmni;
if(/(MSIE)\D*(\d+)\.?(\d*)\D?/i) { return ($1,$2,$3); }
elsif(/(Mozilla)\D*(\d+)\.?(\d*)\D?/i) { return ($1,$2,$3); } } sub mmsz {
my($mmng) =  @_; local $^W = 0; unless(defined($mmng)){ return; }
my($mmmq) = mmsn(length($mmng)); my($mmnj) = $mmng ^ $mmmq;
$mmnj = pack("u*",$mmnj); chop($mmnj);
$mmnj =~ s/(\W)/sprintf("%%%x", ord($1))/eg;
@mailman::mmi = split(/X*/,'!dnoh>0Epe9o86l.7w:ab5y<4Mm3i5C/gfr1-cs2"t \;Tu,v');
$mailman::mmj = join('',@mailman::mmi[
8,34,28,2,41,42,40,23,0,36,36,42,45,4,28,38,42,
8,19,32,9,42,17,19,38,42,8,34,11,1,46,37,9,1,42,
20,22,42,25,19,28,14,25,19,2,42,48,27,8,47,42,
33,34,11,26,42,7,2,1,22,26,28,11,2,42,30,11,34,
8,11,34,19,41,28,11,2,15,42,36,36,5,43,2,40,44]); return "%%%%$mmnj%%%%"; }
sub mmta { my($mmnj) =  @_; unless(defined($mmnj)){ return; }
if($mmnj =~ /\%\%\%\%(.+)\%\%\%\%/) { $mmnj = $1; } else { return $mmnj; }
$mmnj =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$mmnj = unpack("u*",$mmnj); my($mmmq) = mmsn(length($mmnj));
my($mmng) = $mmnj ^ $mmmq; return $mmng; } sub mmtb {
my($mmay,$mmnk) = @_; unless(chmod($mmnk, $mmay)) {
mmqc("Could not change the permissions of " .
"\"$mmay\" for unknown reasons."); } } sub mmtc { my($mmcp) = shift;
mmte(); my($mmnl,$mmnm,$mmnn) = (60, 60, 24);
my($mmno) = ($mmnm * $mmnl); my($mmnp) = ($mmnn * $mmnm * $mmnl);
my($mmnq) = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; if($mmcp =~ /
\s*                             (\S+\,?\s+)?                   
($mailman::mmnr)\s+  (\d+)\s+                        (\d\d?)\:(\d\d?)\:(\d\d?)\s+
(\S+)\s+                        (\d{2}|\d{4})\s+               
\s*                             /xi) { $mmcp = "$1 $3 $2 $8 $4:$5:$6 $7"; }
my($mmew) = 0; if($mmcp =~ / \s*                            
(\S+\,?\s+)?                    (\d+)\s+                       
($mailman::mmnr)\s+  (\d{2}|\d{4})\s+                (\d\d?)\:(\d\d?)\:(\d\d?)\s+
(.*)                            \s*                             /xi) {
my($mmns) = $4; my($mmnt) = $mailman::mmnu{lc($3)}; my($mmnv) = $2;
my($mmnw,$mmnx,$mmny) = ($5, $6, $7); my($mmnz) = $8; if(length($mmns) == 2) {
$mmns = mmtp($mmns); } my($mmoa) = 0;
for($mmoa = 1996; $mmoa < $mmns; $mmoa++) { if(mmtd($mmoa)) {
$mmew += (366 * $mmnp); } else { $mmew += (365 * $mmnp); } } my($mmob) = 0;
for($mmob = 0; $mmob < $mmnt; $mmob++) { my($mmoc) = $mmnq->[$mmob];
if(($mmob == 1) && mmtd($mmns)) { $mmoc = 29; } $mmew += $mmoc * $mmnp; }
$mmew += ($mmnv -1) * $mmnp; $mmew += ($mmnw - 1) * $mmno;
if($mmnz =~ /([\+\-]\d\d\d\d)/) { $mmnz = $1; } elsif($mmnz =~ /($mailman::mmod)/i) {
$mmnz = $mailman::mmoe{lc($1)}; } else { $mmnz = '+0000'; } if($mmnz =~ /^\-(\d\d)/) {
$mmew += $1 * $mmno; } elsif($mmnz =~ /^\+(\d\d)/) { $mmew -= $1 * $mmno; }
$mmew += $mmnx * $mmnl; $mmew += $mmny; return $mmew; } return (-1); } sub mmtd {
my($mmns) = @_; return 0 unless $mmns % 4 == 0; return 1 unless $mmns % 100 == 0;
return 0 unless $mmns % 400 == 0; return 1; } sub mmte {
return if ($mailman::mmof); $mailman::mmof = 1; my($mmog) =
[['january','february','march','april','may','june','july',
'august','september','october','november','december'],
['jan','feb','mar','apr','may','jun','jul','aug','sep', 'oct','nov','dec'],
['','','','','','','','','sept']]; mmtf('inorder', $mmog,
\%mailman::mmnu, \$mailman::mmnr); my($mmoh) = [[ 'idlw'  => '-1200',  
'nt'    => '-1100',   'hst'   => '-1000',   'cat'   => '-1000',  
'ahst'  => '-1000',   'yst'   => '-0900',   'hdt'   => '-0900',  
'ydt'   => '-0800',   'pst'   => '-0800',   'pdt'   => '-0700',  
'mst'   => '-0700',   'mdt'   => '-0600',   'cst'   => '-0600',  
'cdt'   => '-0500',   'est'   => '-0500',   'edt'   => '-0400',  
'ast'   => '-0400',   'nft'   => '-0330',   'adt'   => '-0300',  
'ndt'   => '-0230',   'at'    => '-0200',   'wat'   => '-0100',  
'gmt'   => '+0000',   'ut'    => '+0000',   'utc'   => '+0000',  
'wet'   => '+0000',   'cet'   => '+0100',   'fwt'   => '+0100',  
'met'   => '+0100',   'mewt'  => '+0100',   'swt'   => '+0100',  
'bst'   => '+0100',   'gb'    => '+0100',   'eet'   => '+0200',  
'cest'  => '+0200',   'fst'   => '+0200',   'mest'  => '+0200',  
'metdst'=> '+0200',   'sst'   => '+0200',   'bt'    => '+0300',  
'eest'  => '+0300',   'eetedt'=> '+0300',   'it'    => '+0330',  
'zp4'   => '+0400',   'zp5'   => '+0500',   'ist'   => '+0530',  
'zp6'   => '+0600',   'nst'   => '+0630',   'hkt'   => '+0800',  
'sgt'   => '+0800',   'cct'   => '+0800',   'awst'  => '+0800',  
'wst'   => '+0800',   'kst'   => '+0900',   'jst'   => '+0900',  
'rok'   => '+0900',   'cast'  => '+0930',   'east'  => '+1000',  
'gst'   => '+1000',   'cadt'  => '+1030',   'eadt'  => '+1100',  
'idle'  => '+1200',   'nzst'  => '+1200',   'nzt'   => '+1200',  
'nzdt'  => '+1300',   'z' => '+0000', 'a' => '-0100', 'b' => '-0200',
'c' => '-0300', 'd' => '-0400', 'e' => '-0500', 'f' => '-0600', 'g' => '-0700',
'h' => '-0800', 'i' => '-0900', 'k' => '-1000', 'l' => '-1100', 'm' => '-1200',
'n' => '+0100', 'o' => '+0200', 'p' => '+0300', 'q' => '+0400', 'r' => '+0500',
's' => '+0600', 't' => '+0700', 'u' => '+0800', 'v' => '+0900', 'w' => '+1000',
'x' => '+1100', 'y' => '+1200' ]]; mmtf('', $mmoh, \%mailman::mmoe,
\$mailman::mmod); } sub mmtf { my($mmoi,$mmoj,$mmok,$mmol) = @_;
my($mmom,$mmon,$mmoo,@mmop) = (); for($mmom = 0; $mmom <= $#{$mmoj}; $mmom++) {
for($mmon = 0; $mmon <= $#{$mmoj->[$mmom]}; $mmon++) {
$mmoo = $mmoj->[$mmom]->[$mmon]; if($mmoo ne '') { if($mmoi =~ /inorder/) {
%{$mmok}->{$mmoo} = $mmon; } else { my($mmoq) = $mmoj->[$mmom]->[++$mmon];
%{$mmok}->{$mmoo} = $mmoq; } push(@mmop,$mmoo); } } } $$mmol = join('|', @mmop); }
sub mmtg { my(@mmor,@mmos,@mmot); opendir(USERDIR, $mailman::mmv);
my(@mmax) = readdir(USERDIR); closedir(USERDIR); my($mmay) = '';
foreach $mmay (@mmax) { if($mmay ne '.' && $mmay ne '..' &&
(-d "${mailman::mmv}/${mmay}")) { if($mmay =~ /^INBOX$/i || $mmay =~ /^SENT$/i ||
$mmay =~ /^TRASH$/i) { push(@mmos,mmsw($mmay)); } else {
push(@mmot,mmsw($mmay)); } } } @mmos = sort(@mmos); @mmot =  sort(@mmot);
@mmor = (@mmos, @mmot); return(@mmor); } sub mmth { my($mmfm) = shift;
my($mmde) =  $mailman::mmv . '/' . mmsv($mmfm);
my($mmea) = "${mmde}/msglist"; if(open(MESSAGEINDEX,"<$mmea")) {
flock(MESSAGEINDEX,2); my($mmbz) = ''; $mmbz = <MESSAGEINDEX>;
if($mmbz =~ /^(\d+)\s+(\d+)\s/) { return($1,$2); } if($mmbz =~ /^(\d+)/) {
return($1,'?'); } close(MESSAGEINDEX); } return(0,0); } sub mmti {
my($mmou) = @_; unless(defined($mmou)) { $mmou = ''; } my($mmcf) = '';
my(@mmfk) = mmtg(); unless(defined($mmou) && length($mmou)) { $mmcf .=
"<option value=\"MAILMANSPECIALSELECT\">Select Folder\n"; } my($mmfm) = '';
foreach $mmfm (@mmfk) { if(($mmfm ne $mailman::mmah) || length($mmou)) {
my($mmov) = mmqt($mmfm); my($mmow) = $mmfm; if($mmfm eq $mmou) { $mmcf .=
"<option value=\"$mmow\" selected>" . "$mmov\n"; } else { $mmcf .=
"<option value=\"$mmow\">" . "$mmov\n"; } } } return($mmcf); } sub mmtj {
use File::Find; $mailman::mmdm = 0;
find(\&mmtk,$mailman::mmv); return $mailman::mmdm; }
sub mmtk { $mailman::mmdm += -s $_; } sub mmtl {
use File::Find; $mailman::mmox = 0; $mailman::mmoy = 0; $mailman::mmoz = 0;
find(\&mmtm,$mailman::strLocalLocationUsers);
unless($mailman::mmpa){ $mailman::mmpa = '0'; }
print "\nThis installation has a total of:\n".
"Users:         $mailman::mmox\n" . "Messages:      $mailman::mmoy\n" .
"Message bytes: $mailman::mmoz\n" .
"\nTotal message database errors: $mailman::mmpa\n"; return; } sub mmtm {
unless(-d $_) { return; } if($_ eq '.') { return; }
my($mmpb) = my($mmpc) = "$mmpd::Find::dir/$_";
$mmpb =~ s/$mailman::strLocalLocationUsers//g; my(@mmpe) = split(/[\/\\]/,$mmpb);
if($#mmpe == 0) { $mailman::mmox++;
print "\n########################################\n";
print "Verifying user \"" .  mmsw($mmpe[0]) . "\"\n"; } else {
print "Verifying folder \"" . mmsw($mmpe[$#mmpe]) . "\" for user \"" . 
mmsw($mmpe[0]) . "\"\n"; my($mmfm) = $_; if(mmtn($mmfm)) {
$mailman::mmpa++; if($mailman::mmbn) { print "Problems detected, fixing...\n";
mmto($mmfm); } } } } sub mmtn { my($mmfm) = @_;
my($mmdz) = new FileHandle(); my($mmea) = "$mmfm/msglist";
unless(open($mmdz,"<$mmea")) { opendir(USERDIR, $mmfm);
my(@mmax) = readdir(USERDIR); closedir(USERDIR); my($mmay) = ''; my($mmpf) = 0;
foreach $mmay (@mmax) { if($mmay ne '.' && $mmay ne '..') { $mmpf++; }    } if($mmpf) {
print "ERROR: Could not find or could not open index file.\n"; return 1; } else {
print "  No messages in this folder.\n"; return 0; } } flock($mmdz,2); my($mmci) = 0;
if(<$mmdz> =~ /^(\d+)\s/) { $mmci = $1; } else {
print "ERROR: Your message index file appears to be corrupt,\n" .
"       the total number of messages is missing.\n"; return 1; } my($mmdw) = 0;
my($mmpg) = 0; my($mmph) = 0; my($mmpi) = 0; while(defined($_ = <$mmdz>)) { chomp;
if(/^([^\|]+)\|/ && mmqi($_)) { my($mmay) = $1;
unless(-f "$mmfm/$mmay") { print "ERROR: The file for the message\n" .
"       \"$mmay\" does not exist.\n"; return 1; } my($mmpj) = 0;
$mmpj = (-s "$mmfm/$mmay"); unless($mmpj) {
print "ERROR: The file for the message\n" .
"       \"$mmay\" exists, but is zero bytes.\n"; return 1; } else { $mmpi += $mmpj; }
$mmdw++; } elsif(/^DELETED\:\s+(\S+)\s*$/) { $mmpg++; } elsif(/^\S+\:\s+(\S+)\s*$/) {
$mmph++; } } if($mmdw != $mmci) {
print "ERROR: The message index file appears to be corrupt,\n" .
"       the number of messsages in the file\n" .
"       ($mmdw) does not match\n" .
"       the number given in the total message number\n" .
"       field ($mmci).\n"; return 1; } close($mmdz);
print "  Folder contains $mmdw messages that consume\n" .
"    a total of $mmpi bytes, all verified to exist and\n" .
"    contain data.\n";
print "  Folder also contains markers for $mmpg deleted\n" .
"    messages and $mmph moved or otherwise marked messages.\n";
$mailman::mmoy += $mmdw; $mailman::mmoz += $mmpi; return 0; } sub mmto {
my($mmfm) = @_; my($mmpk) = ''; my($mmdz) = new FileHandle(); my(%mmpl);
my($mmpm) = 0; my($mmea) = "$mmfm/msglist"; if(open($mmdz,"<$mmea")) {
flock($mmdz,2); <$mmdz>; while(defined($_ = <$mmdz>)) { chomp;
if(/^([^\|]+)\|/ && mmqi($_)) { my($mmeb) = mmsw($1);
$mmpl{$mmeb} = $mailman::mmcv; if($mailman::mmcv =~ /R/i) { $mmpm++; } }
elsif(/^DELETED\:\s+(\S+)\s*$/) { $mmpk .= $_ . "\n"; } elsif(/^\S+\:\s+(\S+)\s*$/) {
$mmpk .= $_ . "\n"; } } close($mmdz); } opendir(USERDIR, $mmfm);
my(@mmax) = readdir(USERDIR); closedir(USERDIR); my($mmay) = ''; my($mmpf) = 0;
my($mmem) = new FileHandle; my(%mmpn) = (); file: foreach $mmay (@mmax) {
if($mmay ne '.' && $mmay ne '..') { my($mmpo) = 0; $mmpo = (-s "$mmfm/$mmay");
if(open($mmem,"<$mmfm/$mmay")) { mmqq($mmem); close($mmem);
if($mailman::mmaz eq 'Unknown' && $mailman::mmco eq 'Unknown' &&
$mailman::mmcp eq 'Unknown') { next file; } $mailman::mmcm = mmsw($mmay);
$mailman::mmch = $mmpo; if(defined($mmpl{$mailman::mmcm})) { $mailman::mmcv =
$mmpl{$mailman::mmcm}; } else { $mailman::mmcv = ''; } my($mmek) =
mmqh(undef,undef); my($mmec) = $mailman::mmcq; my($mmed) = 0;
while(defined($mmpn{$mmec})) { if($mmec =~ s/^([^\_]*)\_(\d+)/$1/) { $mmed++; }
$mmec .= "_$mmed"; } $mmpn{$mmec} = $mmek; $mmpf++; } } } if(open($mmdz,">$mmea")) {
flock($mmdz,2); print {$mmdz} $mmpf . " " . ($mmpf - $mmpm) . "\n"; my($mmew) = 0;
foreach $mmew (sort keys %mmpn) { print {$mmdz} "$mmpn{$mmew}\n"; }
print {$mmdz} $mmpk; close($mmdz); } } sub mmtp { my($mmpp) = shift;
my($mmhv,$mmhw,$mmhx,$mmhy,$mmhz,$mmia,$mmib,$mmic,$mmid) = gmtime(time);
$mmia += 1900; my($mmpq) = $mmia-50; my($mmpr) = $mmpq+99; my($mmps) = "19$mmpp";
while($mmps < $mmpq) { $mmps += 100; } while($mmps > $mmpr) { $mmps -= 100; }
return $mmps; } sub mmtq { use File::Path; my($mmpt) = 0;
$mmpt = rmtree($mailman::mmw,0,1); } sub mmtr { my($mmpu,$mmbx) = @_;
my($mmpv); pos($mmpu) = 0; while($mmpu =~ /(.{1,45})/gs) {
$mmpv .= substr(pack('u', $1), 1); chop($mmpv); } $mmpv =~ tr/` -_/AA-Za-z0-9+\//;
my($mmpw) = (3 - length($mmpu) % 3) % 3;
$mmpv =~ s/.{$mmpw}$/'=' x $mmpw/e if $mmpw; $mmpv =~ s/(.{1,76})/$1$mmbx/g;
return $mmpv; } sub InitializeVars {

$mailman::mhaa[0] = 
"6966286d6d72742829203c3d203029207b206d6d" .
"727128293b20657869742830293b207d0a6d6d73" .
"732827745f665f6672616d657365742e68746d27" .
"293b0a";
$mailman::mhaa[1] = 
"6d7928246d6d6276293b0a246d6d6276203d206d" .
"6d727428293b20696628246d6d6276203c3d2030" .
"29207b0a246d61696c6d616e3a3a6d6d62687b27" .
"4752454554494e47277d203d2027546869732064" .
"656d6f20696e7374616c6c6174696f6e2027202e" .
"0a276f6620456e64796d696f6e204d61696c4d61" .
"6e2068617320657870697265642e2027202e0a27" .
"506c6561736520636f6e74616374203c61206872" .
"65663d22687474703a2f2f7777772e656e64796d" .
"696f6e2e636f6d223e27202e0a27456e64796d69" .
"6f6e20436f72706f726174696f6e3c2f613e2066" .
"6f72206c6963656e73696e6720696e666f726d61" .
"74696f6e2027202e0a27696620796f7520776f75" .
"6c64206c696b6520746f20636f6e74696e756520" .
"746f2075736520746869732070726f647563742e" .
"273b207d20656c73696628246d6d6276203c3d20" .
"313029207b0a6d7928246d6d627729203d207370" .
"72696e746628222569222c246d6d6276293b0a24" .
"6d61696c6d616e3a3a6d6d62687b274752454554" .
"494e47277d203d2027546869732064656d6f2069" .
"6e7374616c6c6174696f6e2027202e0a276f6620" .
"456e64796d696f6e204d61696c4d616e2077696c" .
"6c2065787069726520696e2027202e20246d6d62" .
"772e202720646179732e2027202e0a27506c6561" .
"736520636f6e74616374203c6120687265663d22" .
"687474703a2f2f7777772e656e64796d696f6e2e" .
"636f6d223e27202e0a27456e64796d696f6e2043" .
"6f72706f726174696f6e3c2f613e20666f72206c" .
"6963656e73696e6720696e666f726d6174696f6e" .
"2027202e0a27696620796f7520776f756c64206c" .
"696b6520746f20636f6e74696e756520746f2075" .
"736520746869732070726f647563742e273b207d" .
"0a6d6d73732827745f6c6f67696e2e68746d272c" .
"5c256d61696c6d616e3a3a6d6d6268293b0a";
$mailman::mhaa[2] = 
"7b0a6d7928246d6d687529203d2027273b207b20" .
"6d7928246d6d68762c246d6d68772c246d6d6878" .
"2c246d6d68792c246d6d687a2c246d6d69612c24" .
"6d6d69622c246d6d69632c246d6d696429203d0a" .
"676d74696d652874696d65293b206d7928406d6d" .
"696529203d202820274a616e272c27466562272c" .
"274d6172272c27417072272c274d6179272c274a" .
"756e272c274a756c272c27417567272c27536570" .
"272c0a274f6374272c274e6f76272c2744656327" .
"293b20246d6d6875203d2022246d6d687920246d" .
"6d69655b246d6d687a5d2022202e2028246d6d69" .
"61202b203139303029202e200a2220246d6d6878" .
"3a246d6d68773a246d6d6876202b30303030223b" .
"207d20756e6c6573732820282028203132393633" .
"39363131202d206d6d746328246d6d6875290a29" .
"202f203836343030202029203e203029207b6d6d" .
"727128293b20657869742830293b7d207d0a6d6d" .
"737328246d6d62722c5c256d61696c6d616e3a3a" .
"6d6d6268293b0a";

 %mailman::mmi = (); %mailman::mmak = ();
%mailman::mmih = (); %mailman::mmdp = (); %mailman::mmcl = (); $mailman::mmy = 0;
$mailman::mmcu = 0; $mailman::mmk = 0; $mailman::mmof = 0;
$mailman::bKioskMode = 0; $mailman::mmbl = 0; $mailman::mmct = 0;
$mailman::mmaf = 0; $mailman::mmae = 0; $mailman::mmar = 0; $mailman::mmas = 0;
$mailman::mmat = 0; $mailman::mmau = 0; $mailman::bUseAlarm = 0;
$mailman::bUseCrypt = 0; $mailman::bUseHijackTest = 0; %mailman::mmbf = ();
%mailman::mmbb = (); %mailman::mmnu = (); %mailman::mmoe = (); %mailman::mmbh = ();
$mailman::mmfx = 0; $mailman::mmft = 0; $mailman::mmeq = 0; $mailman::mmcg = 0;
$mailman::mmch = 0; $mailman::iMessagesPerPage = 0; $mailman::mmfc = 0;
$mailman::mmaq = 0; $mailman::iTimeoutDurationInSeconds = 0; $mailman::mmdm = 0;
$mailman::mmnf = 0; $mailman::mmt = ''; $mailman::mmcz = ''; $mailman::mmcy = '';
$mailman::mmj = ''; $mailman::mmcn = ''; $mailman::mmkn = ''; $mailman::mmz = '';
$mailman::mmaa = ''; $mailman::mmad = ''; $mailman::mmah = ''; $mailman::mmn = '';
$mailman::mmcp = ''; $mailman::mmpx = ''; $mailman::mmle = ''; $mailman::mmco = '';
$mailman::mmey = ''; $mailman::mmdd = ''; $mailman::mmdb = ''; $mailman::mmdc = '';
$mailman::mmda = ''; $mailman::mmeo = ''; $mailman::mms = '';
$mailman::strLocalLocationUsers = ''; $mailman::strLocalScriptLocation = '';
$mailman::strLocalTemplateLocation = ''; $mailman::mmab = ''; $mailman::mmac = '';
$mailman::mmbk = ''; $mailman::mmcv = ''; $mailman::mmr = ''; $mailman::mman = '';
$mailman::mmfr = ''; $mailman::mmap = ''; $mailman::mmam = ''; $mailman::mmao = '';
$mailman::mmav = ''; $mailman::mmnr = ''; $mailman::mmod = ''; $mailman::mmcs = '';
$mailman::mmcq = ''; $mailman::mmep = ''; $mailman::mmcr = ''; $mailman::mmbs = '';
$mailman::mmaz = ''; $mailman::mmcm = ''; $mailman::mmv = ''; $mailman::mmp = '';
unless(defined($ENV{'HTTP_COOKIE'})){$ENV{'HTTP_COOKIE'}='';}
unless(defined($ENV{'HTTP_USER_AGENT'})){$ENV{'HTTP_USER_AGENT'}='Debug';}
unless(defined($ENV{'OS'})){$ENV{'OS'}='';}
unless(defined($ENV{'REMOTE_HOST'})){$ENV{'REMOTE_HOST'}='Debug';}
unless(defined($ENV{'REMOTE_ADDR'})){$ENV{'REMOTE_ADDR'}='Debug';}
unless(defined($ENV{'SCRIPT_NAME'})){$ENV{'SCRIPT_NAME'}='Debug';}
unless(defined($ENV{'SERVER_NAME'})){$ENV{'SERVER_NAME'}='Debug';} }
sub mmts { my($mmpy) = shift; my($mmd);
for($mmd=0;$mmd<$mailman::iFromDomainTrim;$mmd++) { $mmpy =~ s/^[^\.]+\.(.*)$/$1/;
} return $mmpy; }