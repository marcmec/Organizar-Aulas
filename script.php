<?php
require_once 'src/Cronograma.php';

$aulas = fopen('aulasscript.txt', 'r');
$aulasArray = [];

while(!feof($aulas)) {
    $linha = fgets($aulas);
    if(trim($linha) == '') continue;

    $partes = explode('-', $linha);
    if (count($partes) >= 2) {
        $aula = trim($partes[0]);
        $professor = trim($partes[1]);
        $professorNome = explode(' ', $professor)[1];
        preg_match('/[0-9]+/', $partes[1], $hora);

        $aulasArray[] = new Aula($aula, $professorNome, isset($hora[0]) ? $hora[0] : 0);
    }
}

fclose($aulas);

$cronograma = Cronograma::montarCronograma($aulasArray);
foreach ($cronograma as $linha) {
    echo $linha . "\n";
}
?>