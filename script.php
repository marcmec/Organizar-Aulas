<?php 

class Aula {
    public $aula;
    public $professor;
    public $hora;

    public function __construct($aula, $professor, $hora) {
        $this->aula = $aula;
        $this->professor = $professor;
        $this->hora = $hora;
    }
}

$aulas = fopen('aulas.txt', 'r');
$aulasArray = [];

while(!feof($aulas)) {
    $linha = fgets($aulas);
    if(trim($linha) == '') continue; // Pula linhas vazias
    
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

function montarCronograma($aulasArray) {
    $dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'];
    $cronograma = [];
    
    $aulaIndex = 0;
    
    foreach ($dias as $dia) {
        $cronograma[] = "📅 $dia:";
        
        $horaAtual = 9;
        $minutoAtual = 0;
        
        while ($horaAtual < 12 && $aulaIndex < count($aulasArray)) {
            $aula = $aulasArray[$aulaIndex];
            $duracao = intval($aula->hora);
            
            // Verificar se a aula cabe no período restante
            $minutosRestantes = (12 - $horaAtual) * 60 - $minutoAtual;
            if ($duracao > $minutosRestantes) {
                break; // Não cabe mais aulas na manhã
            }
            
            $horarioFormatado = sprintf("%02d:%02d", $horaAtual, $minutoAtual);
            $cronograma[] = "$horarioFormatado {$aula->aula} - Prof. {$aula->professor} {$aula->hora}min";
            
            // Calcular próximo horário
            $minutoAtual += $duracao;
            while ($minutoAtual >= 60) {
                $horaAtual++;
                $minutoAtual -= 60;
            }
            
            $aulaIndex++;
        }

        
        // Período da tarde (13:00 - 17:00)
        $horaAtual = 13;
        $minutoAtual = 0;
        
        while ($horaAtual < 17 && $aulaIndex < count($aulasArray)) {
            $aula = $aulasArray[$aulaIndex];
            $duracao = intval($aula->hora);
            
            // Verificar se a aula cabe no período restante
            $minutosRestantes = (17 - $horaAtual) * 60 - $minutoAtual;
            if ($duracao > $minutosRestantes) {
                break; // Não cabe mais aulas na tarde
            }
            
            $horarioFormatado = sprintf("%02d:%02d", $horaAtual, $minutoAtual);
            $cronograma[] = "$horarioFormatado {$aula->aula} - Prof. {$aula->professor} {$aula->hora}min";
            
            // Calcular próximo horário
            $minutoAtual += $duracao;
            while ($minutoAtual >= 60) {
                $horaAtual++;
                $minutoAtual -= 60;
            }
            
            $aulaIndex++;
        }
        
        // Se não há aulas na tarde
        if ($horaAtual == 13 && $minutoAtual == 0) {
            $cronograma[] = "13:00 (sem aulas disponíveis)";
        }
        
        // Reunião dos professores
        $cronograma[] = "17:00 Reunião de Professores";
        $cronograma[] = ""; // Linha vazia entre dias
    }
    
    return $cronograma;
}

// Gerar e exibir o cronograma
$cronograma = montarCronograma($aulasArray);
foreach ($cronograma as $linha) {
    echo $linha . "\n";
}