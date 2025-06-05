<?php 

$aulas =  fopen('aulas.txt', 'a+');

while(!feof($aulas)) {
    $linha = fgets($aulas);
    $partes = explode('-', $linha);
    if (count($partes) >= 2) {
        $aula = trim($partes[0]);
        $professor = trim($partes[1]);
        if (preg_match('/([0-9]+)/', $professor, $hora)) {
            echo "$hora[0]\n";
        }
    } else {
        echo "Linha inválida: $linha\n";
    }
}
