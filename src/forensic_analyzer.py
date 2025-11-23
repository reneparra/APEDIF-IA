#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Análisis Forense Mejorado - Asistente Forense IA
Analiza casos forenses y genera reportes detallados con evaluación de riesgo
"""

import json
import os
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter, defaultdict
import numpy as np

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/ForensicAI/logs/analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurar matplotlib para evitar problemas de display
plt.style.use('default')
sns.set_palette("husl")

class EnhancedForensicAnalyzer:
    """Analizador forense mejorado con capacidades avanzadas"""
    
    def __init__(self):
        self.analysis_results = {}
        self.threat_patterns = {
            'data_exfiltration': [
                'large_file_transfers', 'cloud_uploads', 'external_storage'
            ],
            'evidence_destruction': [
                'ccleaner', 'bleachbit', 'eraser', 'secure_delete'
            ],
            'unauthorized_access': [
                'privilege_escalation', 'credential_theft', 'backdoor'
            ],
            'insider_threat': [
                'after_hours_activity', 'unusual_file_access', 'policy_violation'
            ]
        }
        
        self.risk_thresholds = {
            'file_count_suspicious': 5,
            'network_connections_suspicious': 3,
            'after_hours_threshold': 10,
            'large_transfer_size': 50 * 1024 * 1024,  # 50MB
            'critical_risk_score': 80
        }

    def load_case(self, case_file_path: str) -> Dict[str, Any]:
        """Carga un caso desde archivo JSON"""
        try:
            with open(case_file_path, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
            
            logger.info(f"Caso cargado: {case_data.get('case_id', 'Unknown')}")
            return case_data
        
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {case_file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado cargando caso: {e}")
            raise

    def analyze_file_system(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análisis avanzado del sistema de archivos"""
        logger.info("Iniciando análisis del sistema de archivos...")
        
        # Estadísticas básicas
        total_files = len(files)
        suspicious_files = [f for f in files if f.get('is_suspicious', False)]
        
        # Análisis por tipos de archivo
        file_types = Counter(f.get('file_type', 'unknown') for f in files)
        
        # Análisis temporal
        file_times = []
        suspicious_times = []
        
        for file in files:
            try:
                modified_time = datetime.datetime.strptime(file['modified'], "%Y-%m-%d %H:%M:%S")
                file_times.append(modified_time.hour)
                
                if file.get('is_suspicious', False):
                    suspicious_times.append(modified_time.hour)
            except (ValueError, KeyError):
                continue
        
        # Detectar patrones temporales anómalos
        after_hours_activity = sum(1 for hour in file_times if hour >= 22 or hour <= 6)
        
        # Análisis de tamaños
        file_sizes = [f.get('size', 0) for f in files]
        avg_file_size = np.mean(file_sizes) if file_sizes else 0
        large_files = [f for f in files if f.get('size', 0) > 100 * 1024 * 1024]  # >100MB
        
        # Detección de herramientas de limpieza
        cleanup_tools = []
        for file in files:
            filename = file.get('name', '').lower()
            if any(tool in filename for tool in ['ccleaner', 'bleach', 'eraser', 'wipe']):
                cleanup_tools.append(file)
        
        # Análisis de ubicaciones sospechosas
        suspicious_locations = defaultdict(int)
        for file in suspicious_files:
            path = file.get('path', '').lower()
            if 'temp' in path:
                suspicious_locations['temp'] += 1
            elif 'recycle' in path:
                suspicious_locations['recycle'] += 1
            elif 'backup' in path:
                suspicious_locations['backup'] += 1
            elif 'hidden' in path:
                suspicious_locations['hidden'] += 1
        
        # Calcular puntuación de riesgo del sistema de archivos
        risk_score = 0
        risk_factors = []
        
        if len(suspicious_files) > self.risk_thresholds['file_count_suspicious']:
            risk_score += len(suspicious_files) * 5
            risk_factors.append(f"High number of suspicious files: {len(suspicious_files)}")
        
        if cleanup_tools:
            risk_score += len(cleanup_tools) * 20
            risk_factors.append(f"Evidence destruction tools found: {len(cleanup_tools)}")
        
        if after_hours_activity > self.risk_thresholds['after_hours_threshold']:
            risk_score += after_hours_activity * 2
            risk_factors.append(f"Excessive after-hours activity: {after_hours_activity} events")
        
        if large_files:
            risk_score += len(large_files) * 10
            risk_factors.append(f"Large files detected: {len(large_files)}")
        
        # Análisis de patrones de nomenclatura
        naming_patterns = self._analyze_naming_patterns(files)
        
        analysis_result = {
            'total_files': total_files,
            'suspicious_files': len(suspicious_files),
            'file_types_distribution': dict(file_types),
            'after_hours_activity': after_hours_activity,
            'large_files_count': len(large_files),
            'cleanup_tools': len(cleanup_tools),
            'suspicious_locations': dict(suspicious_locations),
            'average_file_size': int(avg_file_size),
            'hourly_distribution': Counter(file_times),
            'suspicious_hourly_distribution': Counter(suspicious_times),
            'naming_patterns': naming_patterns,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors
        }
        
        logger.info(f"Análisis de archivos completado: {total_files} archivos, {len(suspicious_files)} sospechosos")
        return analysis_result

    def _analyze_naming_patterns(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza patrones en nombres de archivos"""
        patterns = {
            'sequential_names': 0,
            'random_names': 0,
            'hidden_files': 0,
            'suspicious_extensions': 0
        }
        
        suspicious_extensions = ['.tmp', '.bak', '.log', '.exe', '.bat', '.ps1']
        
        for file in files:
            name = file.get('name', '')
            
            # Archivos ocultos (empiezan con punto)
            if name.startswith('.'):
                patterns['hidden_files'] += 1
            
            # Extensiones sospechosas
            if any(name.lower().endswith(ext) for ext in suspicious_extensions):
                patterns['suspicious_extensions'] += 1
            
            # Nombres secuenciales (file001, file002, etc.)
            if any(char.isdigit() for char in name[-10:]):
                patterns['sequential_names'] += 1
        
        return patterns

    def analyze_network_activity(self, connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análisis avanzado de actividad de red"""
        logger.info("Iniciando análisis de actividad de red...")
        
        total_connections = len(connections)
        suspicious_connections = [c for c in connections if c.get('is_suspicious', False)]
        
        # Análisis de destinos
        destinations = Counter(c.get('destination_ip', 'unknown') for c in connections)
        ports = Counter(c.get('destination_port', 0) for c in connections)
        protocols = Counter(c.get('protocol', 'unknown') for c in connections)
        
        # Análisis temporal de red
        connection_hours = []
        for conn in connections:
            try:
                timestamp = datetime.datetime.strptime(conn['timestamp'], "%Y-%m-%d %H:%M:%S")
                connection_hours.append(timestamp.hour)
            except (ValueError, KeyError):
                continue
        
        # Transferencias de datos
        total_bytes = sum(c.get('bytes_transferred', 0) for c in connections)
        large_transfers = [c for c in connections if c.get('bytes_transferred', 0) > self.risk_thresholds['large_transfer_size']]
        
        # Detección de servicios en la nube
        cloud_services = []
        cloud_indicators = ['drive.google.com', 'dropbox.com', 'onedrive.live.com', 'mega.nz']
        
        for conn in connections:
            dest_ip = conn.get('destination_ip', '')
            if any(indicator in dest_ip for indicator in cloud_indicators):
                cloud_services.append(conn)
        
        # Conexiones después del horario laboral
        after_hours_connections = sum(1 for hour in connection_hours if hour >= 22 or hour <= 6)
        
        # Análisis de patrones de conexión
        connection_patterns = self._analyze_connection_patterns(connections)
        
        # Calcular puntuación de riesgo de red
        risk_score = 0
        risk_factors = []
        
        if len(suspicious_connections) > self.risk_thresholds['network_connections_suspicious']:
            risk_score += len(suspicious_connections) * 15
            risk_factors.append(f"Multiple suspicious connections: {len(suspicious_connections)}")
        
        if large_transfers:
            risk_score += len(large_transfers) * 20
            risk_factors.append(f"Large data transfers: {len(large_transfers)}")
        
        if cloud_services:
            risk_score += len(cloud_services) * 10
            risk_factors.append(f"Cloud service usage: {len(cloud_services)} connections")
        
        if after_hours_connections > 5:
            risk_score += after_hours_connections * 3
            risk_factors.append(f"After-hours network activity: {after_hours_connections} connections")
        
        analysis_result = {
            'total_connections': total_connections,
            'suspicious_connections': len(suspicious_connections),
            'destinations_distribution': dict(destinations.most_common(10)),
            'ports_distribution': dict(ports.most_common(10)),
            'protocols_distribution': dict(protocols),
            'total_bytes_transferred': total_bytes,
            'large_transfers_count': len(large_transfers),
            'cloud_services_count': len(cloud_services),
            'after_hours_connections': after_hours_connections,
            'hourly_distribution': Counter(connection_hours),
            'connection_patterns': connection_patterns,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors
        }
        
        logger.info(f"Análisis de red completado: {total_connections} conexiones, {len(suspicious_connections)} sospechosas")
        return analysis_result

    def _analyze_connection_patterns(self, connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza patrones en las conexiones de red"""
        patterns = {
            'burst_activity': False,
            'regular_intervals': False,
            'unusual_ports': [],
            'repeated_destinations': []
        }
        
        # Puertos inusuales (no estándar)
        unusual_ports = [c for c in connections if c.get('destination_port', 80) not in [80, 443, 25, 110, 143, 993, 995]]
        patterns['unusual_ports'] = len(unusual_ports)
        
        # Destinos repetidos (posible C&C)
        dest_counts = Counter(c.get('destination_ip', '') for c in connections)
        patterns['repeated_destinations'] = len([dest for dest, count in dest_counts.items() if count > 10])
        
        return patterns

    def generate_comprehensive_risk_assessment(self, file_analysis: Dict[str, Any], 
                                             network_analysis: Dict[str, Any],
                                             case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera evaluación comprensiva de riesgo"""
        logger.info("Generando evaluación comprensiva de riesgo...")
        
        # Combinar puntuaciones de riesgo
        file_risk = file_analysis.get('risk_score', 0)
        network_risk = network_analysis.get('risk_score', 0)
        
        # Ponderación: archivos 60%, red 40%
        combined_risk_score = int(file_risk * 0.6 + network_risk * 0.4)
        
        # Factores de riesgo combinados
        all_risk_factors = (
            file_analysis.get('risk_factors', []) + 
            network_analysis.get('risk_factors', [])
        )
        
        # Determinar nivel de riesgo
        if combined_risk_score >= 90:
            risk_level = "CRITICAL"
            risk_color = "#FF0000"
        elif combined_risk_score >= 70:
            risk_level = "HIGH"
            risk_color = "#FF6600"
        elif combined_risk_score >= 40:
            risk_level = "MEDIUM"
            risk_color = "#FFAA00"
        elif combined_risk_score >= 20:
            risk_level = "LOW"
            risk_color = "#FFFF00"
        else:
            risk_level = "MINIMAL"
            risk_color = "#00FF00"
        
        # Recomendaciones basadas en el análisis
        recommendations = self._generate_recommendations(file_analysis, network_analysis, risk_level)
        
        # Indicadores de compromiso (IOCs)
        iocs = self._extract_iocs(file_analysis, network_analysis)
        
        # Timeline de eventos críticos
        critical_timeline = self._build_critical_timeline(case_data)
        
        risk_assessment = {
            'overall_risk_score': combined_risk_score,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'file_system_risk': file_risk,
            'network_risk': network_risk,
            'risk_factors': all_risk_factors,
            'recommendations': recommendations,
            'indicators_of_compromise': iocs,
            'critical_timeline': critical_timeline,
            'threat_categories': self._categorize_threats(all_risk_factors),
            'confidence_level': self._calculate_confidence(file_analysis, network_analysis)
        }
        
        logger.info(f"Evaluación de riesgo completada: {risk_level} ({combined_risk_score}/100)")
        return risk_assessment

    def _generate_recommendations(self, file_analysis: Dict[str, Any], 
                                network_analysis: Dict[str, Any], 
                                risk_level: str) -> List[str]:
        """Genera recomendaciones específicas basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones basadas en archivos
        if file_analysis.get('cleanup_tools', 0) > 0:
            recommendations.append("Investigar el uso de herramientas de limpieza de evidencia")
            recommendations.append("Recuperar archivos eliminados usando herramientas forenses especializadas")
        
        if file_analysis.get('after_hours_activity', 0) > 10:
            recommendations.append("Correlacionar actividad fuera de horario con registros de acceso físico")
            recommendations.append("Entrevistar al sospechoso sobre actividades laborales nocturnas")
        
        if file_analysis.get('suspicious_files', 0) > 10:
            recommendations.append("Analizar en detalle los archivos marcados como sospechosos")
            recommendations.append("Verificar la legitimidad del acceso a información confidencial")
        
        # Recomendaciones basadas en red
        if network_analysis.get('large_transfers_count', 0) > 0:
            recommendations.append("Investigar destinos de transferencias de datos grandes")
            recommendations.append("Verificar si los datos transferidos están autorizados")
        
        if network_analysis.get('suspicious_connections', 0) > 0:
            recommendations.append("Analizar conexiones a IPs sospechosas con herramientas de threat intelligence")
            recommendations.append("Verificar si se utilizaron redes TOR o VPNs")
        
        if network_analysis.get('cloud_services_count', 0) > 0:
            recommendations.append("Revisar políticas de uso de servicios en la nube")
            recommendations.append("Solicitar logs de actividad de las cuentas de cloud identificadas")
        
        # Recomendaciones basadas en nivel de riesgo
        if risk_level in ["HIGH", "CRITICAL"]:
            recommendations.extend([
                "Preservar evidencia adicional inmediatamente",
                "Considerar medidas legales urgentes",
                "Notificar a las autoridades competentes",
                "Implementar controles de acceso adicionales"
            ])
        elif risk_level == "MEDIUM":
            recommendations.extend([
                "Realizar investigación más profunda",
                "Revisar políticas de seguridad internas",
                "Considerar entrevista formal con el sospechoso"
            ])
        
        return recommendations

    def _extract_iocs(self, file_analysis: Dict[str, Any], 
                     network_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extrae indicadores de compromiso del análisis"""
        iocs = {
            'suspicious_files': [],
            'malicious_ips': [],
            'suspicious_domains': [],
            'unusual_ports': [],
            'file_hashes': []
        }
        
        # Placeholder para IOCs específicos - en implementación real
        # se extraerían de los datos analizados
        if network_analysis.get('suspicious_connections', 0) > 0:
            iocs['malicious_ips'].append("192.168.1.100")  # Ejemplo
        
        return iocs

    def _build_critical_timeline(self, case_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Construye timeline de eventos críticos"""
        timeline = []
        
        # Agregar eventos de archivos sospechosos
        for file in case_data.get('files', []):
            if file.get('is_suspicious', False):
                timeline.append({
                    'timestamp': file.get('modified', ''),
                    'event': f"Archivo sospechoso modificado: {file.get('name', '')}",
                    'type': 'file_activity',
                    'severity': file.get('risk_level', 'NORMAL')
                })
        
        # Agregar conexiones sospechosas
        for conn in case_data.get('network_connections', []):
            if conn.get('is_suspicious', False):
                timeline.append({
                    'timestamp': conn.get('timestamp', ''),
                    'event': f"Conexión sospechosa a {conn.get('destination_ip', '')}",
                    'type': 'network_activity',
                    'severity': 'HIGH'
                })
        
        # Ordenar por timestamp
        timeline.sort(key=lambda x: x['timestamp'])
        
        return timeline[:20]  # Mostrar solo los 20 eventos más críticos

    def _categorize_threats(self, risk_factors: List[str]) -> Dict[str, int]:
        """Categoriza amenazas basadas en factores de riesgo"""
        categories = {
            'data_exfiltration': 0,
            'evidence_destruction': 0,
            'unauthorized_access': 0,
            'insider_threat': 0
        }
        
        for factor in risk_factors:
            factor_lower = factor.lower()
            
            if any(keyword in factor_lower for keyword in ['transfer', 'upload', 'cloud']):
                categories['data_exfiltration'] += 1
            
            if any(keyword in factor_lower for keyword in ['clean', 'delete', 'wipe', 'eraser']):
                categories['evidence_destruction'] += 1
            
            if any(keyword in factor_lower for keyword in ['unauthorized', 'privilege', 'backdoor']):
                categories['unauthorized_access'] += 1
            
            if any(keyword in factor_lower for keyword in ['after-hours', 'unusual', 'suspicious']):
                categories['insider_threat'] += 1
        
        return categories

    def _calculate_confidence(self, file_analysis: Dict[str, Any], 
                            network_analysis: Dict[str, Any]) -> str:
        """Calcula nivel de confianza del análisis"""
        total_evidence = (
            file_analysis.get('total_files', 0) + 
            network_analysis.get('total_connections', 0)
        )
        
        suspicious_evidence = (
            file_analysis.get('suspicious_files', 0) + 
            network_analysis.get('suspicious_connections', 0)
        )
        
        if total_evidence == 0:
            return "LOW"
        
        confidence_ratio = suspicious_evidence / total_evidence
        
        if confidence_ratio >= 0.3:
            return "HIGH"
        elif confidence_ratio >= 0.15:
            return "MEDIUM"
        else:
            return "LOW"

    def create_visualizations(self, file_analysis: Dict[str, Any], 
                            network_analysis: Dict[str, Any], 
                            output_dir: str = "C:/ForensicAI/reportes") -> Dict[str, str]:
        """Crea visualizaciones mejoradas del análisis"""
        logger.info("Generando visualizaciones del análisis...")
        
        os.makedirs(output_dir, exist_ok=True)
        generated_files = {}
        
        try:
            # 1. Distribución de tipos de archivo
            if file_analysis.get('file_types_distribution'):
                plt.figure(figsize=(12, 8))
                file_types = file_analysis['file_types_distribution']
                
                # Solo mostrar los top 10 tipos
                top_types = dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10])
                
                plt.subplot(2, 2, 1)
                bars = plt.bar(top_types.keys(), top_types.values(), color='skyblue')
                plt.title('Distribución de Tipos de Archivo', fontsize=14, fontweight='bold')
                plt.xlabel('Tipo de Archivo')
                plt.ylabel('Cantidad')
                plt.xticks(rotation=45)
                
                # Añadir valores en las barras
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom')
                
                # 2. Actividad por horas
                plt.subplot(2, 2, 2)
                hourly_dist = file_analysis.get('hourly_distribution', {})
                hours = list(range(24))
                activity = [hourly_dist.get(hour, 0) for hour in hours]
                
                plt.plot(hours, activity, marker='o', linewidth=2, markersize=6)
                plt.axvspan(22, 24, alpha=0.3, color='red', label='Horario Sospechoso')
                plt.axvspan(0, 6, alpha=0.3, color='red')
                plt.axvspan(8, 18, alpha=0.3, color='green', label='Horario Normal')
                plt.title('Actividad de Archivos por Hora', fontsize=14, fontweight='bold')
                plt.xlabel('Hora del Día')
                plt.ylabel('Número de Actividades')
                plt.legend()
                plt.grid(True, alpha=0.3)
                
                # 3. Análisis de red por horas
                plt.subplot(2, 2, 3)
                network_hourly = network_analysis.get('hourly_distribution', {})
                network_activity = [network_hourly.get(hour, 0) for hour in hours]
                
                plt.plot(hours, network_activity, marker='s', linewidth=2, markersize=6, color='orange')
                plt.axvspan(22, 24, alpha=0.3, color='red')
                plt.axvspan(0, 6, alpha=0.3, color='red')
                plt.axvspan(8, 18, alpha=0.3, color='green')
                plt.title('Actividad de Red por Hora', fontsize=14, fontweight='bold')
                plt.xlabel('Hora del Día')
                plt.ylabel('Número de Conexiones')
                plt.grid(True, alpha=0.3)
                
                # 4. Comparación de archivos normales vs sospechosos
                plt.subplot(2, 2, 4)
                categories = ['Archivos Normales', 'Archivos Sospechosos']
                counts = [
                    file_analysis.get('total_files', 0) - file_analysis.get('suspicious_files', 0),
                    file_analysis.get('suspicious_files', 0)
                ]
                colors = ['lightgreen', 'lightcoral']
                
                wedges, texts, autotexts = plt.pie(counts, labels=categories, colors=colors, 
                                                  autopct='%1.1f%%', startangle=90)
                plt.title('Distribución de Archivos', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                
                viz_file = os.path.join(output_dir, "forensic_analysis_overview.png")
                plt.savefig(viz_file, dpi=300, bbox_inches='tight')
                generated_files['overview'] = viz_file
                plt.close()
            
            # 5. Gráfico de riesgo temporal
            plt.figure(figsize=(14, 6))
            
            # Simular timeline de riesgo
            suspicious_files = file_analysis.get('suspicious_files', 0)
            suspicious_connections = network_analysis.get('suspicious_connections', 0)
            
            timeline_data = {
                'Archivos Sospechosos': suspicious_files,
                'Conexiones Sospechosas': suspicious_connections,
                'Actividad Fuera de Horario': file_analysis.get('after_hours_activity', 0),
                'Transferencias Grandes': network_analysis.get('large_transfers_count', 0)
            }
            
            bars = plt.bar(timeline_data.keys(), timeline_data.values(), 
                          color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            
            plt.title('Indicadores de Riesgo Detectados', fontsize=16, fontweight='bold')
            plt.ylabel('Cantidad')
            plt.xticks(rotation=45)
            
            # Añadir valores en las barras
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            risk_file = os.path.join(output_dir, "risk_indicators.png")
            plt.savefig(risk_file, dpi=300, bbox_inches='tight')
            generated_files['risk_indicators'] = risk_file
            plt.close()
            
            logger.info(f"Visualizaciones generadas exitosamente en: {output_dir}")
            
        except Exception as e:
            logger.error(f"Error generando visualizaciones: {e}")
        
        return generated_files

    def analyze_case(self, case_file_path: str) -> Dict[str, Any]:
        """Analiza un caso completo y genera reporte"""
        logger.info(f"Iniciando análisis completo del caso: {case_file_path}")
        
        try:
            # Cargar caso
            case_data = self.load_case(case_file_path)
            
            # Realizar análisis
            file_analysis = self.analyze_file_system(case_data.get('files', []))
            network_analysis = self.analyze_network_activity(case_data.get('network_connections', []))
            
            # Generar evaluación de riesgo
            risk_assessment = self.generate_comprehensive_risk_assessment(
                file_analysis, network_analysis, case_data
            )
            
            # Crear visualizaciones
            visualizations = self.create_visualizations(file_analysis, network_analysis)
            
            # Compilar resultado completo
            complete_analysis = {
                'case_info': {
                    'case_id': case_data.get('case_id'),
                    'case_type': case_data.get('case_type'),
                    'suspect_name': case_data.get('suspect_name'),
                    'analysis_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                'file_analysis': file_analysis,
                'network_analysis': network_analysis,
                'risk_assessment': risk_assessment,
                'visualizations': visualizations,
                'summary': {
                    'total_files_analyzed': file_analysis.get('total_files', 0),
                    'suspicious_files_found': file_analysis.get('suspicious_files', 0),
                    'total_network_connections': network_analysis.get('total_connections', 0),
                    'suspicious_connections_found': network_analysis.get('suspicious_connections', 0),
                    'overall_risk_level': risk_assessment.get('risk_level'),
                    'overall_risk_score': risk_assessment.get('overall_risk_score'),
                    'confidence_level': risk_assessment.get('confidence_level')
                }
            }
            
            # Guardar análisis
            self.analysis_results[case_data.get('case_id')] = complete_analysis
            
            logger.info(f"Análisis completado exitosamente para caso: {case_data.get('case_id')}")
            return complete_analysis
            
        except Exception as e:
            logger.error(f"Error durante el análisis del caso: {e}")
            raise

    def save_analysis_report(self, analysis_result: Dict[str, Any], 
                           output_dir: str = "C:/ForensicAI/reportes") -> str:
        """Guarda el reporte de análisis en JSON"""
        os.makedirs(output_dir, exist_ok=True)
        
        case_id = analysis_result['case_info']['case_id']
        filename = f"{case_id}_analysis_report.json"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte de análisis guardado en: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            raise

    def generate_summary_report(self, analysis_result: Dict[str, Any]) -> str:
        """Genera un reporte resumen en texto plano"""
        case_info = analysis_result['case_info']
        file_analysis = analysis_result['file_analysis']
        network_analysis = analysis_result['network_analysis']
        risk_assessment = analysis_result['risk_assessment']
        summary = analysis_result['summary']
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    REPORTE DE ANÁLISIS FORENSE               ║
╚══════════════════════════════════════════════════════════════╝

📋 INFORMACIÓN DEL CASO
═══════════════════════════════════════════════════════════════
ID del Caso: {case_info['case_id']}
Tipo de Caso: {case_info['case_type'].replace('_', ' ').title()}
Sospechoso: {case_info['suspect_name']}
Fecha de Análisis: {case_info['analysis_timestamp']}

🎯 RESUMEN EJECUTIVO
═══════════════════════════════════════════════════════════════
Nivel de Riesgo: {risk_assessment['risk_level']} ({risk_assessment['overall_risk_score']}/100)
Nivel de Confianza: {risk_assessment['confidence_level']}

📊 ESTADÍSTICAS PRINCIPALES
═══════════════════════════════════════════════════════════════
• Archivos Analizados: {summary['total_files_analyzed']}
• Archivos Sospechosos: {summary['suspicious_files_found']}
• Conexiones de Red: {summary['total_network_connections']}
• Conexiones Sospechosas: {summary['suspicious_connections_found']}

🔍 ANÁLISIS DEL SISTEMA DE ARCHIVOS
═══════════════════════════════════════════════════════════════
• Actividad Fuera de Horario: {file_analysis.get('after_hours_activity', 0)} eventos
• Archivos Grandes (>100MB): {file_analysis.get('large_files_count', 0)}
• Herramientas de Limpieza: {file_analysis.get('cleanup_tools', 0)}
• Puntuación de Riesgo: {file_analysis.get('risk_score', 0)}/100

🌐 ANÁLISIS DE ACTIVIDAD DE RED
═══════════════════════════════════════════════════════════════
• Transferencias Grandes: {network_analysis.get('large_transfers_count', 0)}
• Servicios en la Nube: {network_analysis.get('cloud_services_count', 0)}
• Conexiones Fuera de Horario: {network_analysis.get('after_hours_connections', 0)}
• Puntuación de Riesgo: {network_analysis.get('risk_score', 0)}/100

⚠️ FACTORES DE RIESGO DETECTADOS
═══════════════════════════════════════════════════════════════"""

        for i, factor in enumerate(risk_assessment.get('risk_factors', []), 1):
            report += f"\n{i:2d}. {factor}"

        report += f"""

💡 RECOMENDACIONES PRINCIPALES
═══════════════════════════════════════════════════════════════"""

        for i, recommendation in enumerate(risk_assessment.get('recommendations', [])[:5], 1):
            report += f"\n{i:2d}. {recommendation}"

        report += f"""

📈 CATEGORIZACIÓN DE AMENAZAS
═══════════════════════════════════════════════════════════════"""

        threat_categories = risk_assessment.get('threat_categories', {})
        for threat_type, count in threat_categories.items():
            if count > 0:
                threat_name = threat_type.replace('_', ' ').title()
                report += f"\n• {threat_name}: {count} indicadores"

        report += f"""

═══════════════════════════════════════════════════════════════
Reporte generado por: Asistente Forense IA
Versión: 2.0 - Motor de Análisis Mejorado
═══════════════════════════════════════════════════════════════
        """
        
        return report.strip()

def main():
    """Función principal para demostrar el analizador"""
    print("🔬 MOTOR DE ANÁLISIS FORENSE MEJORADO")
    print("=" * 60)
    
    analyzer = EnhancedForensicAnalyzer()
    
    # Buscar casos disponibles
    cases_dir = "C:/ForensicAI/casos_reales/casos_procesados"
    
    if not os.path.exists(cases_dir):
        print("❌ No se encontraron casos para analizar.")
        print(f"   Ejecuta primero: python forensic_data_generator.py")
        return
    
    case_files = [f for f in os.listdir(cases_dir) if f.endswith('.json')]
    
    if not case_files:
        print("❌ No se encontraron archivos de casos en el directorio.")
        return
    
    # Analizar el primer caso disponible
    case_file = os.path.join(cases_dir, case_files[0])
    
    print(f"📋 Analizando caso: {case_files[0]}")
    print("-" * 60)
    
    try:
        # Realizar análisis completo
        analysis_result = analyzer.analyze_case(case_file)
        
        # Mostrar resumen
        print("\n📊 RESUMEN DEL ANÁLISIS:")
        print("-" * 60)
        
        summary = analysis_result['summary']
        risk = analysis_result['risk_assessment']
        
        print(f"✅ Caso: {analysis_result['case_info']['case_id']}")
        print(f"👤 Sospechoso: {analysis_result['case_info']['suspect_name']}")
        print(f"📁 Archivos Analizados: {summary['total_files_analyzed']}")
        print(f"⚠️  Archivos Sospechosos: {summary['suspicious_files_found']}")
        print(f"🌐 Conexiones de Red: {summary['total_network_connections']}")
        print(f"🚨 Conexiones Sospechosas: {summary['suspicious_connections_found']}")
        print(f"🎯 Nivel de Riesgo: {risk['risk_level']} ({risk['overall_risk_score']}/100)")
        print(f"🔍 Confianza: {risk['confidence_level']}")
        
        # Mostrar factores de riesgo principales
        if risk.get('risk_factors'):
            print(f"\n⚠️ PRINCIPALES FACTORES DE RIESGO:")
            for i, factor in enumerate(risk['risk_factors'][:3], 1):
                print(f"   {i}. {factor}")
        
        # Guardar reporte
        report_file = analyzer.save_analysis_report(analysis_result)
        print(f"\n💾 Reporte completo guardado en:")
        print(f"   {report_file}")
        
        # Generar reporte de texto
        text_report = analyzer.generate_summary_report(analysis_result)
        report_text_file = report_file.replace('.json', '_summary.txt')
        
        with open(report_text_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        print(f"📄 Reporte resumen guardado en:")
        print(f"   {report_text_file}")
        
        # Mostrar ubicación de visualizaciones
        if analysis_result.get('visualizations'):
            print(f"\n📊 Visualizaciones generadas:")
            for viz_type, viz_path in analysis_result['visualizations'].items():
                print(f"   • {viz_type}: {viz_path}")
        
        print(f"\n🎉 ¡Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        logger.error(f"Error en main: {e}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")