#!usr/local/bin/perl
read(STDIN,$input,$ENV{CONTENT_LENGTH});
@tmp= split("&",$input); 
foreach(@tmp) {
    ($name,$value)= split("=", $_);
    $name  =~   s/%(..)/pack("c",hex($1))/ge;
    $value =~   s/%(..)/pack("c",hex($1))/ge;
    $fields{$name}=$value;
#Tratamiento de los datos
#------------------------
	if ($name eq "apellidos_y_nombres") {$_ = $value;s/\+/ /g;$apellidos_y_nombres = $_;}
	if ($name eq "login") {$_ = $value;s/\+/ /g;$login = $_;}
	if ($name eq "paswd") {$_ = $value;s/\+/ /g;$paswd = $_;}
	if ($name eq "direccion_actual") {$_ = $value;s/\+/ /g;$direccion_actual = $_;}
	if ($name eq "telefono") {$_ = $value;s/\+/ /g;$telefono = $_;}
	if ($name eq "correo_electronico") {$_ = $value;s/\+/ /g;$correo_electronico = $_;}
	if ($name eq "lugar_y_fecha_de_nacimiento") {$_ = $value;s/\+/ /g;$lugar_y_fecha_de_nacimiento = $_;}
	if ($name eq "documento_de_identidad") {$_ = $value;s/\+/ /g;$documento_de_identidad = $_;}
	if ($name eq "primaria") {$_ = $value;s/\+/ /g;$primaria = $_;}
	if ($name eq "secundaria") {$_ = $value;s/\+/ /g;$secundaria = $_;}
	if ($name eq "superior") {$_ = $value;s/\+/ /g;$superior = $_;}
	if ($name eq "otros_estudios") 
		{@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$otros_estudios=$otros_estudios.$_."<br>";
		}}

	if ($name eq "lengua_nativa") {$_ = $value;s/\+/ /g;$lengua_nativa = $_;}
	if ($name eq "idioma_1") {$_ = $value;s/\+/ /g;$idioma_1 = $_;}	
	if ($name eq "idioma_2") {$_ = $value;s/\+/ /g;$idioma_2 = $_;}	
	if ($name eq "otro_idioma") {$_ = $value;s/\+/ /g;$otro_idioma = $_;}	

	if ($name eq "cursos_y_seminarios") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$cursos_y_seminarios=$cursos_y_seminarios.$_."<br>";
		}}

	if ($name eq "experiencia_laboral") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$experiencia_laboral=$experiencia_laboral.$_."<br>";
		}}

	if ($name eq "software_que_maneja") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$software_que_maneja=$software_que_maneja.$_."<br>";
		}}

	if ($name eq "hobbies") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$hobbies=$hobbies.$_."<br>";
		}}
	
	if ($name eq "intereses_profesionales") {
		@t=split(/=/,$_);
		$hlov=@t[1];
		@lista=split(/%0D%0A/,$hlov);
		foreach (@lista) {
			s/%(..)/pack("c",hex($1))/ge;
			s/\+/ /g;
			$intereses_profesionales=$intereses_profesionales.$_."<br>";
		}}	
}

#------------------
# Rutina principal
#------------------
if (@tmp[2] eq "situacion=nuevo_curriculo"){
	open(Farch,">>curri.bd");
	print Farch "$login^$paswd^$apellidos_y_nombres^$direccion_actual^$telefono^$correo_electronico^$lugar_y_fecha_de_nacimiento^$documento_de_identidad^$primaria^$secundaria^$superior^$otros_estudios^$lengua_nativa^$idioma_1^$idioma_2^$otro_idioma^$experiencia_laboral^$cursos_y_seminarios^$software_que_maneja^$hobbies^$intereses_profesionales\n";
	close(Farch);
	print "Sus datos han sido ingresados con éxito en nuestra base de datos"
}

#--------------------------------
# Rutina de edicion de currículo
#--------------------------------
if (@tmp[0] eq "situacion=edita_curriculo"){
	open(ESCR,">tamp.dat");
	open(Farch,"curri.bd");
	while(<Farch>) {
	 $linea=$_;
	 @lista=split(/\^/,$_);
         if (@lista[0] eq $login ) {
          print ESCR "$login^@lista[1]^$apellidos_y_nombres^$direccion_actual^$telefono^$correo_electronico^$lugar_y_fecha_de_nacimiento^$documento_de_identidad^$primaria^$secundaria^$superior^$otros_estudios^$lengua_nativa^$idioma_1^$idioma_2^$otro_idioma^$experiencia_laboral^$cursos_y_seminarios^$software_que_maneja^$hobbies^$intereses_profesionales\n";
	}
	else {
         print ESCR $linea;
        } 
 
 }
 close(Farch);
 close(ESCR);
 unlink "curri.bd";
 rename("tamp.dat","curri.bd");
 print "Datos Actualizados"
}

