#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asistente IA Forense Mejorado - Integración con Llama 3.1 8B
Proporciona interpretación inteligente de análisis forenses usando IA local
"""

import json
import os
import subprocess
import datetime
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import time
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/ForensicAI/logs/ai_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedForensicAIAssistant:
    """Asistente IA forense mejorado con Llama 3.1 8B"""
    
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.model_name = model_name
        self.is_ollama_available = False
        self.conversation_history = []
        self.current_case_context = None
        
        # Prompts especializados en forense
        self.system_prompts = {
            'forensic_expert': """Eres un experto senior en informática forense con 15 años de experiencia en investigaciones digitales. Tu especialidad incluye:

- Análisis de evidencia digital en casos corporativos
- Interpretación de patrones de comportamiento sospechoso
- Evaluación de riesgo y amenazas internas
- Generación de reportes técnicos para tribunales
- Recomendaciones de investigación forense

INSTRUCCIONES IMPORTANTES:
1. Responde SIEMPRE en español de manera profesional y técnica
2. Basa tus análisis en la evidencia digital proporcionada
3. Proporciona recomendaciones específicas y accionables
4. Usa terminología forense apropiada
5. Mantén objetividad científica en tus conclusiones
6. Considera aspectos legales y de cumplimiento normativo

Contexto: Estás analizando evidencia digital en una investigación corporativa.""",

            'executive_summary': """Eres un consultor forense senior que debe generar resúmenes ejecutivos para directivos y equipos legales. 

Tu tarea: Crear un resumen claro, conciso y profesional que explique:
- Los hallazgos más importantes
- El nivel de riesgo para la organización
- Las implicaciones legales y de negocio
- Las acciones inmediatas recomendadas

Responde en español con un lenguaje profesional pero accesible para no-técnicos.""",

            'technical_analysis': """Eres un analista forense técnico especializado en interpretación detallada de evidencia digital.

Enfócate en:
- Análisis técnico profundo de los datos
- Correlación de eventos y patrones
- Metodologías forenses aplicadas
- Validez técnica de la evidencia
- Recomendaciones técnicas específicas

Responde en español con terminología técnica precisa.""",

            'legal_compliance': """Eres un especialista en cumplimiento legal y normativo en investigaciones forenses digitales.

Considera:
- Aspectos de protección de datos (GDPR, CCPA)
- Cadena de custodia de evidencia
- Admisibilidad legal de la evidencia
- Recomendaciones de compliance
- Riesgos legales y regulatorios

