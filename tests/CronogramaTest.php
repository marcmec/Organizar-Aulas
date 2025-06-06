<?php

use PHPUnit\Framework\TestCase;

require_once 'src/Cronograma.php';

class CronogramaTest extends TestCase {
    
    public function testAulaSimples() {
        $aulas = [
            new Aula('Matemática', 'João', 60)
        ];

        $resultado = Cronograma::montarCronograma($aulas);

        $this->assertContains('📅 Segunda-feira', $resultado);
        $this->assertContains('🕘 09:00 - Matemática (João 60 min)', $resultado);
        $this->assertContains('🍽️ 12:00 - Intervalo para Almoço', $resultado);
    }
    
    public function testAulaNaoUltrapassaIntervalo() {
        $aulas = [
            new Aula('Aula Longa', 'Professor', 45)
        ];

        $resultado = Cronograma::montarCronograma($aulas);
        $linhasAntesAlmoco = [];
        foreach ($resultado as $linha) {
            if (strpos($linha, 'Intervalo para Almoço') !== false) {
                break;
            }
            $linhasAntesAlmoco[] = $linha;
        }
        foreach ($linhasAntesAlmoco as $linha) {
            if (preg_match('/🕘 (\d{2}):(\d{2})/', $linha, $matches)) {
                $hora = intval($matches[1]);
                $minuto = intval($matches[2]);
                $this->assertTrue($hora < 12 || ($hora == 12 && $minuto == 0));
            }
        }
    }
    
    public function testMultiplasAulas() {
        $aulas = [
            new Aula('Matemática', 'João', 30),
            new Aula('Português', 'Maria', 45),
            new Aula('História', 'Pedro', 60)
        ];
        
        $resultado = Cronograma::montarCronograma($aulas);
        
        $this->assertContains('🕘 09:00 - Matemática (João 30 min)', $resultado);
        $this->assertContains('🕘 09:30 - Português (Maria 45 min)', $resultado);
        $this->assertContains('🕘 10:15 - História (Pedro 60 min)', $resultado);
    }
    
    public function testArrayVazio() {
        $aulas = [];

        $resultado = Cronograma::montarCronograma($aulas);

        $this->assertContains('📅 Segunda-feira', $resultado);
        $this->assertContains('🍽️ 12:00 - Intervalo para Almoço', $resultado);
    }
    
    public function testLimiteTempoManha() {
        $aulas = [
            new Aula('Aula1', 'Prof1', 180),
            new Aula('Aula2', 'Prof2', 30)  
        ];

        $resultado = Cronograma::montarCronograma($aulas);

        $this->assertContains('🕘 09:00 - Aula1 (Prof1 180 min)', $resultado);
        $this->assertContains('🕘 13:00 - Aula2 (Prof2 30 min)', $resultado);
    }

    public function testCronogramaCompletoDoArquivo() {
        $aulas = Cronograma::lerAulasDoArquivo('aulas.txt');
        $this->assertNotEmpty($aulas, 'Arquivo aulas.txt deve conter aulas');
        
        $resultado = Cronograma::montarCronograma($aulas);
        
        $outputEsperado = [
            '📅 Segunda-feira',
            '🕘 09:00 - Introdução à IA (João 60 min)',
            '🕘 10:00 - Técnicas de Aprendizado Supervisionado (Ana 45 min)',
            '🕘 10:45 - Redes Neurais Convolucionais (João 30 min)',
            '🕘 11:15 - Ética na IA (Carla 5 min)',
            '🍽️ 12:00 - Intervalo para Almoço',
            '🕘 13:00 - Linguagens de Programação Funcionais (Paulo 45 min)',
            '🕘 13:45 - História da Computação (Carla 30 min)',
            '🕘 14:15 - Banco de Dados NoSQL (Ana 60 min)',
            '🕘 15:15 - Lógica Computacional (Paulo 45 min)',
            '🕘 16:00 - Compiladores e Interpretadores (João 60 min)',
            '🕘 17:00 - Reunião dos Professores',
            '📅 Terça-feira',
            '🕘 09:00 - Computação Quântica (Carla 45 min)',
            '🕘 09:45 - Algoritmos Avançados (Ana 60 min)',
            '🕘 10:45 - Programação Paralela (Paulo 30 min)',
            '🕘 11:15 - Pensamento Computacional (Carla 30 min)',
            '🍽️ 12:00 - Intervalo para Almoço'
        ];
        
        $this->assertEquals($outputEsperado, $resultado, 'O cronograma deve corresponder exatamente ao output esperado');
        
        // Verificação adicional para debug
        foreach ($resultado as $index => $linha) {
            echo "Linha $index: $linha\n";
        }
        
        $this->assertCount(count($outputEsperado), $resultado, 'Deve ter exatamente ' . count($outputEsperado) . ' linhas no cronograma');
    }
}