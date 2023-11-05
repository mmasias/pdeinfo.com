#!/usr/bin/perl

#######################################################################
#                     Application Information                          #
########################################################################

# Application Name: Extropia's WebCal
# Application Authors: Eric Tachibana (Selena Sol) and Gunther Birznieks
# Version: 5.0
# Last Modified: 17NOV98
#
# Copyright:
#
#     You may use this code according to the terms specified in
#     the "Artistic License" included with this distribution.  The license
#     can be found in the "Documentation" subdirectory as a file named
#     README.LICENSE. If for some reason the license is not included, you
#     may also find it at www.extropia.com.
#
#     Though you are not obligated to do so, please let us know if you
#     have successfully installed this application.  Not only do we
#     appreciate seeing the wonderful things you've done with it, but we
#     will then be able to contact you in the case of bug reports or
#     security announcements.  To register yourself, simply send an
#     email to register@extropia.com.
#
#    Finally, if you have done some cool modifications to the scripts,
#    please consider submitting your code back to the public domain and 
#    getting some community recognition by submitting your modifications
#    to the Extropia Cool Hacks page.  To do so, send email to
#    hacks@extropia.com
# 
# Description:
#
#    This calendar allows multiple users to view, add to, modify and
#    delete from a shared calendar. However, though clients can all see
#    all of the scheduled events, only the poster of a message can modify
#    that message. (This script runs multiple calendars with multiple
#    events databases as well).
#     
# Basic Usage:
#
#    1. Read the README.CHANGES, README.LICENSE, and README.SECURITY
#       files and follow any directions contained there
#
#    2. Change the first line of each of the scripts so that they
#       reference your local copy of the Perl interpreter. (ie:
#       #!/usr/local/bin/perl) (Make sure that you are using Perl 5.0 or
#       higher.)
#
#    3. Set the read, write and access permissions for files in the
#       application according to the instructions in the
#       README.INSTALLATION file.
#
#    4. Define the global variables in calendr.setup.cgi according to the
#       instructions in the README.INSTALLATION file.
#
#    5. Point your web browser at the script
#       (ie:http://www.yourdomain.com/cgi-bin/calendar.cgi)
#
# More Information
#
#    
#    You will find more information in the Documentation sub-directory.
#    We recommend opening the index.html file with your web browser to
#    get a listing of supporting documentation files.

########################################################################
#                     Application Code                                 #
########################################################################

#######################################################################
#                       Print http Header.                            #
#######################################################################

# First tell Perl to bypass the buffer.  Then, print out the HTTP
# header. We'll output this quickly so that we
# will be able to do some of our debugging from the web and so that in
# the case of a bogged down server, we won't get timed-out. 

  $! = 1;
  print "Content-type: text/html\n\n";

#######################################################################
#                       Require Libraries.                            #
#######################################################################

# Now require the necessary files with the subroutine at the end of this
# script marked by "sub CgiRequire".  We use this subroutine so that if
# there is a problem with the require, we will get a meaningful error
# message. 

# ($lib is the location of the Library directory where these files
# are to be stored.  Set $lib = "." if you do not have a Library
# directory.  This variable must be set in this file AS WELL AS in
# calendar.setup!!!)

  $lib = "./Library";

  &CgiRequire("$lib/cgi-lib.pl", "$lib/cgi-lib.sol",
           "$lib/auth-lib.pl", "$lib/date.pl");

#######################################################################
#                        Gather Form Data.                            #
#######################################################################

# Now use cgi-lib.pl to parse the incoming form data.  We'll pass
# cgi-lib.pl (*form_data) so that our variable will come out as
# $form_data{'key'} instead of $in{'$key'}.  I like to use form_data
# because it is easier for me to remember what the variable is.
# In the end, we will be able to reference all of the incoming form data as
# $form_data{'variablename'}

  &ReadParse(*form_data);

#######################################################################
#             Determine Which Calendar Database to Use.               #
#######################################################################

# Now we will need to determine which calendar database to use.  If the
# admin has set up more than one calendar, each calendar database will be
# in a subdirectory.  In order to reference these separate databases, the
# link to this script must have added ?calenar=Somesubdirectory at the end
# of the URL.  If we are asking for the main calendar, this variable will
# not be equal to anything.

  if ($form_data{'calendar'} ne "")
    {
    $form_data{'calendar'} =~ /^([\-\w]+)/o;
    $calendar_type = "./$1";
#    $calendar_type = "./$form_data{'calendar'}";
    }
  else
    {
    $calendar_type = "./";
    }

#######################################################################
#                            Define Variables                         #
#######################################################################

# Now we will define all of our variables by using the define file that
# you should have customized for your own site.

    &CgiRequire("./calendar.setup.cgi");

# Now we are going to want to make sure that we "remember" the
# session_file so that we can continually check for authentication and
# keep track of who the current client is.  However, if the client has
# already logged on, then we will not be going back through the
# authentication routines but will be getting the $session_file as form
# data (the same hidden field we are about to define).  So, we need to
# rename $form_data{'session_file'} to $session_file so that in both cases
# (first time to this point or continuing client) we'll have the
# session_id in the same variable name form.

  if ($form_data{'session_file'} ne "")
      {
      $session_file = $form_data{'session_file'};
      }

# Now rename some other variables with the same idea...

  if ($form_data{'year'} ne "")
    {
    $current_year = "$form_data{'year'}";
    }
  else
    {
    $current_year = "$the_current_year";
    }

  if ($form_data{'month'} eq "")
    {
    @mymonth = &make_month_array(&today);
    $current_month_name = &monthname($currentmonth);
    }
  else
    {
    @mymonth = &make_month_array(&jday($form_data{'month'},1,$current_year));
    $current_month_name = &monthname($form_data{'month'});
    }

#######################################################################
#                       Print out Generic Header HTML.                #
#######################################################################

# Okay, so if we got to this line, it means that the client has
# successfully made it past security.  So let's print out the basic
# header information.  You may modify everything between the 
# "print qq! and the !; but be careful of
# illegal characters like @ which must be preceded by a backslash 
# (i.e.: selena\@extropia.com)
#
# Also create the hidden form tags that will pass along the session_file
# info and the name of the calendar that we are dealing with.  It is
# crucial that we make sure to pass this info along through every page so
# that this script can keep track of the clients as they wander about.

#######################################################################
#                       Print out Calendar                            #
#######################################################################