Responde en español con enfoque en aspectos legales y normativos."""
        }
        
        # Verificar disponibilidad de Ollama
        self._check_ollama_availability()

    def _check_ollama_availability(self) -> bool:
        """Verifica si Ollama está disponible y el modelo está descargado"""
        try:
            # Verificar que Ollama esté instalado
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                logger.error("Ollama no está instalado o no responde")
                return False
            
            # Verificar que el modelo esté disponible
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            if self.model_name not in result.stdout:
                logger.warning(f"Modelo {self.model_name} no encontrado. Intentando descargarlo...")
                self._download_model()
            
            self.is_ollama_available = True
            logger.info(f"Ollama y modelo {self.model_name} disponibles")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout al verificar Ollama")
            return False
        except FileNotFoundError:
            logger.error("Ollama no está instalado en el sistema")
            return False
        except Exception as e:
            logger.error(f"Error verificando Ollama: {e}")
            return False

    def _download_model(self) -> bool:
        """Descarga el modelo Llama 3.1 8B si no está disponible"""
        try:
            logger.info(f"Descargando modelo {self.model_name}... (esto puede tomar varios minutos)")
            
            # Ejecutar descarga en hilo separado para no bloquear
            def download_thread():
                subprocess.run(['ollama', 'pull', self.model_name], 
                             capture_output=True, text=True, timeout=1800)  # 30 min timeout
            
            thread = threading.Thread(target=download_thread)
            thread.start()
            thread.join(timeout=1800)  # 30 minutos máximo
            
            if thread.is_alive():
                logger.error("Timeout descargando modelo")
                return False
            
            logger.info(f"Modelo {self.model_name} descargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error descargando modelo: {e}")
            return False

    def _call_ollama(self, prompt: str, system_prompt: str = None, 
                    temperature: float = 0.1, max_tokens: int = 4096) -> str:
        """Realiza llamada a Ollama con manejo de errores mejorado"""
        if not self.is_ollama_available:
            return "Error: IA no disponible. Verificar instalación de Ollama."
        
        try:
            # Preparar el prompt completo
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nPregunta del usuario: {prompt}"
            
            # Configurar parámetros del modelo
            model_params = {
                'temperature': temperature,
                'num_predict': max_tokens,
                'top_k': 40,
                'top_p': 0.9
            }
            
            # Preparar comando
            cmd = ['ollama', 'run', self.model_name]
            
            # Ejecutar consulta con timeout
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            stdout, stderr = process.communicate(input=full_prompt, timeout=120)
            
            if process.returncode != 0:
                logger.error(f"Error en Ollama: {stderr}")
                return f"Error en IA: {stderr[:200]}..."
            
            # Limpiar respuesta
            response = stdout.strip()
            if not response:
                return "Error: La IA no generó respuesta."
            
            # Registrar en historial
            self.conversation_history.append({
                'timestamp': datetime.datetime.now().isoformat(),
                'prompt': prompt,
                'response': response,
                'model': self.model_name
            })
            
            logger.info(f"Respuesta de IA generada exitosamente ({len(response)} caracteres)")
            return response
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout en consulta a IA")
            return "Error: Timeout - La consulta tardó demasiado tiempo."
        except Exception as e:
            logger.error(f"Error en llamada a IA: {e}")
            return f"Error inesperado en IA: {str(e)[:200]}..."

    def load_case_context(self, case_file_path: str) -> bool:
        """Carga el contexto de un caso para análisis"""
        try:
            with open(case_file_path, 'r', encoding='utf-8') as f:
                self.current_case_context = json.load(f)
            
            logger.info(f"Contexto de caso cargado: {self.current_case_context.get('case_id', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando contexto del caso: {e}")
            return False

    def generate_executive_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Genera resumen ejecutivo usando IA"""
        logger.info("Generando resumen ejecutivo con IA...")
        
        # Preparar datos del análisis para la IA
        case_info = analysis_result.get('case_info', {})
        summary = analysis_result.get('summary', {})
        risk_assessment = analysis_result.get('risk_assessment', {})
        
        prompt = f"""
ANÁLISIS FORENSE DIGITAL - RESUMEN EJECUTIVO

INFORMACIÓN DEL CASO:
- ID del Caso: {case_info.get('case_id')}
- Tipo de Investigación: {case_info.get('case_type', '').replace('_', ' ').title()}
- Sospechoso: {case_info.get('suspect_name')}
- Fecha de Análisis: {case_info.get('analysis_timestamp')}

ESTADÍSTICAS CLAVE:
- Archivos Analizados: {summary.get('total_files_analyzed', 0)}
- Archivos Sospechosos: {summary.get('suspicious_files_found', 0)}
- Conexiones de Red: {summary.get('total_network_connections', 0)}
- Conexiones Sospechosas: {summary.get('suspicious_connections_found', 0)}

EVALUACIÓN DE RIESGO:
- Nivel de Riesgo: {risk_assessment.get('risk_level')}
- Puntuación: {risk_assessment.get('overall_risk_score')}/100
- Confianza: {risk_assessment.get('confidence_level')}

FACTORES DE RIESGO DETECTADOS:
"""
        
        for i, factor in enumerate(risk_assessment.get('risk_factors', []), 1):
            prompt += f"{i}. {factor}\n"
        
        prompt += """
INSTRUCCIONES:
Genera un resumen ejecutivo profesional para directivos que incluya:
1. Evaluación del riesgo para la organización
2. Principales hallazgos críticos
3. Implicaciones de negocio y legales
4. Recomendaciones inmediatas prioritarias
5. Próximos pasos sugeridos

El resumen debe ser claro, conciso y enfocado en decisiones ejecutivas.
        """
        
        return self._call_ollama(prompt, self.system_prompts['executive_summary'])

    def analyze_temporal_patterns(self, analysis_result: Dict[str, Any]) -> str:
        """Analiza patrones temporales usando IA"""
        logger.info("Analizando patrones temporales con IA...")
        
        file_analysis = analysis_result.get('file_analysis', {})
        network_analysis = analysis_result.get('network_analysis', {})
        
        prompt = f"""
ANÁLISIS DE PATRONES TEMPORALES

ACTIVIDAD DE ARCHIVOS:
- Eventos fuera de horario: {file_analysis.get('after_hours_activity', 0)}
- Distribución horaria: {file_analysis.get('hourly_distribution', {})}

ACTIVIDAD DE RED:
- Conexiones fuera de horario: {network_analysis.get('after_hours_connections', 0)}
- Distribución horaria de red: {network_analysis.get('hourly_distribution', {})}

INSTRUCCIONES:
Analiza estos patrones temporales y proporciona:
1. Interpretación del comportamiento temporal anómalo
2. Significancia forense de la actividad fuera de horario
3. Correlación entre actividad de archivos y red
4. Posibles explicaciones para estos patrones
5. Recomendaciones para investigación adicional

Enfócate en el aspecto forense y las implicaciones de estos patrones temporales.
        """
        
        return self._call_ollama(prompt, self.system_prompts['technical_analysis'])

    def analyze_network_behavior(self, analysis_result: Dict[str, Any]) -> str:
        """Analiza comportamiento de red usando IA"""
        logger.info("Analizando comportamiento de red con IA...")
        
        network_analysis = analysis_result.get('network_analysis', {})
        
        prompt = f"""
ANÁLISIS DE COMPORTAMIENTO DE RED

ESTADÍSTICAS DE CONEXIONES:
- Total de conexiones: {network_analysis.get('total_connections', 0)}
- Conexiones sospechosas: {network_analysis.get('suspicious_connections', 0)}
- Transferencias grandes: {network_analysis.get('large_transfers_count', 0)}
- Servicios en la nube: {network_analysis.get('cloud_services_count', 0)}

DISTRIBUCIÓN DE DESTINOS:
{network_analysis.get('destinations_distribution', {})}

DISTRIBUCIÓN DE PUERTOS:
{network_analysis.get('ports_distribution', {})}

DISTRIBUCIÓN DE PROTOCOLOS:
{network_analysis.get('protocols_distribution', {})}

INSTRUCCIONES:
Analiza este comportamiento de red y proporciona:
1. Evaluación de amenazas en las conexiones detectadas
2. Análisis de patrones de exfiltración de datos
3. Identificación de actividad maliciosa potencial
4. Evaluación del uso de servicios en la nube
5. Recomendaciones técnicas específicas para la investigación

Enfócate en aspectos de ciberseguridad e investigación forense.
        """
        
        return self._call_ollama(prompt, self.system_prompts['technical_analysis'])

    def generate_recommendations(self, analysis_result: Dict[str, Any]) -> str:
        """Genera recomendaciones específicas usando IA"""
        logger.info("Generando recomendaciones con IA...")
        
        risk_assessment = analysis_result.get('risk_assessment', {})
        threat_categories = risk_assessment.get('threat_categories', {})
        
        prompt = f"""
GENERACIÓN DE RECOMENDACIONES FORENSES

NIVEL DE RIESGO: {risk_assessment.get('risk_level')} ({risk_assessment.get('overall_risk_score')}/100)

CATEGORÍAS DE AMENAZAS DETECTADAS:
- Exfiltración de datos: {threat_categories.get('data_exfiltration', 0)} indicadores
- Destrucción de evidencia: {threat_categories.get('evidence_destruction', 0)} indicadores
- Acceso no autorizado: {threat_categories.get('unauthorized_access', 0)} indicadores
- Amenaza interna: {threat_categories.get('insider_threat', 0)} indicadores

FACTORES DE RIESGO:
"""
        
        for factor in risk_assessment.get('risk_factors', []):
            prompt += f"- {factor}\n"
        
        prompt += """
INSTRUCCIONES:
Genera recomendaciones específicas y priorizadas que incluyan:

ACCIONES INMEDIATAS (próximas 24-48 horas):
1. Medidas de preservación de evidencia
2. Acciones de contención de riesgos
3. Pasos críticos de investigación

ACCIONES A MEDIANO PLAZO (próximas 1-2 semanas):
1. Investigación forense detallada
2. Entrevistas y procedimientos legales
3. Análisis técnico profundo

ACCIONES PREVENTIVAS A LARGO PLAZO:
1. Mejoras en controles de seguridad
2. Políticas y procedimientos
3. Monitoreo y detección

Cada recomendación debe ser específica, accionable y justificada técnicamente.
        """
        
        return self._call_ollama(prompt, self.system_prompts['forensic_expert'])

    def generate_narrative_report(self, analysis_result: Dict[str, Any]) -> str:
        """Genera reporte narrativo completo usando IA"""
        logger.info("Generando reporte narrativo completo con IA...")
        
        case_info = analysis_result.get('case_info', {})
        summary = analysis_result.get('summary', {})
        risk_assessment = analysis_result.get('risk_assessment', {})
        
        prompt = f"""
GENERACIÓN DE REPORTE NARRATIVO FORENSE

CASO: {case_info.get('case_id')}
TIPO: {case_info.get('case_type', '').replace('_', ' ').title()}
SOSPECHOSO: {case_info.get('suspect_name')}

EVIDENCIA ANALIZADA:
- {summary.get('total_files_analyzed', 0)} archivos digitales
- {summary.get('total_network_connections', 0)} conexiones de red
- Nivel de riesgo: {risk_assessment.get('risk_level')} ({risk_assessment.get('overall_risk_score')}/100)

HALLAZGOS PRINCIPALES:
- {summary.get('suspicious_files_found', 0)} archivos sospechosos identificados
- {summary.get('suspicious_connections_found', 0)} conexiones de red anómalas
- Confianza en el análisis: {risk_assessment.get('confidence_level')}

INSTRUCCIONES:
Genera un reporte narrativo profesional estilo pericial que incluya:

1. INTRODUCCIÓN Y METODOLOGÍA
2. DESCRIPCIÓN DE LA EVIDENCIA ANALIZADA
3. HALLAZGOS TÉCNICOS DETALLADOS
4. ANÁLISIS E INTERPRETACIÓN DE EVIDENCIA
5. CONCLUSIONES Y OPINIÓN TÉCNICA
6. LIMITACIONES DEL ANÁLISIS

El reporte debe ser:
- Técnicamente preciso y detallado
- Apropiado para uso judicial
- Redactado en español formal
- Estructurado y profesional
- Basado únicamente en la evidencia analizada

Incluye referencias a metodologías forenses estándar y mantén objetividad científica.
        """
        
        return self._call_ollama(prompt, self.system_prompts['legal_compliance'], temperature=0.05)

    def answer_custom_question(self, question: str, analysis_result: Dict[str, Any] = None) -> str:
        """Responde preguntas personalizadas sobre el caso"""
        logger.info(f"Respondiendo pregunta personalizada: {question[:50]}...")
        
        context = ""
        if analysis_result:
            case_info = analysis_result.get('case_info', {})
            summary = analysis_result.get('summary', {})
            
            context = f"""
CONTEXTO DEL CASO ACTUAL:
- Caso: {case_info.get('case_id')}
- Sospechoso: {case_info.get('suspect_name')}
- Archivos analizados: {summary.get('total_files_analyzed', 0)}
- Archivos sospechosos: {summary.get('suspicious_files_found', 0)}
- Conexiones de red: {summary.get('total_network_connections', 0)}
- Nivel de riesgo: {analysis_result.get('risk_assessment', {}).get('risk_level')}

"""
        
        prompt = f"""
{context}

PREGUNTA DEL USUARIO: {question}

INSTRUCCIONES:
Responde la pregunta basándote en:
1. Tu experiencia en informática forense
2. El contexto del caso actual (si está disponible)
3. Mejores prácticas en investigación digital
4. Consideraciones legales y técnicas relevantes

Proporciona una respuesta detallada, técnica y profesional en español.
        """
        
        return self._call_ollama(prompt, self.system_prompts['forensic_expert'])

    def get_case_insights(self, analysis_result: Dict[str, Any]) -> Dict[str, str]:
        """Obtiene insights completos del caso usando IA"""
        logger.info("Generando insights completos del caso...")
        
        insights = {}
        
        try:
            # Generar diferentes tipos de análisis
            insights['executive_summary'] = self.generate_executive_summary(analysis_result)
            insights['temporal_analysis'] = self.analyze_temporal_patterns(analysis_result)
            insights['network_analysis'] = self.analyze_network_behavior(analysis_result)
            insights['recommendations'] = self.generate_recommendations(analysis_result)
            
            logger.info("Insights completos generados exitosamente")
            
        except Exception as e:
            logger.error(f"Error generando insights: {e}")
            insights['error'] = f"Error generando análisis IA: {str(e)}"
        
        return insights

    def save_ai_analysis(self, insights: Dict[str, str], case_id: str, 
                        output_dir: str = "C:/ForensicAI/reportes") -> str:
        """Guarda el análisis de IA en archivo"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{case_id}_ai_analysis.json"
        filepath = os.path.join(output_dir, filename)
        
        ai_report = {
            'case_id': case_id,
            'analysis_timestamp': datetime.datetime.now().isoformat(),
            'model_used': self.model_name,
            'insights': insights,
            'conversation_history': self.conversation_history
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(ai_report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Análisis de IA guardado en: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error guardando análisis de IA: {e}")
            raise

def main():
    """Función principal para demostrar el asistente IA"""
    print("🤖 ASISTENTE IA FORENSE MEJORADO")
    print("=" * 50)
    
    # Inicializar asistente
    assistant = EnhancedForensicAIAssistant()
    
    if not assistant.is_ollama_available:
        print("❌ Ollama no está disponible.")
        print("   Instala Ollama y el modelo llama3.1:8b")
        return
    
    print(f"✅ IA inicializada con modelo: {assistant.model_name}")
    
    # Buscar análisis disponibles
    reports_dir = "C:/ForensicAI/reportes"
    
    if not os.path.exists(reports_dir):
        print("❌ No se encontraron reportes para analizar.")
        print("   Ejecuta primero: python forensic_analyzer.py")
        return
    
    analysis_files = [f for f in os.listdir(reports_dir) if f.endswith('_analysis_report.json')]
    
    if not analysis_files:
        print("❌ No se encontraron reportes de análisis.")
        return
    
    # Cargar el primer análisis disponible
    analysis_file = os.path.join(reports_dir, analysis_files[0])
    
    print(f"📋 Analizando con IA: {analysis_files[0]}")
    print("-" * 50)
    
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_result = json.load(f)
        
        case_id = analysis_result['case_info']['case_id']
        
        print(f"🔄 Generando análisis IA para caso: {case_id}")
        
        # Generar insights completos
        insights = assistant.get_case_insights(analysis_result)
        
        # Mostrar resumen ejecutivo
        if 'executive_summary' in insights:
            print(f"\n📊 RESUMEN EJECUTIVO (IA):")
            print("-" * 50)
            print(insights['executive_summary'][:500] + "..." if len(insights['executive_summary']) > 500 else insights['executive_summary'])
        
        # Guardar análisis completo
        ai_report_file = assistant.save_ai_analysis(insights, case_id)
        
        print(f"\n💾 Análisis IA completo guardado en:")
        print(f"   {ai_report_file}")
        
        # Ofrecer consulta interactiva
        print(f"\n💬 ¿Deseas hacer una consulta personalizada? (s/n): ", end="")
        response = input().lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            print(f"\n🤖 Modo consulta interactiva activado")
            print(f"Escribe 'salir' para terminar\n")
            
            while True:
                question = input("❓ Tu pregunta: ").strip()
                
                if question.lower() in ['salir', 'exit', 'quit']:
                    break
                
                if not question:
                    continue
                
                print(f"\n🔄 Consultando IA...")
                answer = assistant.answer_custom_question(question, analysis_result)
                print(f"\n🤖 Respuesta:")
                print(f"{answer}\n")
                print("-" * 50)
        
        print(f"\n🎉 ¡Análisis IA completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante el análisis IA: {e}")
        logger.error(f"Error en main: {e}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")