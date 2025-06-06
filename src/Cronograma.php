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

class Cronograma {

        public static function lerAulasDoArquivo($caminhoArquivo) {
        $aulasArray = [];
        
        if (!file_exists($caminhoArquivo)) {
            return $aulasArray;
        }
        
        $aulas = fopen($caminhoArquivo, 'r');
        
        while(!feof($aulas)) {
            $linha = fgets($aulas);
            if(trim($linha) == '') continue;

            $partes = explode(' - ', $linha);
            if (count($partes) >= 2) {
                $aula = trim($partes[0]);
                $professor = trim($partes[1]);
                $professorNome = explode(' ', $professor)[1];
                preg_match('/(\d+)min/', $partes[1], $hora);

                $aulasArray[] = new Aula($aula, $professorNome, isset($hora[1]) ? $hora[1] : 0);
            }
        }

        fclose($aulas);
        return $aulasArray;
    }

    public static function montarCronograma($aulasArray) {
        $dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'];
        $cronograma = [];
        $aulaIndex = 0;

        foreach ($dias as $dia) {
            $cronograma[] = "📅 $dia";
            $horaAtual = 9;
            $minutoAtual = 0;
            $tempoRestante = 180;

            while ($aulaIndex < count($aulasArray) && $horaAtual < 12) {
                $aula = $aulasArray[$aulaIndex];
                $duracao = intval($aula->hora);

                $minutoFim = $minutoAtual + $duracao;
                $horaFim = $horaAtual;
                if ($minutoFim >= 60) {
                    $horaFim += intval($minutoFim / 60);
                    $minutoFim = $minutoFim % 60;
                }

                if ($horaFim > 12 || ($horaFim == 12 && $minutoFim > 0)) {
                    break;
                }
                
                $tempoRestante -= $duracao;

                if ($tempoRestante >= 0) {
                    $horarioFormatado = sprintf('%02d:%02d', $horaAtual, $minutoAtual);
                    $cronograma[] = "🕘 {$horarioFormatado} - {$aula->aula} ({$aula->professor} {$aula->hora} min)";
                    $minutoAtual += $duracao;
                    if ($minutoAtual >= 60) {
                        $horaAtual += intval($minutoAtual / 60);
                        $minutoAtual = $minutoAtual % 60;
                    }
                    $aulaIndex++;
                } else {
                    break;
                }
            }

            $cronograma[] = "🍽️ 12:00 - Intervalo para Almoço";
            $horaAtual = 13;
            $minutoAtual = 0;
            $tempoRestante = 240;

            while ($aulaIndex < count($aulasArray) && $horaAtual < 17) {
                $aula = $aulasArray[$aulaIndex];
                $duracao = intval($aula->hora);

                $minutoFim = $minutoAtual + $duracao;
                $horaFim = $horaAtual;
                if ($minutoFim >= 60) {
                    $horaFim += intval($minutoFim / 60);
                    $minutoFim = $minutoFim % 60;
                }

                if ($horaFim > 17 || ($horaFim == 17 && $minutoFim > 0)) {
                    break;
                }
                
                $tempoRestante -= $duracao;

                if ($tempoRestante >= 0) {
                    $horarioFormatado = sprintf('%02d:%02d', $horaAtual, $minutoAtual);
                    $cronograma[] = "🕘 {$horarioFormatado} - {$aula->aula} ({$aula->professor} {$aula->hora} min)";
                    $minutoAtual += $duracao;
                    if ($minutoAtual >= 60) {
                        $horaAtual += intval($minutoAtual / 60);
                        $minutoAtual = $minutoAtual % 60;
                    }
                    $aulaIndex++;
                } else {
                    break;
                }
            }

            if ($aulaIndex >= count($aulasArray)) {
                break;
            }

            $horaAtual = 17;

            if ($horaAtual >= 17) {
                $cronograma[] = "🕘 17:00 - Reunião dos Professores";
            }
        }
        
        return $cronograma;
    }
}
