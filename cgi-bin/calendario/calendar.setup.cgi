  $lib = "./Library";
  $this_script_url = "calendario.cgi";
  $the_current_year = "1999";
  $greatest_year = "2020";

# ------------------
# Could be important
# ------------------
  $database_file = "./Databases/$calendar_type/calendar.events";
# -------------------------
# End of Could be important
# -------------------------

  $counter_file = "./Databases/$calendar_type/calendar.counter";
  $temp_file = "./Databases/$calendar_type/calendar_temp.file";
  $lock_file = "./Databases/$calendar_type/calendar_lock.file";

  $auth_lib = "$lib";
  $auth_server =                  "off";
  $auth_cgi =                     "on";

  $auth_user_file =    "./Databases/$calendar_type/calendar.users";
  $auth_alt_user_file =           "";
  $auth_default_group =           "user";
  $auth_add_register =            "on";
  $auth_email_register =          "on";

  $auth_admin_from_address =      "calendario\@pdeinfo.com";
  $auth_admin_email_address =     "calendario\@pdeinfo.com";
  $auth_session_length = 2;
  $auth_session_dir = "./Calendar_session_files";
  $auth_register_message = "Gracias. Ud. puede ahora ingresar con su nombre de usuario y su contraseña.";

  $auth_allow_register =          "on";
  $auth_allow_search =            "on";
  $auth_generate_password =       "off";
  $auth_check_duplicates =        "on";
  $auth_password_message =
        "Su contraseña es:";
  @auth_extra_fields = ("auth_first_name",
                      "auth_last_name",
                      "auth_email");
  @auth_extra_desc = ("First Name",
                    "Last Name",
                    "Email");

  @day_names = ("Domingo", "Lunes", "Martes", "Miercoles", "Jueves",
                "Viernes", "Sabado");

  @month_names = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
                  "Diciembre");

  %MONTH_ARRAY = ('Enero', '1',         'Febrero', '2',
                  'Marzo', '3',         'Abril', '4',
                  'Mayo', '5',           'Junio', '6',
                  'Julio', '7',          'Agosto', '8',
                  'Septiembre', '9',     'Octubre', '10',
                  'Noviembre', '11',     'Diciembre', '12');

  %TIME = ('01:00', '1 AM',     '02:00', '2 AM',        '03:00', '3 AM',
           '04:00', '4 AM',     '05:00', '5 AM',        '06:00', '6 AM',
           '07:00', '7 AM',     '08:00', '8 AM',        '09:00', '9 AM',
           '10:00', '10 AM',    '11:00', '11 AM',       '12:00', '12 del mediodía',
           '13:00', '1 PM',     '14:00', '2 PM',        '15:00', '3 PM',
           '16:00', '4 PM',     '17:00', '5 PM',        '18:00', '6 PM',
           '19:00', '7 PM',     '20:00', '8 PM',        '21:00', '9 PM',
           '22:00', '10 PM',    '23:00', '11 PM',       '24:00',
           '12 de la medianoche');

  @time_values = ("01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
                  "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
                  "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
                  "19:00", "20:00", "21:00", "22:00", "23:00", "24:00");

  %FIELD_ARRAY = ('Day', 'day',
                  'Month', 'month',
                  'Year', 'year',
                  'Username', 'username',
                  'First Name', 'first_name',
                  'Last Name', 'last_name',
                  'Email Address', 'email',
                  'Subject', 'subject',
                  'Event Time', 'time',
                  'Body', 'body',
                  'Database Id Number', 'databse_id_number');

  @field_names = ("Day", "Month", "Year", "Username", "First Name",
                  "Last Name", "Email Address", "Subject", "Event Time",
                  "Body", "Database Id Number");

  @field_values = ("day", "month", "year", "username", "first_name",
                   "last_name", "email", "subject", "time", "body",
                   "databse_id_number");
$index_of_username = 3;
$index_of_first_name = 4;
$index_of_last_name = 5;
$index_of_email = 6;
$field_num_time = "8";

