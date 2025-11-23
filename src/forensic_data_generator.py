#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Datos Sintéticos Mejorado - Asistente Forense IA
Genera casos forenses realistas para entrenamiento y demo del sistema
"""

import json
import random
import datetime
import hashlib
import os
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/ForensicAI/logs/data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FileEvidence:
    """Clase para representar evidencia de archivos"""
    name: str
    path: str
    size: int
    created: str
    modified: str
    accessed: str
    file_type: str
    hash_md5: str
    hash_sha256: str
    is_suspicious: bool
    suspicion_reason: str = ""
    risk_level: str = "NORMAL"  # NORMAL, SUSPICIOUS, HIGH, CRITICAL

@dataclass
class NetworkConnection:
    """Clase para representar conexiones de red"""
    timestamp: str
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: str
    bytes_transferred: int
    connection_type: str
    is_suspicious: bool
    suspicion_reason: str = ""

@dataclass
class ForensicCase:
    """Clase principal para casos forenses"""
    case_id: str
    case_type: str
    suspect_name: str
    description: str
    created_timestamp: str
    files: List[FileEvidence]
    network_connections: List[NetworkConnection]
    system_info: Dict[str, Any]
    investigation_notes: List[str]
    risk_assessment: Dict[str, Any]

class EnhancedForensicDataGenerator:
    """Generador mejorado de datos forenses sintéticos"""
    
    def __init__(self):
        self.case_types = [
            "employee_data_theft",
            "intellectual_property_theft", 
            "insider_trading",
            "corporate_espionage",
            "malware_infection",
            "ransomware_attack",
            "unauthorized_access",
            "financial_fraud"
        ]
        
        self.suspicious_file_patterns = [
            "confidential", "secreto", "privado", "backup_emails", 
            "client_list", "customer_data", "financial_records",
            "strategy", "internal", "restricted", "password",
            "credentials", "ccleaner", "bleachbit", "eraser",
            "tor_browser", "vpn_config", "keylogger", "backdoor"
        ]
        
        self.suspicious_extensions = [
            ".zip", ".rar", ".7z", ".pst", ".ost", ".sql", 
            ".csv", ".xlsx", ".docx", ".pdf", ".key", ".p12"
        ]
        
        self.malicious_tools = [
            "ccleaner_portable.exe", "bleachbit.exe", "eraser.exe",
            "tor.exe", "wireshark.exe", "nmap.exe", "metasploit.exe",
            "hashcat.exe", "john.exe", "keylogger.exe"
        ]
        
        self.cloud_services = [
            "drive.google.com", "dropbox.com", "onedrive.live.com",
            "mega.nz", "wetransfer.com", "sendspace.com"
        ]

    def generate_realistic_timestamp(self, base_date: datetime.datetime = None, 
                                   hours_offset: int = 0) -> str:
        """Genera timestamps realistas"""
        if base_date is None:
            base_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
        
        # Simular actividad sospechosa fuera de horario
        if random.random() < 0.3:  # 30% de actividad sospechosa
            # Horario sospechoso: 22:00 - 06:00
            hour = random.choice(list(range(22, 24)) + list(range(0, 6)))
            minute = random.randint(0, 59)
        else:
            # Horario normal: 08:00 - 18:00
            hour = random.randint(8, 18)
            minute = random.randint(0, 59)
        
        timestamp = base_date.replace(hour=hour, minute=minute, second=random.randint(0, 59))
        timestamp += datetime.timedelta(hours=hours_offset)
        
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def generate_file_hash(self, filename: str) -> tuple:
        """Genera hashes MD5 y SHA256 realistas"""
        # Usar el nombre del archivo como seed para hashes consistentes
        seed_data = f"{filename}_{random.randint(1000, 9999)}".encode()
        
        md5_hash = hashlib.md5(seed_data).hexdigest()
        sha256_hash = hashlib.sha256(seed_data).hexdigest()
        
        return md5_hash, sha256_hash

    def is_file_suspicious(self, filename: str, file_path: str) -> tuple:
        """Determina si un archivo es sospechoso y por qué"""
        filename_lower = filename.lower()
        path_lower = file_path.lower()
        
        # Verificar patrones sospechosos en nombre
        for pattern in self.suspicious_file_patterns:
            if pattern in filename_lower:
                return True, f"Nombre contiene patrón sospechoso: '{pattern}'"
        
        # Verificar herramientas maliciosas
        if filename in self.malicious_tools:
            return True, f"Herramienta de limpieza/hacking detectada: {filename}"
        
        # Verificar ubicaciones sospechosas
        suspicious_paths = ["temp", "recycle", "backup", "hidden", "cache"]
        for susp_path in suspicious_paths:
            if susp_path in path_lower:
                return True, f"Ubicación sospechosa: {susp_path}"
        
        # Verificar extensiones con contenido sospechoso
        for ext in self.suspicious_extensions:
            if filename_lower.endswith(ext):
                if random.random() < 0.4:  # 40% de archivos con extensiones sospechosas
                    return True, f"Archivo {ext} en contexto sospechoso"
        
        return False, ""

    def generate_file_evidence(self, case_type: str, num_files: int = None) -> List[FileEvidence]:
        """Genera evidencia de archivos realista"""
        if num_files is None:
            num_files = random.randint(80, 200)
        
        files = []
        base_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 15))
        
        # Tipos de archivos según el caso
        file_templates = {
            "employee_data_theft": [
                ("Lista_Clientes_VIP.xlsx", "/Documents/Confidential/", True),
                ("Backup_Emails_2024.pst", "/AppData/Local/Microsoft/Outlook/", True),
                ("Estrategia_Marketing_2024.docx", "/Documents/Internal/", True),
                ("ccleaner_portable.zip", "/Downloads/", True),
                ("tor_browser.exe", "/Downloads/Security/", True)
            ],
            "intellectual_property_theft": [
                ("Codigo_Fuente_Proyecto_X.zip", "/Documents/Development/", True),
                ("Patente_Algoritmo_IA.pdf", "/Documents/Legal/", True),
                ("Diseños_Producto_2025.dwg", "/Documents/Engineering/", True),
                ("Research_Notes_Confidential.docx", "/Documents/Research/", True)
            ],
            "malware_infection": [
                ("invoice_payment.exe", "/Downloads/", True),
                ("document.pdf.exe", "/Desktop/", True),
                ("system_update.bat", "/Temp/", True),
                ("winlogon.exe", "/Windows/System32/", True)
            ]
        }
        
        # Archivos específicos del tipo de caso
        if case_type in file_templates:
            for filename, path, is_suspicious in file_templates[case_type]:
                size = random.randint(1024, 50*1024*1024)  # 1KB - 50MB
                created = self.generate_realistic_timestamp(base_date)
                modified = self.generate_realistic_timestamp(base_date, random.randint(1, 48))
                accessed = self.generate_realistic_timestamp(base_date, random.randint(49, 72))
                
                md5_hash, sha256_hash = self.generate_file_hash(filename)
                
                suspicion_reason = ""
                risk_level = "NORMAL"
                
                if is_suspicious:
                    _, suspicion_reason = self.is_file_suspicious(filename, path)
                    risk_level = random.choice(["SUSPICIOUS", "HIGH", "CRITICAL"])
                
                file_evidence = FileEvidence(
                    name=filename,
                    path=path,
                    size=size,
                    created=created,
                    modified=modified,
                    accessed=accessed,
                    file_type=filename.split('.')[-1] if '.' in filename else 'unknown',
                    hash_md5=md5_hash,
                    hash_sha256=sha256_hash,
                    is_suspicious=is_suspicious,
                    suspicion_reason=suspicion_reason,
                    risk_level=risk_level
                )
                
                files.append(file_evidence)
        
        # Generar archivos normales adicionales
        normal_files = [
            "document.docx", "report.pdf", "presentation.pptx", "data.xlsx",
            "photo.jpg", "video.mp4", "music.mp3", "archive.zip",
            "config.ini", "log.txt", "backup.bak", "temp.tmp"
        ]
        
        normal_paths = [
            "/Documents/", "/Desktop/", "/Downloads/", "/Pictures/",
            "/Videos/", "/Music/", "/AppData/Local/", "/Users/Public/"
        ]
        
        remaining_files = num_files - len(files)
        for i in range(remaining_files):
            filename = f"{random.choice(['doc', 'file', 'report', 'data'])}{i:03d}.{random.choice(['docx', 'pdf', 'xlsx', 'txt', 'jpg'])}"
            path = random.choice(normal_paths)
            
            size = random.randint(1024, 10*1024*1024)  # 1KB - 10MB
            created = self.generate_realistic_timestamp(base_date)
            modified = self.generate_realistic_timestamp(base_date, random.randint(1, 24))
            accessed = self.generate_realistic_timestamp(base_date, random.randint(25, 48))
            
            md5_hash, sha256_hash = self.generate_file_hash(filename)
            
            # Algunos archivos normales pueden ser sospechosos por contexto
            is_suspicious, suspicion_reason = self.is_file_suspicious(filename, path)
            risk_level = "SUSPICIOUS" if is_suspicious else "NORMAL"
            
            file_evidence = FileEvidence(
                name=filename,
                path=path,
                size=size,
                created=created,
                modified=modified,
                accessed=accessed,
                file_type=filename.split('.')[-1],
                hash_md5=md5_hash,
                hash_sha256=sha256_hash,
                is_suspicious=is_suspicious,
                suspicion_reason=suspicion_reason,
                risk_level=risk_level
            )
            
            files.append(file_evidence)
        
        return files

    def generate_network_connections(self, case_type: str, num_connections: int = None) -> List[NetworkConnection]:
        """Genera conexiones de red realistas"""
        if num_connections is None:
            num_connections = random.randint(15, 50)
        
        connections = []
        base_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 7))
        
        # IPs sospechosas conocidas
        suspicious_ips = [
            "185.220.101.182", "tor-exit-node.com",
            "194.195.216.146", "malware-c2.net",
            "45.142.214.109", "phishing-site.org"
        ]
        
        # Servicios en la nube
        cloud_ips = [
            "172.217.16.142",  # Google
            "13.107.42.14",    # Microsoft
            "31.13.64.35"      # Facebook/Meta
        ]
        
        for i in range(num_connections):
            timestamp = self.generate_realistic_timestamp(base_date, random.randint(0, 168))
            source_ip = "192.168.1.100"  # IP del sospechoso
            
            # Determinar tipo de conexión
            is_suspicious = False
            suspicion_reason = ""
            connection_type = "normal_browsing"
            
            if random.random() < 0.2:  # 20% conexiones sospechosas
                destination_ip = random.choice(suspicious_ips)
                destination_port = random.choice([80, 443, 9050, 8080])
                is_suspicious = True
                suspicion_reason = "Conexión a IP conocida por actividades maliciosas"
                connection_type = "suspicious"
            elif random.random() < 0.3:  # 30% servicios en la nube
                destination_ip = random.choice(cloud_ips)
                destination_port = 443
                connection_type = "cloud_service"
                # Las transferencias grandes a la nube pueden ser sospechosas
                if random.random() < 0.4:
                    is_suspicious = True
                    suspicion_reason = "Transferencia grande a servicio en la nube"
            else:
                # Conexión normal
                destination_ip = f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                destination_port = random.choice([80, 443, 25, 110, 993, 995])
            
            protocol = random.choice(["TCP", "UDP", "HTTPS", "HTTP"])
            bytes_transferred = random.randint(1024, 100*1024*1024)  # 1KB - 100MB
            
            # Transferencias grandes son sospechosas
            if bytes_transferred > 50*1024*1024:  # > 50MB
                is_suspicious = True
                if not suspicion_reason:
                    suspicion_reason = "Transferencia de datos excepcionalmente grande"
            
            connection = NetworkConnection(
                timestamp=timestamp,
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_port=destination_port,
                protocol=protocol,
                bytes_transferred=bytes_transferred,
                connection_type=connection_type,
                is_suspicious=is_suspicious,
                suspicion_reason=suspicion_reason
            )
            
            connections.append(connection)
        
        return connections

    def calculate_risk_assessment(self, files: List[FileEvidence], 
                                network_connections: List[NetworkConnection],
                                case_type: str) -> Dict[str, Any]:
        """Calcula evaluación de riesgo del caso"""
        suspicious_files = [f for f in files if f.is_suspicious]
        suspicious_connections = [c for c in network_connections if c.is_suspicious]
        
        # Contar actividad fuera de horario
        after_hours_activity = 0
        for file in files:
            hour = int(file.modified.split(' ')[1].split(':')[0])
            if hour >= 22 or hour <= 6:
                after_hours_activity += 1
        
        for conn in network_connections:
            hour = int(conn.timestamp.split(' ')[1].split(':')[0])
            if hour >= 22 or hour <= 6:
                after_hours_activity += 1
        
        # Calcular puntuación de riesgo
        risk_score = 0
        risk_factors = []
        
        # Factores de archivos
        if suspicious_files:
            risk_score += len(suspicious_files) * 10
            risk_factors.append(f"Found {len(suspicious_files)} suspicious files")
        
        # Herramientas de destrucción de evidencia
        destruction_tools = [f for f in suspicious_files if any(tool in f.name.lower() for tool in ['ccleaner', 'bleach', 'eraser'])]
        if destruction_tools:
            risk_score += len(destruction_tools) * 15
            risk_factors.append(f"Evidence destruction tools detected: {len(destruction_tools)}")
        
        # Actividad fuera de horario
        if after_hours_activity > 5:
            risk_score += after_hours_activity * 2
            risk_factors.append(f"After-hours file activity: {after_hours_activity} instances")
        
        # Conexiones sospechosas
        if suspicious_connections:
            risk_score += len(suspicious_connections) * 8
            risk_factors.append(f"Suspicious network connections: {len(suspicious_connections)}")
        
        # Transferencias grandes
        large_transfers = [c for c in network_connections if c.bytes_transferred > 50*1024*1024]
        if large_transfers:
            risk_score += len(large_transfers) * 12
            risk_factors.append(f"Large data transfers detected: {len(large_transfers)}")
        
        # Determinar nivel de riesgo
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        elif risk_score >= 10:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"
        
        return {
            "risk_score": min(risk_score, 100),  # Cap at 100
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "total_files": len(files),
            "suspicious_files": len(suspicious_files),
            "total_connections": len(network_connections),
            "suspicious_connections": len(suspicious_connections),
            "after_hours_activity": after_hours_activity,
            "large_transfers": len(large_transfers)
        }

    def generate_investigation_notes(self, case_type: str, risk_assessment: Dict[str, Any]) -> List[str]:
        """Genera notas de investigación realistas"""
        notes = [
            f"Caso iniciado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Tipo de investigación: {case_type.replace('_', ' ').title()}",
            f"Nivel de riesgo preliminar: {risk_assessment['risk_level']}"
        ]
        
        if risk_assessment['suspicious_files'] > 0:
            notes.append(f"Se detectaron {risk_assessment['suspicious_files']} archivos sospechosos")
        
        if risk_assessment['after_hours_activity'] > 10:
            notes.append(f"Actividad significativa fuera de horario laboral: {risk_assessment['after_hours_activity']} eventos")
        
        if risk_assessment['large_transfers'] > 0:
            notes.append(f"Transferencias de datos grandes detectadas: {risk_assessment['large_transfers']} instancias")
        
        case_specific_notes = {
            "employee_data_theft": [
                "Investigar acceso a sistemas de clientes y bases de datos",
                "Verificar uso de herramientas de limpieza de evidencia",
                "Revisar actividad de correo electrónico y transferencias externas"
            ],
            "intellectual_property_theft": [
                "Analizar acceso a repositorios de código fuente",
                "Verificar descargas de documentación técnica",
                "Revisar comunicaciones con competidores"
            ],
            "malware_infection": [
                "Identificar vector de infección inicial",
                "Analizar propagación lateral en la red",
                "Verificar exfiltración de datos"
            ]
        }
        
        if case_type in case_specific_notes:
            notes.extend(case_specific_notes[case_type])
        
        return notes

    def generate_case(self, case_type: str = None, case_id: str = None) -> ForensicCase:
        """Genera un caso forense completo"""
        if case_type is None:
            case_type = random.choice(self.case_types)
        
        if case_id is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            case_id = f"{case_type}_{timestamp}"
        
        # Nombres de sospechosos realistas
        suspect_names = [
            "Juan Martínez", "María García", "Carlos López", "Ana Rodriguez",
            "Luis Fernández", "Carmen Sánchez", "José González", "Isabel Ruiz"
        ]
        
        suspect_name = random.choice(suspect_names)
        
        # Descripción del caso
        case_descriptions = {
            "employee_data_theft": f"Empleado {suspect_name} bajo sospecha de robar información confidencial de clientes antes de su renuncia",
            "intellectual_property_theft": f"Investigación de {suspect_name} por posible robo de propiedad intelectual y código fuente",
            "insider_trading": f"Análisis forense del equipo de {suspect_name} por sospecha de uso de información privilegiada",
            "corporate_espionage": f"Caso de espionaje corporativo involucrando a {suspect_name} y transferencia de secretos comerciales",
            "malware_infection": f"Análisis de infección de malware en el sistema de {suspect_name} con posible exfiltración de datos",
            "ransomware_attack": f"Investigación de ataque de ransomware iniciado desde el equipo de {suspect_name}",
            "unauthorized_access": f"Acceso no autorizado detectado en la cuenta de {suspect_name} con actividad sospechosa",
            "financial_fraud": f"Investigación de fraude financiero con evidencia digital del equipo de {suspect_name}"
        }
        
        description = case_descriptions.get(case_type, f"Investigación forense general del equipo de {suspect_name}")
        
        logger.info(f"Generando caso: {case_id} - {case_type}")
        
        # Generar evidencia
        files = self.generate_file_evidence(case_type)
        network_connections = self.generate_network_connections(case_type)
        
        # Calcular evaluación de riesgo
        risk_assessment = self.calculate_risk_assessment(files, network_connections, case_type)
        
        # Generar notas de investigación
        investigation_notes = self.generate_investigation_notes(case_type, risk_assessment)
        
        # Información del sistema
        system_info = {
            "os": "Windows 11 Professional",
            "computer_name": f"WORKSTATION-{random.randint(100, 999)}",
            "user_account": suspect_name.replace(" ", ".").lower(),
            "last_login": self.generate_realistic_timestamp(),
            "timezone": "UTC-03:00 (Argentina Standard Time)",
            "total_disk_space": f"{random.randint(250, 1000)} GB",
            "available_space": f"{random.randint(50, 200)} GB"
        }
        
        case = ForensicCase(
            case_id=case_id,
            case_type=case_type,
            suspect_name=suspect_name,
            description=description,
            created_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            files=files,
            network_connections=network_connections,
            system_info=system_info,
            investigation_notes=investigation_notes,
            risk_assessment=risk_assessment
        )
        
        logger.info(f"Caso generado exitosamente: {len(files)} archivos, {len(network_connections)} conexiones, riesgo {risk_assessment['risk_level']}")
        
        return case

    def save_case(self, case: ForensicCase, output_dir: str = "C:/ForensicAI/casos_reales/casos_procesados") -> str:
        """Guarda el caso en formato JSON"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{case.case_id}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Convertir a diccionario serializable
        case_dict = asdict(case)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(case_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Caso guardado en: {filepath}")
        return filepath

def main():
    """Función principal para generar casos de demo"""
    print("🧪 GENERADOR DE DATOS SINTÉTICOS MEJORADO")
    print("=" * 50)
    
    generator = EnhancedForensicDataGenerator()
    
    # Generar casos de cada tipo para demo
    case_types = [
        "employee_data_theft",
        "intellectual_property_theft", 
        "malware_infection"
    ]
    
    generated_cases = []
    
    for case_type in case_types:
        print(f"\n📋 Generando caso: {case_type}")
        case = generator.generate_case(case_type)
        filepath = generator.save_case(case)
        generated_cases.append((case_type, filepath))
        
        print(f"✅ {case.case_id}")
        print(f"   Sospechoso: {case.suspect_name}")
        print(f"   Archivos: {len(case.files)} (sospechosos: {case.risk_assessment['suspicious_files']})")
        print(f"   Conexiones: {len(case.network_connections)} (sospechosas: {case.risk_assessment['suspicious_connections']})")
        print(f"   Nivel de Riesgo: {case.risk_assessment['risk_level']} ({case.risk_assessment['risk_score']}/100)")
        print(f"   Guardado en: {filepath}")
    
    print(f"\n🎉 ¡{len(generated_cases)} casos generados exitosamente!")
    print(f"📁 Ubicación: C:/ForensicAI/casos_reales/casos_procesados/")
    
    return generated_cases

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")