# Now let's actually print out the dynamically generated calendar. We'll
# need to do this in two cases.  Firstly, if we have just logged on and
# the client is asking for the very first page ($form_data{'session_file'}
# ne "") and secondly, if the client has already been moving through
# various pages and has asked to view the calendar again
# ($form_data{'change_month_year'} ne "").  The || means "or".  Thus, if
# either case is true, we will proceed.

  if ($form_data{'change_month_year'} ne "" ||
      $ENV{'REQUEST_METHOD'} eq "GET" && $form_data{'day'} eq "")
    {

# Now print out the HTML calendar

    &header ("Selena Sol's Groupware Calendar Demo: $current_month_name - 
	      $current_year");
    print qq!
    <CENTER>
    <H2>$current_month_name - $current_year</H2>
    </CENTER>
    <TABLE BORDER = "2" CELLPADDING = "4" CELLSPACING = "4">
    <TR>!;

# Print up the table header (Weekdays).  For every day (foreach $day) in
# our list of days (@day_names), print out the day as a table header.
# Then plop in the table row delimiters...

    foreach $day (@day_names)
      {
      print "<TH>$day</TH>\n";
      }
    print "</TR>\n<TR>\n";

# Create the variable $count_till_last_day which we will use to make sure
# that we do not add on too many <TR>s.  Also clear out a new variable
# called $weekday which we will use to keep track of the two dimensional
# aspect of the calendar...that is, we need to break the calendar rows
# after every seventh cell representing as week. (We'll talk more about
# this in just a bit).

    $count_till_last_day = "0";
    $weekday = 0;

# For every day in the mymonth array we are going to need to create a
# cell for the calendar.  @mymonth, if you recall, is an array we got from 
# &make_month_array

#######################################################################
#                   Create a Table Cell for Each Day                  #
#######################################################################

    foreach $day_number (@mymonth)
      {

# Begin incrementing our two counter variables.

      $count_till_last_day++;
      $weekday++;

# Make sure that we add a break for every week to make the calendar 2 
# dimensional.  Thus, when we have gone through sets of seven days in this
# foreach loop, we will reset $weekday to zero.  Below, we'll use these
# values to determine where we drop the </TR><TR>, making a new calendar
# room.  When weekday is greater than 6, we'll know that we need a
# </TR><TR> so by setting the $weekday flag to zero, we will notify the
# script just a few lines down from here to insert the row break.

      $weekday = 0 if ($weekday > 6);

# Print a table cell for each day.  However, since we want to make each
# of the numbers in each of the cells clickable so that someone can click
# on the number to see a day view, we are going to need to manage a lot of
# information here.  Firstly, we will build a variable called
# $variable_list which will be used to create a long URL appendix which
# will be used to transfer information using URL encoding.  As we will
# learn more specifically later, the routine which generates the day views
# needs to have the day, year, and month values if it is to bring up a day
# view.  It must also have the session_file value (as all the routines in
# this script must) and the special tag view_day=on.  So we'll gather all
# of that information and appending it to the $variable_list variable.

      $variable_list = "";
      $variable_list = "day=$day_number&year=$currentyear";
      $variable_list .= "&month=$currentmonth";
      $variable_list .= "&session_file=$session_file";
      $variable_list .= "&calendar=$form_data{'calendar'}";
      $variable_list .= "&view_day=on";

# Now create the actual cell.  Notice, the number in each cell is made
# clickable by using URL encoding to tag the URL with all of the variables
# we want passed.

      print qq!<TD VALIGN = "top" WIDTH = "150">\n!;
      print qq!<A HREF = "$this_script_url?$variable_list">$day_number</A>\n!;

# Grab the subject listings for all the entries on that day.  Make sure
# also that if we are unable to open the database file, that we send a
# useful message back to us for debugging.  We'll do this using the
# open_error subroutine in cgi-lib.sol passing the routine the location of
# the database file.    

      open (DATABASE, "$database_file") || &CgiDie ("I am sorry, but I
	was unable to open the calendar data file in the Create a Table
	Cell for Each Day routine.  The value I have is $database_file.
	Would you please check the path and the permissions.");

      while (<DATABASE>)
        {
        ($day, $month, $year, $username, $first_name, $last_name, $email,
         $subject, $time, $body, $database_id_number) = split (/\|/,$_);

# We are going to need to run through all of the database items and look
# for database rows whose subject belong on the day cell we are building.
# Thus, for every row, we must determine if the day, month, and year of
# the item on that row equal the day, month and year of the cell we are
# building.

        if ($day eq "$day_number" && $month eq "$currentmonth" && 
            $year eq "$currentyear")
          {

# If we were able to answer true to all of those conditions, then we have
# found a match and we should print out the subject in that cell.

          print qq!<BR><FONT SIZE = "1">$subject</FONT>\n!;  

          } # End of if ($day eq "$day_number" && $month eq ...
        } # End of while (<DATABASE>)

# Once we have checked all the way through the database, we should close
# that cell and move on to the next.

      print "</TD>\n";

# If, however, we have reached the end of a week row, we are going to need
# to begin a new table row for the next week.  If $weekday is equal to
# zero, then we know that it is time.  If not, continue with the row.
# (BTW, here we use == instead of just = because if we used =, perl would
# interpret the part inside the if () to be assigning the value of zero to
# $weekday...which it would do...and evaluate the whole process as true.
# That of course would undercut the whole point of counting with
# $weekday.)

      if ($weekday == 0)
	{
	print "</TR>\n";

# But before we just blindly print up another table row, we better be sure
# that we haven't actually reached the end of the month...Thus, if
# $count_till_last_day equals @mymonth we know that there are no more days
# left and we should not begin a new row.  (Notice that when we reference
# @mymonth without quotes we receive the numerical value of the number of
# elements in the array).

        unless ($count_till_last_day == @mymonth)
          {
          print "<TR>";
          } # End of unless ($count_till_last_day == @mymonth)

        } # End of if ($weekday == 0)
      } # End of foreach $day_number (@mymonth)

# Finally, once we are done making all of the cells for the calendar, 
# print up the HTML footer

    print qq!
    </TABLE>
    </CENTER>
    <BLOCKQUOTE>
    For day-at-a-glance-calendar, click on the day number on the
    calendar above.
    <BR>
    Or, to see another $year month, choose one!;

# Create a select box which will allow the client to choose a new month to
# view.  We'll use the subroutine select_a_month at the end of this
# script.

    &select_a_month;

    print "<P>Or, to see another year, select one\n";

# Likewise, create a select box which will allow the client to choose a
# new year to view.  We'll use the subroutine select_a_year at the end
# of this script.

    &select_a_year;

    print qq!
    <P>
    * Note: This calendar is best viewed by opening your
    browser window to its maximum size. And, you can only submit
    a month if the year field is cleared.<P>
    </BLOCKQUOTE>
    <CENTER>
    <INPUT TYPE = "submit" NAME = "change_month_year" 
        VALUE = "Change Month/Year">
    <INPUT TYPE = "reset" VALUE = "Clear this form">
    <INPUT TYPE = "submit" NAME = "add_item_form"
         VALUE = "Add Item">
    </FORM>
    </CENTER>
    </BODY>
    </HTML>!;
    exit;
    } # End of if ($form_data{'change_month_year'} ne "" ||...

#######################################################################
#                              View a Day.                            #
#######################################################################

# Okay, in the routine above we made every number in every cell of the
# calendar clickable so that the client could actually view the detailed
# descriptions of the events scheduled for that day.  In the URL encoded
# string we built, we included a tag view_day=on.  Here is where that
# comes in handy.  This if test will check to see if the person has
# clicked on a number, cause if they have, we will evaluate to true.  If
# true, print the header.

  if ($form_data{'view_day'} eq "on")
    {
    &header ("$current_month_name $form_data{'day'}, $current_year");
    print qq!
    <CENTER>
    <H2>$current_month_name $form_data{'day'}, $current_year</H2>
    </CENTER>!;

# Now open up the database again and look for database rows that match the
# requested day, month, and year.

    open (DAYFILE, "$database_file") || &CgiDie ("I am sorry, but I was
	unable to open the calendar data file in the View a Day routine.  The
	value I have is $database_file.  Would you please check the permissions
	and path.");

    while (<DAYFILE>)
      {

# Just as we did above in the routine for generating subject lines for
# day cells, we are going to pay attention only to database rows that
# match our client defined day, month and year.

      ($day, $month, $year, $username, $first_name, $last_name, $email,
             $subject, $time, $body, $database_id_number) = split (/\|/,$_);
      if ($day eq "$form_data{'day'}" && $month eq "$form_data{'month'}"
             && $year eq "$current_year")
        {

# Set the $item_found flag so that we know that we have actually found an
# item in the database.

        $item_found = "yes";

# Print out a <HR> delimited detailed list of events on the day, then a
# standard footer.

        print qq!
        <B>Time:</B> $TIME{$time}<BR>
        <B>Subject:</B> $subject<BR>
        <B>Poster:</B> <A HREF = "mailto:$email">$first_name $last_name</A><BR>
        <B>Body:</B><BLOCKQUOTE>$body</BLOCKQUOTE>
        <P><CENTER><HR WIDTH = "50%"></CENTER><P>!;
        } # End of if ($day eq "$form_data{'day'}" &&........)
      } # End of while (<DAYFILE>)

# If we were not able to find any items in the database, we should let the
# client know.  So if $item_found was never set to "yes", we know to send
# them back a little note of explanation.

    if ($item_found ne "yes")
      {
      print "<BLOCKQUOTE>It appears that there are no entries posted for
             this day.  Would you like to add one?</BLOCKQUOTE>";

      }

    print qq!
    <CENTER>
    <INPUT TYPE = "hidden" NAME = "day" VALUE = "$form_data{'day'}">
    <INPUT TYPE = "hidden" NAME = "month" VALUE = "$form_data{'month'}">
    <INPUT TYPE = "hidden" NAME = "year" VALUE = "$current_year">
    <INPUT TYPE = "submit" NAME = "modify_item_form"
         VALUE = "Modify Item">
    <INPUT TYPE = "submit" NAME = "delete_item_form"
         VALUE = "Delete Item">
    <INPUT TYPE = "submit" NAME = "add_item_form"
         VALUE = "Add Item">
    <INPUT TYPE = "submit" NAME = "change_month_year"
         VALUE = "View Month">
    </FORM>
    </CENTER>
    </BODY>
    </HTML>!;
    exit;      
    }

#######################################################################
#                       Basic User Authentication                     #
#######################################################################

# Now let's check to see if the client is a user who is authorized to use
# this script.  We will use the web of routines in the library
# file session-lib.pl to do the following:
#
# 1. Ask the user to submit a userid and password.
# 2. Check that userid/password pair against the information in
#    $user_file.
# 3. If the information is invalid, disallow entrance and provide a
#    routine for the user to apply for an account.
# 4. If the information was valid, send back to this script a "session
#    file id" corresponding to a session file which will have been created
#    by session-lib.pl and which will contain the users personal
#    information.  This script will then pass along the session id as a
#    hidden variable throughout in order to make sure that the user is
#    valid.

# We'll pass the subroutine GetSessionInfo which is contained in
# auth-lib.pl three parameters, the $session_file value (which will be
# nothing if one has not been set yet), the name of this script (so it can
# provide links back) and the associative array of form data we got from
# cgi-lib.pl.

  ($session_file, $session_username, $session_group, $session_first_name,
	$session_last_name, $session_email) = 
        &GetSessionInfo($session_file, $this_script_url, *form_data);

# Take off the newline character for the last member in the array.

  chomp $session_email;

#######################################################################
#                      Create Add Item Form                           #
#######################################################################

# Now, if the client wants to add an item, we are going to need to present
# them with a form which they can use to submit information for each of
# the database fields.

  if ($form_data{'add_item_form'} ne "")
    {

    &header ("Add an Item to Selena's Groupware Calendar Demo");

# We'll use the subroutine submission_form at the end of this script to
# generate a form with input fields for every item in the database which
# can be manipulated by the client.

    &submission_form;

# Print out a standard footer and quit.

    print qq!
    <CENTER><P>
    <INPUT TYPE = "submit" NAME = "add_item" VALUE = "Add Item">
    <INPUT TYPE = "reset" VALUE = "Clear This Form">
    <INPUT TYPE = "submit" NAME = "change_month_year" VALUE = "View Month">
    </CENTER></BODY></HTML>!;
    exit;
    }

#######################################################################
#                     Add an Item to the Database                     #
#######################################################################

  if ($form_data{'add_item'} ne "")
    {

    &header ("Adding an Item to the Calendar Database");

# Make sure that the client has filled out all the necessary fields in the
# submission form.  First we'll get a list of the variable names (keys)
# associated with the associative array %form_data given to us by
# cgi-lib.pl.  Thus, we will have a list of every field, empty or not,
# submitted by our form.

    @form_data = keys (%form_data);

# For every element in our @form_data array, check to see if the
# associated value in %form_data has content.  If not, send back an error
# message and quit.

#######################################################################
#                Did They Fill Out All The Form Fields?               #
#######################################################################

    foreach $variable_name (@form_data)
      {
      if ($form_data{$variable_name} eq "" && $variable_name
        ne "calendar")
        {
        print qq!
        <BLOCKQUOTE>
        <FONT SIZE = "+3">
        I'm very sorry but you must enter something in the 
        <B>$variable_name</B> input box.  Please hit the back
        button and try again.
        </FONT>
        </BLOCKQUOTE>
        </BODY>
        </HTML>!;
        exit;
        }
      }

# If they have entered data into all of the fields, we can go ahead and
# add their new entry.  

# Now create a lockfile while we edit our database file.  The reason that
# we do this is so that if two people are trying to edit the datafile at
# one time, one person will not destroy the modifications made by the
# other person.  We'll create the lock file using the subroutine
# GetFileLoc in cgi-lib.sol, passing it one parameter, the location of
# the lock file used by this program.  You should definitely not create
# the lock file yourself...

  &GetFileLock ("$lock_file");

# First get a unique number from the counter file by
# using the subroutine counter in cgi-lib.sol.  We'll pass the routine one
# parameter which will be the location of the counter file used by this
# program.  The unique counter number is essential because every row must
# be uniquely identifiable for modifications and deletions.  The numbers
# don't need to be in any order, and there can be gaping holes between
# numbers (as when items are deleted) but they must be unique.

    &counter($counter_file);

#######################################################################
#                        Make The Addition                            #
#######################################################################

# If we got past the lockfile routine it means that we are now the sole
# owner of the database file and can safely make changes.  So let's write
# the contents of the new entry to the database file (appending (>>) the
# new data to the end of the existing list of items...

    open (DATABASE, ">>$database_file") || &CgiDie ("I am sorry, but I was
	unable to open the calendar data file in the  Make The Addition
	routine. The value I have is $database_file.  Would you please
	check the path and permissions.");

# Now let's format the incoming form data so that it will all stay on one
# line.  We'll substitute (=~ s/) all occurrences (/g) of newlines (\n) for
# <BR> and all occurrences of two hard returns (\r\r) for <P>'s.  

    foreach $value (@field_values)
      {
      $form_data{$value} =~ s/\n/<BR>/g;
      $form_data{$value} =~ s/\r\r/<P>/g;
      $form_data{$value} =~ s/\|/:/g;
      $form_data{$value} =~ s/\-/:/g;
      }

# Now let's simplify some of the variables and generate the new database
# row. (.= means that you should append the new value to the end of the
# existing value for the variable.)

  if ($session_first_name eq "")
    {
    $session_first_name =  "$form_data{'first_name'}";
    $session_last_name =  "$form_data{'last_name'}";
    $session_email = "$form_data{'email'}";
    }
    $subject = "$form_data{'subject'}";
    $event_time = "$form_data{'time'}";
    $month = "$form_data{'month'}";
    $day = "$form_data{'day'}";
    $year = "$form_data{'year'}";
    $body = "$form_data{'body'}";

    $new_row = "";
    $new_row .= "$day\|$month\|$year\|$session_username\|";
    $new_row .= "$session_first_name\|$session_last_name\|$session_email\|";
    $new_row .= "$subject\|$event_time\|$body\|$item_number";

# Add the new database row to the database file and delete the lock file
# so that someone else may modify the database file.  Don't forget the new
# line at the end of the database row so that the next item entered will
# have its own line.
 
    print DATABASE "$new_row\n";
    close (DATABASE);
    &ReleaseFileLock ("$lock_file");

# Print out the standard page footer.

    print qq!
    <H2><CENTER>Your item has been added, thanks.</H2>
    <INPUT TYPE = "hidden" NAME = "day" VALUE = "$form_data{'day'}">
    <INPUT TYPE = "hidden" NAME = "month" VALUE = "$form_data{'month'}">
    <INPUT TYPE = "hidden" NAME = "year" VALUE = "$current_year">
    <INPUT TYPE = "submit" NAME = "change_month_year" 
           VALUE = "Return to the Calendar">
    </BODY>
    </HTML>!;

# Now it is time to sort the entries in the database file so that we can
# make sure that when people choose day views, their entries come out
# ordered by time.  Once again, we'll create the lock file so that no one
# else can modify the database file while we are modifying it.

   &GetFileLock ("$lock_file");
   open (DATABASE, "$database_file") ||  &CgiDie ("I am sorry, but I was
        unable to open the calendar data file in the  Make The Addition
        routine. The value I have is $database_file.  Would you please
        check the path and permissions.");

# First, add every row in our database file to an array called
# @database_fields

    while (<DATABASE>)
      {
      @database_fields = split (/\|/, $_);

# Now, create a variable called $comment_row which will be used, for now
# to hold COMMENT lines in the database file since we don not want them
# sorted along with the rest of the items.

      if ($_ =~ /^COMMENT:/)
        {
        $comment_row .= $_;
        }

# If the database row is not a COMMENT row, we are going to find the field
# which has the time of the event and append it to the front of the
# database row (so it occurs twice...once at the beginning of the line and
# once in the middle somewhere) and add (push) the whole string
# ($sortable_row) into a growing array called @database_rows.  We'll
# explain the reason for this in the next comment paragraph.

      else
        {
        $sortable_row = "$database_fields[$field_num_time]~~";
        $sortable_row .= $_;
        push (@database_rows, $sortable_row); 
        }
      }

# When we have added all of the "modified" rows to the array
# @database_rows we'll sort that array.  This is why we wanted to append
# the time to the beginning of each of the rows...the sort routine will
# now sort all of the database items by event time.

    @sorted_temp_database = sort (@database_rows);

# Now go through @sorted_temp_database and take out the extra event_time
# string at the beginning of each database row.  We do this by splitting
# the string at - and then "pushing" the part of the string which
# corresponds to the original database row back into the array
# @final_sorted_database.

    foreach $database_row (@sorted_temp_database)
      {
      ($extra_event_time, $true_database_row) = split (/~~/, $database_row);    
      push (@final_sorted_database, $true_database_row);
      }
    close (DATABASE);

# Now we are going to need to change the original database file so that it
# represents our sorted order.  To do this, we will first create a
# temporary file to which we will first reprint all of the comment rows
# stored in the variable $comment_row.

    open (TEMPFILE, ">$temp_file") || &CgiDie ("I am sorry, but I was
        unable to open the temp file in the Make The Addition
        routine. The value I have is $temp_file.  Would you please
        check the path and permissions.");

    print TEMPFILE "$comment_row";

# Then for each of the database rows stored in @final_sorted_database,
# we'll print to the temp file.

    foreach $row (@final_sorted_database)
      {
      print TEMPFILE "$row";
      }

    close (TEMPFILE);

# Then we will copy our temp file over the original database file so that
# the resulting file will represent the sort.  Then of course, delete the
# lock file so others can manipulate the database.

   unlink ($database_file);
   rename ($temp_file, $database_file ) || 
           &CgiDie("Unable to rename temporay file");
    &ReleaseFileLock ("$lock_file");
    exit;
    }

#######################################################################
#                   Print out Modify Item Form.                       #
#######################################################################

  if ($form_data{'modify_item_form'} ne "")
    {

    &header ("Modify and Item");

# Print out the basic header including the hidden fields which we want
# transferred to the modification routines which must have all the user
# information if they are to recreate database rows.  Since the
# modification routines are going to compare incoming form data to
# database row information, we will want this information to come in with
# the rest of the form data.

    print qq!
    <INPUT TYPE = "hidden" NAME = "username" VALUE = "$session_username">
    <INPUT TYPE = "hidden" NAME = "first_name" VALUE = "$session_first_name">
    <INPUT TYPE = "hidden" NAME = "last_name" VALUE = "$session_last_name">
    <INPUT TYPE = "hidden" NAME = "email" VALUE = "$session_email">
    <CENTER>
    <H2>$current_month_name $form_data{'day'}, $current_year</H2>
    </CENTER>!;

# Begin a table which we will use to display all of the items posted by
# the client on the day they are interested in.  But, for the time being,
# let's not print out the table, but build it in a variable called $table

    $table .= "<TABLE BORDER = \"1\" CELLSPACING = \"2\" CELLPADDING = \"2\"
               WIDTH = \"1100\">\n";
    $table .= "<TR>\n";
    $table .= "<TH>Modify Item</TH>\n";

# Create the header row

    foreach $name (@field_names)
      {
      $table .= "<TH>$name</TH>\n";
      }
    $table .= "</TR>\n";

# Now open the database and check for items which correspond to the user
# as well as the day, month and year they have requested to look at or
# modify.

    open (DAYFILE, "$database_file") || &CgiDie ("I am sorry, but I was
        unable to open the calendar data file in the Print out Modify Item Form
        routine. The value I have is $database_file.  Would you please
        check the path and permissions.");

    while (<DAYFILE>)
      {
      chomp $_; # Make sure to take out the newline.

# Split out the database row as usual, but this time also use them to make
# an array called @database_values which we'll use in just a bit.

      ($day, $month, $year, $username, $first_name, $last_name, $email,
           $subject, $time, $body, $database_id_number) = split (/\|/,$_);

      @database_values = split (/\|/,$_);

# Pay attention only to items specific to user, day, month and year

      if ($day eq "$form_data{'day'}" && $month eq "$form_data{'month'}"
         && $year eq "$form_data{'year'}" && ($session_username eq "$username" ||
         $session_group eq "admin"))
        {

# Flag the fact that we did indeed find an item

        $item_found = "yes"; 

# Continue adding to out $table variable by adding the table row
# corresponding to the database row which matched.  Also, offer them a
# radio button so that they can select which table row to modify.

        $table .= "<TR>\n";
        $table .= "<TD ALIGN = \"center\">";
        $table .= "<INPUT TYPE = \"radio\" NAME =\"item_to_modify\"";
        $table .= "VALUE=\"$database_id_number\"></TD>\n";

        foreach $value (@database_values)
          {
          $table .= "<TD>$value</TD>\n";
          }
          $table .= "</TR>\n";
        }
      }

    $table .= "</TR></TABLE><P><CENTER>\n";

# If $item_found is still not equal to yes, it means that we did not match
# any items so we should send the client back a little note.

    if ($item_found ne "yes")
      {
      print qq!
      <BLOCKQUOTE>
      I'm sorry, you have not posted any items for this day, so
      there is nothing for me to modify.
      </BLOCKQUOTE>
      <CENTER>    
      <INPUT TYPE = "submit" NAME = "change_month_year"
         VALUE = "View Month">
      </BODY>
      </HTML>!;
      exit;
      }

# If however, it did equal yes, we can go ahead and print out our table.

    print "$table";

# Now we'll need to give the client a form similar to the add item form so
# that they can make any modifications that they want.  Do that with the
# submission_form subroutine at the end of this script passing it the
# parameter, modify so that it will know to output the form relative to a
# modify rather than to an add.

  &submission_form("modify");

# Finally print out a standard footer and quit.

    print qq!
    <CENTER>
    <P>
    <BLOCKQUOTE><I>Note: Make sure to select an item to modify
    using the radio buttons on the top table.  Then change any of
    the form inputs you want changed, leaving the others as they
    are.  Feel free to cut and paste from the top table to the
    bottom table if you only need to change a small amount of
    text</I></BLOCKQUOTE>
    <INPUT TYPE = "submit" NAME = "modify_item" 
	   VALUE = "Modify Selected Item">
    <INPUT TYPE = "reset" VALUE = "Clear This Form">
    </CENTER>
    </FORM>
    </BODY>
    </HTML>!;

    exit;
    }

#######################################################################
#                    Print Out Delete Item Form                       #
#######################################################################

# Now let's print out a form for item deletion in case that is what they
# want.

    if ($form_data{'delete_item_form'} ne "")
    {
    &header ("Delete an Item");
    print "<CENTER>\n";
    print "<H2>$current_month_name $form_data{'day'}, $current_year</H2>\n";
    print "</CENTER>\n";

# Just as we did for the modify form, create the $table variable and
# print up the delete form or the error message in case no items were
# found relative to the client.

    $table = "";
    $table .= "<TABLE BORDER = \"1\" CELLSPACING = \"2\" CELLPADDING = \"2\"
               WIDTH = \"1100\">";
    $table .= "\n<TR>\n";
    $table .= "<TH>Delete Item</TH>"; 

    foreach $name (@field_names)
      {
      $table .= "<TH>$name</TH>\n";
      }
    $table .= "</TR>\n";

    open (DAYFILE, "$database_file") || &CgiDie ("I am sorry, but I was
        unable to open the calendar data file in the Print Out Delete Item Form
        routine. The value I have is $database_file.  Would you please
        check the path and permissions.");

    while (<DAYFILE>)
      {
      chomp $_;
      ($day, $month, $year, $username, $first_name, $last_name, $email,
           $subject, $time, $body, $database_id_number) = split (/\|/,$_);

      @database_values = split (/\|/,$_);

      if ($day eq "$form_data{'day'}" && $month eq "$form_data{'month'}"
         && $year eq "$form_data{'year'}" && ($session_username eq "$username" ||
         $session_group eq "admin"))
        {
        $item_found = "yes";
        $table .= "<TR>\n";
        $table .= "<TD ALIGN = \"center\">";
        $table .= "<INPUT TYPE = \"radio\" NAME =\"item_to_delete\"";
        $table .= "VALUE=\"$database_id_number\"></TD>\n";

        foreach $value (@database_values)
          {
          $table .= "<TD>$value</TD>\n";
          }
          $table .= "</TR>\n";
        }
      }

    if ($item_found ne "yes")
      {
      print qq!
      <BLOCKQUOTE>
      I'm sorry, you have not posted any items for this day, so
             there is nothing for me to modify.
      </BLOCKQUOTE><CENTER>
      <INPUT TYPE = "submit" NAME = "change_month_year"
         VALUE = "View Month">
      </BODY>
      </HTML>!;
      exit;
      }

    print qq!
    $table
    </TR>
    </TABLE>
    <CENTER>
    <P>
    <INPUT TYPE = "hidden" NAME = "day" VALUE = "$form_data{'day'}">
    <INPUT TYPE = "hidden" NAME = "month" VALUE = "$form_data{'month'}">
    <INPUT TYPE = "hidden" NAME = "year" VALUE = "$current_year">
    <INPUT TYPE = "submit" NAME = "delete_item" 
           VALUE = "Delete Selected Item">
    <INPUT TYPE = "submit" NAME = "change_month_year" 
           VALUE = "Return to the Calendar">
    </CENTER>
    </FORM>
    </BODY>
    </HTML>!;
    exit;
    }

#######################################################################
#                     Delete an Item.                                 #
#######################################################################

# Let's make a deletion if the client requested that we do so...

  if ($form_data{'delete_item'} ne "")
    {

# However, we need to make sure that the client actually chose an item to
# delete with the radio buttons.

    if ($form_data{'item_to_delete'} eq "")
      {
      &header ("Woopsy");
      print qq!
      <CENTER><H2>Delete an Item in the Database Error</H2></CENTER>
      <BLOCKQUOTE>
      I'm sorry, I was not able to modify the database because
      none of the radio buttons on the table was selected so I was
      not sure which item to delete.  Would you please make sure
      that you select an item \"and\" fill in the new information.
      Just hit your back button.  Thanks.
      </BLOCKQUOTE>!;
      exit;
      }

# Lock the database file as we did for the add item routines.

    &GetFileLock ("$lock_file");

# Create a temporary file as we did for the add routines.

    open (TEMP, ">$temp_file") || &CgiDie ("I am sorry, but I was unable
	to open the temp file in the Delete an Item routine.  The value I
	have is $temp_file.  Would you check the path and permissions.");

    close (TEMP);

# While there is data in the database file check to see which item matches
# the  deletion

    open (DATA, "$database_file") || &CgiDie ("I am sorry, but I was unable
        to open the data file in the Delete an Item routine.  The value I
        have is $database_file.  Would you check the path and
	permissions.");

    while (<DATA>)
      {
      @grepfields=split(/\|/,$_);

# Get the unique database id for the database row and chop off the
# newline.

      $database_id = pop (@grepfields);
      chomp $database_id;

# If the unique database id of the row is not equal to the database id
# number submitted by the client then we do not want to delete it so we'll
# print it to the temp file.


      if ($database_id ne "$form_data{'item_to_delete'}")
        {
        open (TEMP, ">>$temp_file") || &CgiDie ("I am sorry, but I was unable
        to open the temp file in the Delete an Item routine.  The value I
        have is $temp_file.  Would you check the path and permissions.");
        print TEMP "$_";
        close (TEMP);
        }
      } # End of while (<DATA>)

# Once we have gone through all of the items in the database, we can copy
# the temp file over the database file and the deletion will have been
# made since the row which matched the database id number will not have
# been printed to the temp file.  Close the database file and delete the
# lock file so others can modify the database file.

    close (DATA);
    unlink ($database_file);

    rename ($temp_file, $database_file ) || 
           &CgiDie("Unable to rename temporay file");
    &ReleaseFileLock ("$lock_file");

# Print up a standard footer

    &header ("Deleting an Item from the Calendar");
    print qq!
    <CENTER>
    <FONT SIZE = "+3">Your item has been deleted
    </FONT>
    <P>
    <INPUT TYPE = "hidden" NAME = "day" VALUE = "$form_data{'day'}">
    <INPUT TYPE = "hidden" NAME = "month" VALUE = "$form_data{'month'}">
    <INPUT TYPE = "hidden" NAME = "year" VALUE = "$current_year">
    <INPUT TYPE = "submit" NAME = "change_month_year"
           VALUE = "Return to the Calendar">
    </CENTER>
    </BODY>
    </HTML>!;
    exit;
    }

#######################################################################
#                             Modify Item                             #
#######################################################################

# Now let's modify an item if the client asked us to do so.

  if ($form_data{'modify_item'} ne "")
    {

# However, we need to make sure that the client actually chose an item to
# modify with the radio buttons.

    &header("Modify and Item in the database");

    if ($form_data{'item_to_modify'} eq "")
      {
      print qq!
      <CENTER><H2>Modifying an Item in the Database Error</H2></CENTER>
      <BLOCKQUOTE>
      I'm sorry, I was not able to modify the database because
      none of the radio buttons on the table was selected so I was
      not sure which item to modify.  Would you please make sure
      that you select an item \"and\" fill in the new information.
      Just hit your back button.  Thanks.
      </BLOCKQUOTE>!;
      exit;
      }

# Just as we did above, create the lock file and temp file.

    &GetFileLock ("$lock_file");

    open (TEMPFILE, ">$temp_file") || &CgiDie ("I am sorry, but I was unable
        to open the temp file in the Modify Item routine.  The value I
        have is $temp_file.  Would you check the path and permissions.");

    open (DATABASE, "$database_file") || &CgiDie ("I am sorry, but I was
	unable to open the data file in the Modify Item routine.  The
	value I have is $database_file.  Would you check the path and
	permissions.");

# As we did for deletion, get the unique database id number for each row.
# (pop(@fields)) But this time, we will make sure to add it back into the
# array so that we have a whole array again push (@fields, $item_id).
# And don't forget to chop off the newline.

    while (<DATABASE>)
      {
      @fields = split (/\|/, $_);
      $item_id = pop(@fields);
      chomp $item_id;
      push (@fields, $item_id);

# If the item id matches the one that the client submitted, then we'll
# rename the  @fields array to @old_fields.  Otherwise, we'll ass the line
# to our growing list of database rows in $new_data

      if ($item_id eq "$form_data{'item_to_modify'}")
        {
        @old_fields = @fields;
        }
      else
        {
        $new_data .= "$_";
        }
      } # End of  while (<DATABASE>)

# Once we get through all the items in the database, we should have found
# one that matched the modify item selected by the client and the rest
# should be stored in $new_data.  So now we'll print the rows in $new_data
# to our temp file.

    print TEMPFILE "$new_data";

# Now we are going to need to substitute the new data submitted by the
# client for the old data that was in the database.  We'll initialize a
# couple of variable first, $counter and $new_line.  We'll use counter to
# keep track of the database fields that we have edited and use $new_line
# to create the new database row.

    $counter = 0;
    $new_line = "";

    until ($counter >= @field_values)
      {
      $value = "";
      $value = "$field_values[$counter]";

      if ($form_data{$value} eq "")
        {
        $new_line .= "$old_fields[$counter]|";
        }
      elsif ($session_group eq "admin" && $counter == $index_of_username)
        {
        $new_line .= "$old_fields[$counter]|";
        }

      elsif ($session_group eq "admin" && $counter == $index_of_first_name)
        {
        $new_line .= "$old_fields[$counter]|";
        }

      elsif ($session_group eq "admin" && $counter == $index_of_last_name)
        {
        $new_line .= "$old_fields[$counter]|";
        }

      elsif ($session_group eq "admin" && $counter == $index_of_email)
        {
        $new_line .= "$old_fields[$counter]|";
        }
      else
        {
        $form_data{$value} =~ s/\n/<BR>/g;
        $form_data{$value} =~ s/\r\r/<P>/g;
#        $form_data{$value} =~ s/\|/~~/g;

        if ($form_data{$value} eq "")
          {
          $form_data{$value} = "<CENTER>-</CENTER>";
          }
        $new_line .= "$form_data{$value}|";
        } # End of else

      $counter++;

      } # End of until ($counter >= @field_values)

    chomp $new_line; # take off last |

# Close everything up and copy the temp file over the original, then
# release the lock file.

    print  TEMPFILE "$new_line\n";
    close (TEMPFILE);
    close (DATABASE);
    unlink ($database_file);
    rename ($temp_file, $database_file ) || 
           &CgiDie("Unable to rename temporay file");
    &ReleaseFileLock ("$lock_file");

# Now print up the usual footer with an option to add another item.

    print qq!
    <CENTER>
    <H2>Your Item has been Modified</H2>
    <INPUT TYPE = "hidden" NAME = "day" VALUE = "$form_data{'day'}">
    <INPUT TYPE = "hidden" NAME = "month" VALUE = "$form_data{'month'}">
    <INPUT TYPE = "hidden" NAME = "year" VALUE = "$current_year">
    <INPUT TYPE = "submit" NAME = "change_month_year"
           VALUE = "Return to the Calendar">
    </CENTER>
    </BODY>
    </HTML>!;

# Now it is time to sort the entries in the database file so that we can
# make sure that when people choose day views, their entries come out
# ordered by time.  Once again, we'll create the lock file so that no one
# else can modify the database file while we are modifying it.

    &GetFileLock ("$lock_file");
    open (DATABASE, "$database_file") ||  &CgiDie ("I am sorry, but I was
        unable to open the data file in the Modify Item routine.  The
        value I have is $database_file.  Would you check the path and
        permissions.");

# First, add every row in our database file to an array called
# @database_fields

    while (<DATABASE>)
      {
      @database_fields = split (/\|/, $_);

# Now, create a variable called $comment_row which will be used, for now
# to hold COMMENT lines in the database file since we don not want them
# sorted along with the rest of the items.

      if ($_ =~ /^COMMENT:/)
        {
        $comment_row .= $_;
        }

# If the database row is not a COMMENT row, we are going to find the field
# which has the time of the event and append it to the front of the
# database row (so it occurs twice...once at the beginning of the line and
# once in the middle somewhere) and add (push) the whole string
# ($sortable_row) into a growing array called @database_rows.  We'll
# explain the reason for this in the next comment paragraph.

      else
        {
        $sortable_row = "$database_fields[$field_num_time]~~";
        $sortable_row .= $_;
        push (@database_rows, $sortable_row); 
        }
      }

# When we have added all of the "modified" rows to the array
# @database_rows we'll sort that array.  This is why we wanted to append
# the time to the beginning of each of the rows...the sort routine will
# now sort all of the database items by event time.

    @sorted_temp_database = sort (@database_rows);

# Now go through @sorted_temp_database and take out the extra event_time
# string at the beginning of each database row.  We do this by splitting
# the string at - and then "pushing" the part of the string which
# corresponds to the original database row back into the array
# @final_sorted_database.

    foreach $database_row (@sorted_temp_database)
      {
      ($extra_event_time, $true_database_row) = split (/~~/, $database_row);    
      push (@final_sorted_database, $true_database_row);
      }
    close (DATABASE);

# Now we are going to need to change the original database file so that it
# represents our sorted order.  To do this, we will first create a
# temporary file to which we will first reprint all of the comment rows
# stored in the variable $comment_row.

    open (TEMPFILE, ">$temp_file") || &CgiDie ("I am sorry, but I was
        unable to open the temp file in the Modify Item routine.  The
        value I have is $temp_file.  Would you check the path and
        permissions.");

    print TEMPFILE "$comment_row";

# Then for each of the database rows stored in @final_sorted_database,
# we'll print to the temp file.

    foreach $row (@final_sorted_database)
      {
      print TEMPFILE "$row";
      }

    close (TEMPFILE);

# Then we will copy our temp file over the original database file so that
# the resulting file will represent the sort.  Then of course, delete the
# lock file so others can manipulate the database.

    unlink ($database_file);
    rename ($temp_file, $database_file ) || 
           &CgiDie("Unable to rename temporay file");
    &ReleaseFileLock ("$lock_file");

    exit;
    }

# Finally, make a default in the case that the client got through
# everything without finding what they wanted...probably because they hit
# return when typing into a text box

  &header("Wooopsy");
  print qq!
  <BLOCKQUOTE>
  I'm sorry, you are not allowed to type return when
  typing in your subject.  Please hit the back button and try
  again.
  </BLOCKQUOTE>
  <CENTER>
  <INPUT TYPE = "submit" NAME = "change_month_year"
         VALUE = "Return to the Calendar">
  </CENTER>
  </BODY>
  </HTML>!;

#########################################################################
#                                SUBROUTINES                            #
#########################################################################

#########################################################################
#                           make_month_array                            #
#########################################################################

sub make_month_array
  {

# Define some variables which will be local to this subroutine

  local($juldate)  = $_[0];
  local($month,$day,$year,$weekday);
  local($tempjdate,$firstweekday,$numdays,$lastweekday);
  local(@myarray);

# The following line gets the date of the passed parameter

  ($month, $day, $year, $weekday) = &jdate($juldate);

# Make a NEW date based on the FIRST of the month instead

  $tempjdate = &jday($month, 1, $year);

# get weekday of 1st of the month

  ($month, $day, $year, $weekday) = &jdate($tempjdate);
  $firstweekday = $weekday;
 
  $currentmonth = "$month";
  $currentyear = "$year";

  $month++; 
  if ($month > 12)
    {
    $month = 1;
    $year++;
    }

  $tempjdate = &jday($month,1,$year);
  $tempjdate--;
  ($month, $day, $year, $weekday) = &jdate($tempjdate);
  $numdays = $day;
  $lastweekday = $weekday;

  for ($x = 0;$x < $firstweekday; $x++)
    {
    $myarray[$x] = " ";
    } #End of for

  for ($x = 1; $x <= $numdays; $x++ )
    {
    $myarray[$x + $firstweekday - 1] = $x;
    }

  for ($x = $lastweekday; $x < 6; $x++)
    {
    push(@myarray,"");
    }
  
  return @myarray;
  }

#########################################################################
#                               &CgiRequire                             #
#########################################################################

# This subroutine checks to see whether the file that we are trying to
# require actually exists and is readable by us.  The reason for this
# subroutine is to provide the developer with an informative error message
# when attempting to debug the scripts.

sub CgiRequire
  {

# Define $require_file as a local variable and set it equal to the
# filename we sent when we called this routine.

  local (@require_files) = @_;

# Check to see if the file exists and is readable by us.  If so, go ahead
# and require it.

  foreach $file (@require_files)
    {
    if (-e "$file" && -r "$file")
      {
      require "$file";
      }

# If not, send back an error message that will help us isolate the
# problem with the script.

    else
      {
      print "I'm sorry, I was not able to open $file.  Would you
             please check to make sure that you gave me a valid filename
             and that the permissions on $require_file are set to allow me
             access?";
      exit;
      }
    }
  }

########################################################################
#                               &select_a_month                        #
########################################################################

  sub select_a_month
    {
    print "<SELECT NAME=\"month\">\n";
    foreach $month (@month_names)
      {
      if ($month ne "$current_month_name")
        {
        print "<OPTION VALUE = \"$MONTH_ARRAY{$month}\">$month\n";
        }
      else
        {
        print "<OPTION SELECTED VALUE = \"$MONTH_ARRAY{$month}\">$month\n";
        }
      }
    print "</SELECT>\n";
    }

######################################################################
#                               &select_a_year                       #
######################################################################

  sub select_a_year
    {
    print "<SELECT NAME = \"year\">\n";

    for ($i = $the_current_year; $i < $greatest_year; $i++)
      {
      if ($i eq "$currentyear")
        {
        print "<OPTION SELECTED VALUE = \"$i\">$i\n";
        }
      else
        {
        print "<OPTION VALUE = \"$i\">$i\n";
        }
      }
    print "</SELECT>\n";
    }

######################################################################
#                              &submission_form                      #
######################################################################
 
  sub submission_form
    {
    local ($type_of_form) = @_;

    if ($session_first_name ne "")
      {
      print qq!
      <TABLE BORDER = "0" CELLSPACING = "2" CELLPADDING = "2">
      <TR ALIGN = "LEFT">
      <TH>Name</TH>
      <TD>$session_first_name $session_last_name</TD>
      <TR ALIGN = "LEFT">
      <TH>Email</TH>
      <TD>$session_email</TD>
      </TR>!;
      }
    else
      {
      print qq!
      <TABLE BORDER = "0" CELLSPACING = "2" CELLPADDING = "2">
      <TR ALIGN = "LEFT">
      <TH>First Name</TH>
      <TD><INPUT TYPE = "text" NAME = "first_name" SIZE = "20"
        MAXLENGTH = "20"></TD>
      </TR>
      <TR ALIGN = "LEFT">
      <TH>Last Name</TH>
      <TD><INPUT TYPE = "text" NAME = "last_name" SIZE = "20"
        MAXLENGTH = "20"></TD>
      </TR>
      <TR ALIGN = "LEFT">
      <TH>Email</TH>
      <TD><INPUT TYPE = "text" NAME = "email" SIZE = "20"
        MAXLENGTH = "20"></TD>
      </TR>!;
      }

    print qq!
    <TR ALIGN = "LEFT">
    <TH>Subject</TH>
    <TD><INPUT TYPE = "text" NAME = "subject" SIZE = "20"
        MAXLENGTH = "20"></TD>
    </TR>
    <TR ALIGN = "LEFT">
    <TH>Year</TH>
    <TD>!;

    &select_a_year;

    print qq!
    </TD>
    </TR>
    <TR ALIGN = "LEFT">
    <TH>Time</TH>
    <TD>
    <SELECT NAME = "time">!;

    if ($type_of_form eq "modify")
      {
      print "<OPTION VALUE = \"\">Don't Change Time\n";
      }

    foreach $time_value (@time_values)
      {
      if ($time_value ne "09:00")
        {
        print "<OPTION VALUE = \"$time_value\">$TIME{$time_value}\n";
        }
      else
        {
        if ($type_of_form ne "modify")
          {
          print "<OPTION SELECTED VALUE = \"$time_value\">$TIME{$time_value}\n";
          }
        }
      }

    print "</SELECT></TD></TR>\n";

    print "<TR>\n<TH>Month</TH>\n";
    print "<TD>\n";
    &select_a_month;
    print "</TD>\n";
    print "</TR>";

    print "<TR ALIGN=LEFT>\n";
    print "<TH>Day</TH>\n";
    print "<TD><SELECT NAME=\"day\">\n";
    for ($i = 1; $i < 32; $i++)
      {
      if ($i eq "$form_data{'day'}")
        {
        print "<OPTION SELECTED VALUE = \"$i\">$i\n";
        }
      else
        {
        print "<OPTION VALUE = \"$i\">$i\n";
        }
      }
    print qq!
    </SELECT></TD>
    </TR>
    <TR ALIGN=LEFT>
    <TH>Body</TH>
    <TD><TEXTAREA WRAP = "virtual" NAME = "body" ROWS = "8"
         COLS = "40"></TEXTAREA></TD>
    </TR>
    </TABLE>!;
    }


  sub header
    {
    local ($title) = @_;
    if ($title eq "")
      {
      $title = "Selena Sol's Groupware Calendar Demo";
      }
    print qq!
    <HTML>
    <HEAD>
    <TITLE>$title</TITLE>
    </HEAD>
    <BODY>
    <FORM METHOD = "post" ACTION = "$this_script_url">
    <INPUT TYPE = "hidden" NAME = "session_file"  VALUE = "$session_file">
    <INPUT TYPE = "hidden" NAME = "calendar" VALUE = "$form_data{'calendar'}">!;
    }
