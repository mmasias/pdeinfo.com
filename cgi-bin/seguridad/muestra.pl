#!/usr/local/bin/perl
read(STDIN, $save_string, $ENV{CONTENT_LENGTH});  # Yes- Use it
# separa la cadena de caracteres en una lista
@prompts = split(/&/,$save_string);
# recorre la lista
foreach (@prompts) {
    # separa el par nombre=valor
    ($name,$value) = split(/=/,$_);
    # descodifica los valores
    $name =~   s/\%(..)/pack("c",hex($1))/ge;
    $value =~  s/\%(..)/pack("c",hex($1))/ge;
    # uniformización de las claves de búsqueda transformando todos los caracteres a minúsculas
    $value =~  tr/a-z/A-Z/;
    # crea una lista asociativa     
    $fields{$name}=$value;
}
# crea una variable con las palabras clave buscadas
$keys = $fields{'busca'};

# separa las palabras clave, el código del símbolo + es 20
@search_key = split(/\x20/,$keys);
$k =0;
# accede al archivo que contiene el anuario
open(MYFILE,"curri.bd");
while(<MYFILE>) {
    # accede a cada elemento del anuario
    $in_line = $_;
    $in_line_m = $in_line;
    $in_line_m =~  tr/a-z/A-Z/; 
    $found = "yes";      
    
    foreach (@search_key) {
        # busca la clave en el elemento del anuario
        $pos_out = rindex($in_line_m,$_);
        if ($pos_out < 0) {
            $found = "no"; 
        }        
    }
    if ($found eq "yes") {
        $found[$k] = $in_line;
        $k = $k + 1;
    }
}
close(MYFILE);

# cabecera HTTP
print("Content-Type: text/html\n\n");
# Generación del documento HTML    
print("<HEAD><TITLE>Resultados</TITLE></HEAD>\n");
print("<BODY>\n");
print <<"HEADFORM";
HEADFORM
print "<HR>";
if($k==0) {
	print "<b>No hay respuesta a la consulta  $keys</b>";
	} else {

foreach (@found){
		print $found[$n];
		$n = $n +1;
	}

}

