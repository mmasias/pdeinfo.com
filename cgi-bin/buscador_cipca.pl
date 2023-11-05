#!/usr/local/bin/perl
#---------------------------------------------------
#--->>>Revisado por Manolo 09:25 p.m. 23/12/99<<<---
#---------------------------------------------------
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
open(MYFILE,"datos.txt");
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
print("<HEAD><TITLE>Resultados</TITLE></HEAD>\n");
print("<body background='/curriculos/_themes/sumipntg/sumtextb.jpg' bgcolor='#FFFFCC' text='#000066' link='#660099' vlink='#993366' alink='#6666CC'><font face='Verdana, Arial, Helvetica'>");
print("<p align='center'><img src='/curriculos/_derived/consulta.htm_cmp_sumipntg110_bnr.gif' width='600' height='60' border='0' alt='Consultas'></p>");
print("<p align='center'><img src='/curriculos/_themes/sumipntg/sumhorsa.gif' width='600' height='10'></p>");

if($k==0) {
	print "No hay respuesta a la consulta <b>$keys</b>";
	} else {
print "Respuesta a la consulta <b>$keys</b><P>";
foreach (@found){
		@campos = split(/\^/,$found[$n]);
		print "* <A HREF='-'>$campos[2]</A><BR>";
		$n = $n +1;
	}

}

print("<HR><p align='center'>Sistema desarrolaldo por <a href='http://pdeinfo.com' target='_blank'>Punto de Información</a></p>");
print("</blockquote></body>");
