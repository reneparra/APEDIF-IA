#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APEDIF IA - Análisis de Evidencia Digital Forense con Inteligencia Artificial
Diseño optimizado: panel izquierdo compacto, fuentes grandes, log integrado
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import customtkinter as ctk
import threading
import json
import os
import subprocess
import datetime
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import webbrowser

# Importar nuestros módulos
try:
    from forensic_data_generator import EnhancedForensicDataGenerator
    from forensic_analyzer import EnhancedForensicAnalyzer
    from ai_forensic_assistant import EnhancedForensicAIAssistant
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos estén en el mismo directorio")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/ForensicAI/logs/gui_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ForensicGUIApplication:
    """Aplicación GUI completa para análisis forense con IA"""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔍 APEDIF IA - Análisis de Evidencia Digital Forense con Inteligencia Artificial")
        self.root.geometry("1700x1000")
        self.root.minsize(1200, 800)

        # Variables de estado
        self.current_case_id = tk.StringVar(value=self._generate_case_id())
        self.case_type = tk.StringVar(value="employee_data_theft")
        self.investigator_name = tk.StringVar(value="Rene Parra")
        self.evidence_type = tk.StringVar(value="synthetic")
        self.selected_image_path = tk.StringVar()

        # Componentes del sistema
        self.data_generator = None
        self.analyzer = None
        self.ai_assistant = None

        # Resultados actuales
        self.current_analysis = None
        self.current_ai_insights = None

        # Crear interfaz
        self._create_interface()
        self._initialize_components()

        # Log inicial
        self._log_message("🚀 APEDIF IA iniciado - Sistema de Rene Parra listo para análisis")

    def _generate_case_id(self) -> str:
        """Genera ID único para el caso"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"CASE_{timestamp}"

    def _create_interface(self):
        """Crea la interfaz con panel izquierdo compacto y panel derecho extendido"""
        # Frame principal con grid
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Layout: 2 columnas, panel izquierdo pequeño (20%), derecho grande (80%)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=4)

        # === PANEL IZQUIERDO: Compacto (encabezado + control + log) ===
        left_panel = ctk.CTkFrame(main_frame)
        left_panel.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=(5, 2), pady=5)
        left_panel.grid_rowconfigure(0, weight=0)
        left_panel.grid_rowconfigure(1, weight=2)
        left_panel.grid_rowconfigure(2, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        # 1. Encabezado en panel izquierdo
        self._create_header(left_panel)
        self.header_frame.pack(fill="x", padx=5, pady=5)

        # 2. Panel de control
        self._create_control_panel(left_panel)
        self.control_frame.pack(fill="x", padx=5, pady=(5, 10))

        # 3. Log de actividad
        self._create_log_section(left_panel)
        self.log_frame.pack(fill="x", padx=5, pady=(0, 5))

        # === PANEL DERECHO: Resultados extendidos (arriba a abajo) ===
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.grid(row=0, column=1, rowspan=2, sticky="nswe", padx=(2, 5), pady=5)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Panel de resultados que ocupa todo el espacio
        self._create_results_section(right_panel)
        self.results_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def _create_header(self, parent):
        """Crea el encabezado dentro del panel izquierdo"""
        self.header_frame = ctk.CTkFrame(parent)
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="🔍 APEDIF IA",
            font=ctk.CTkFont(size=22, weight="bold", family="Segoe UI")
        )
        title_label.pack(pady=(12, 2))

        subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Análisis Forense",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            text_color="#0078D7"
        )
        subtitle_label.pack(pady=(0, 5))

        tech_label = ctk.CTkLabel(
            self.header_frame,
            text="Rene Parra",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color="gray"
        )
        tech_label.pack(pady=(0, 10))

    def _create_control_panel(self, parent):
        """Crea el panel de control compacto con fuentes más grandes"""
        self.control_frame = ctk.CTkFrame(parent)
        case_config_frame = ctk.CTkFrame(self.control_frame)
        case_config_frame.pack(fill="x", padx=8, pady=8)

        case_title = ctk.CTkLabel(
            case_config_frame,
            text="⚙️ Configuración",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI")
        )
        case_title.pack(pady=(10, 6))

        # ID del Caso
        ctk.CTkLabel(case_config_frame, text="ID:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(6, 2))
        ctk.CTkEntry(case_config_frame, textvariable=self.current_case_id, height=32, font=ctk.CTkFont(size=13)).pack(fill="x", padx=10, pady=(0, 6))

        # Tipo de Caso
        ctk.CTkLabel(case_config_frame, text="Tipo:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(6, 2))
        case_type_combo = ctk.CTkComboBox(
            case_config_frame,
            variable=self.case_type,
            values=[
                "employee_data_theft", "intellectual_property_theft", "malware_infection",
                "ransomware_attack", "financial_fraud"
            ],
            height=32,
            font=ctk.CTkFont(size=13)
        )
        case_type_combo.pack(fill="x", padx=10, pady=(0, 6))

        # Investigador
        ctk.CTkLabel(case_config_frame, text="Investigador:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(6, 2))
        ctk.CTkEntry(case_config_frame, textvariable=self.investigator_name, height=32, font=ctk.CTkFont(size=13)).pack(fill="x", padx=10, pady=(0, 6))

        # Tipo de evidencia
        evidence_frame = ctk.CTkFrame(case_config_frame)
        evidence_frame.pack(fill="x", padx=10, pady=(12, 6))

        ctk.CTkLabel(evidence_frame, text="Evidencia:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=5, pady=(0, 4))
        ctk.CTkRadioButton(evidence_frame, text="Sintético", variable=self.evidence_type, value="synthetic", width=80).pack(side="left", padx=5)
        ctk.CTkRadioButton(evidence_frame, text="Real", variable=self.evidence_type, value="real", width=80).pack(side="left", padx=5)

        # Botón de selección de imagen
        select_image_btn = ctk.CTkButton(
            case_config_frame,
            text="📁 Imagen",
            command=self._select_forensic_image,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        select_image_btn.pack(fill="x", padx=10, pady=(12, 6))

        self.image_path_label = ctk.CTkLabel(
            case_config_frame,
            text="Ninguna",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.image_path_label.pack(pady=(0, 10))

        # Acciones
        action_frame = ctk.CTkFrame(case_config_frame)
        action_frame.pack(fill="x", padx=10, pady=(12, 10))

        self.analyze_btn = ctk.CTkButton(
            action_frame,
            text="🔍 Análisis",
            command=self._start_comprehensive_analysis,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.analyze_btn.pack(fill="x", pady=4)

        self.ai_btn = ctk.CTkButton(
            action_frame,
            text="🤖 IA",
            command=self._start_ai_analysis,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.ai_btn.pack(fill="x", pady=4)

        self.report_btn = ctk.CTkButton(
            action_frame,
            text="📄 Reporte",
            command=self._generate_report,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.report_btn.pack(fill="x", pady=4)

        clear_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Limpiar",
            command=self._clear_results,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        clear_btn.pack(fill="x", pady=4)

    def _create_results_section(self, parent):
        """Crea la sección de resultados extendida"""
        self.results_frame = ctk.CTkFrame(parent)
        results_title = ctk.CTkLabel(
            self.results_frame,
            text="📊 Resultados del Análisis",
            font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI")
        )
        results_title.pack(pady=(12, 10))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook.Tab',
                       padding=[20, 12],
                       font=('Segoe UI', 14, 'bold'),
                       foreground='black',
                       background='#e0e0e0')
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', '#0078D7'), ('active', '#005a9e')],
                 foreground=[('selected', 'white'), ('active', 'white')])

        notebook_container = ctk.CTkFrame(self.results_frame)
        notebook_container.pack(fill="both", expand=True, padx=8, pady=8)

        self.notebook = ttk.Notebook(notebook_container, style='Custom.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)

        self._create_summary_tab()
        self._create_files_tab()
        self._create_network_tab()
        self._create_ai_tab()

    def _create_summary_tab(self):
        """Pestaña de resumen"""
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="🏠 RESUMEN")

        main_summary = ctk.CTkScrollableFrame(summary_frame)
        main_summary.pack(fill="both", expand=True, padx=10, pady=10)

        metrics_title = ctk.CTkLabel(
            main_summary,
            text="📈 Métricas Principales",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI")
        )
        metrics_title.pack(pady=12)

        metrics_grid = ctk.CTkFrame(main_summary)
        metrics_grid.pack(fill="x", padx=15, pady=12)

        self.metrics_vars = {
            'total_files': tk.StringVar(value="0"),
            'suspicious_files': tk.StringVar(value="0"),
            'total_connections': tk.StringVar(value="0"),
            'suspicious_connections': tk.StringVar(value="0"),
            'risk_level': tk.StringVar(value="N/A"),
            'risk_score': tk.StringVar(value="0/100")
        }

        metrics_info = [
            ("📁 Archivos", 'total_files', "#0078D7"),
            ("⚠️ Sospechosos", 'suspicious_files', "#D83B01"),
            ("🌐 Conexiones", 'total_connections', "#107C10"),
            ("🚨 Sospechosas", 'suspicious_connections', "#FF8C00"),
            ("🎯 Riesgo", 'risk_level', "#7951A8"),
            ("📊 Puntaje", 'risk_score', "#00B294")
        ]

        for i, (label_text, var_key, color) in enumerate(metrics_info):
            row = i // 3
            col = i % 3
            metric_frame = ctk.CTkFrame(metrics_grid)
            metric_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew", ipady=20)
            ctk.CTkLabel(
                metric_frame,
                text=label_text,
                font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
                text_color="gray"
            ).pack(pady=(6, 3))
            ctk.CTkLabel(
                metric_frame,
                textvariable=self.metrics_vars[var_key],
                font=ctk.CTkFont(size=28, weight="bold", family="Segoe UI"),
                text_color=color
            ).pack(pady=(0, 6))

        for i in range(3):
            metrics_grid.grid_columnconfigure(i, weight=1)
        for i in range(2):
            metrics_grid.grid_rowconfigure(i, minsize=110)

        risk_title = ctk.CTkLabel(
            main_summary,
            text="⚠️ Factores de Riesgo",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI")
        )
        risk_title.pack(pady=12)

        self.risk_factors_text = ctk.CTkTextbox(
            main_summary,
            height=180,
            font=ctk.CTkFont(size=14, family="Segoe UI")
        )
        self.risk_factors_text.pack(fill="x", padx=15, pady=(0, 18))

    def _create_files_tab(self):
        """Pestaña de archivos"""
        files_frame = ttk.Frame(self.notebook)
        self.notebook.add(files_frame, text="📁 ARCHIVOS")

        files_main = ctk.CTkScrollableFrame(files_frame)
        files_main.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(
            files_main,
            text="📁 Análisis Detallado del Sistema de Archivos",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI")
        )
        title_label.pack(pady=(10, 12))

        self.files_info_text = ctk.CTkTextbox(
            files_main,
            height=500,
            font=ctk.CTkFont(size=14, family="Consolas")
        )
        self.files_info_text.pack(fill="both", expand=True, padx=10, pady=(0, 18))

    def _create_network_tab(self):
        """Pestaña de red"""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="🌐 RED")

        network_main = ctk.CTkScrollableFrame(network_frame)
        network_main.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(
            network_main,
            text="🌐 Análisis Detallado de Actividad de Red",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI")
        )
        title_label.pack(pady=(10, 12))

        self.network_info_text = ctk.CTkTextbox(
            network_main,
            height=500,
            font=ctk.CTkFont(size=14, family="Consolas")
        )
        self.network_info_text.pack(fill="both", expand=True, padx=10, pady=(0, 18))

    def _create_ai_tab(self):
        """Pestaña de IA"""
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="🤖 IA")

        ai_main = ctk.CTkFrame(ai_frame)
        ai_main.pack(fill="both", expand=True, padx=10, pady=10)

        ai_title = ctk.CTkLabel(
            ai_main,
            text="🤖 Análisis con Inteligencia Artificial",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI")
        )
        ai_title.pack(pady=(12, 10))

        ai_subtitle = ctk.CTkLabel(
            ai_main,
            text="Llama 3.1 8B Local",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            text_color="#0078D7"
        )
        ai_subtitle.pack(pady=(0, 12))

        ai_buttons_frame = ctk.CTkFrame(ai_main)
        ai_buttons_frame.pack(fill="x", padx=10, pady=10)

        ai_buttons = [
            ("📋 Resumen", self._ai_executive_summary, "#0078D7"),
            ("⏰ Temporal", self._ai_temporal_analysis, "#D83B01"),
            ("🌐 Red", self._ai_network_analysis, "#107C10"),
            ("💡 Recomend.", self._ai_recommendations, "#FF8C00"),
            ("📝 Narrativo", self._ai_narrative_report, "#7951A8")
        ]

        for i, (text, command, color) in enumerate(ai_buttons):
            btn = ctk.CTkButton(
                ai_buttons_frame,
                text=text,
                command=command,
                width=130,
                height=35,
                font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
                fg_color=color,
                hover_color=self._darken_color(color)
            )
            btn.grid(row=0, column=i, padx=6, pady=6, sticky="ew")

        for i in range(5):
            ai_buttons_frame.grid_columnconfigure(i, weight=1)

        custom_frame = ctk.CTkFrame(ai_main)
        custom_frame.pack(fill="x", padx=10, pady=12)

        ctk.CTkLabel(
            custom_frame,
            text="💬 Consulta Personalizada:",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI")
        ).pack(anchor="w", padx=10, pady=(10, 6))

        query_frame = ctk.CTkFrame(custom_frame)
        query_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.custom_query_entry = ctk.CTkEntry(
            query_frame,
            placeholder_text="Ej: ¿Esto confirma robo de datos?",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            height=35
        )
        self.custom_query_entry.pack(side="left", fill="x", expand=True, padx=(5, 5), pady=5)

        ask_btn = ctk.CTkButton(
            query_frame,
            text="❓",
            command=self._ai_custom_question,
            width=70,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        ask_btn.pack(side="right", padx=5, pady=5)

        response_label = ctk.CTkLabel(
            ai_main,
            text="📋 Respuesta de la IA:",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI")
        )
        response_label.pack(anchor="w", padx=10, pady=(12, 6))

        self.ai_response_text = ctk.CTkTextbox(
            ai_main,
            height=280,
            font=ctk.CTkFont(size=14, family="Segoe UI")
        )
        self.ai_response_text.pack(fill="both", expand=True, padx=10, pady=(0, 12))

    def _darken_color(self, hex_color):
        """Oscurece un color hex para hover"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"

    def _create_log_section(self, parent):
        """Crea el log dentro del panel izquierdo"""
        self.log_frame = ctk.CTkFrame(parent)
        log_title = ctk.CTkLabel(
            self.log_frame,
            text="📋 Log",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI")
        )
        log_title.pack(pady=(6, 3))
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=130,
            font=ctk.CTkFont(size=13, family="Consolas")
        )
        self.log_text.pack(fill="x", padx=6, pady=(0, 6))

    def _initialize_components(self):
        """Inicializa los componentes del sistema"""
        try:
            self.data_generator = EnhancedForensicDataGenerator()
            self.analyzer = EnhancedForensicAnalyzer()
            self.ai_assistant = EnhancedForensicAIAssistant()
            if self.ai_assistant.is_ollama_available:
                self._log_message("✅ Todos los componentes inicializados correctamente")
            else:
                self._log_message("⚠️ IA no disponible - Ollama no encontrado")
        except Exception as e:
            self._log_message(f"❌ Error inicializando componentes: {e}")

    def _log_message(self, message: str):
        """Agrega mensaje al log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        logger.info(message)

    # === ✅ FUNCIÓN FALTANTE AÑADIDA AQUÍ ===
    def _select_forensic_image(self):
        """Selecciona imagen forense"""
        file_types = [
            ("Imágenes Forenses", "*.001 *.dd *.e01 *.raw"),
            ("Archivos DD", "*.dd"),
            ("Archivos E01", "*.e01"),
            ("Todos los archivos", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Seleccionar Imagen Forense",
            filetypes=file_types,
            initialdir="C:/ForensicAI/casos_reales/imagenes_forenses"
        )
        if filename:
            self.selected_image_path.set(filename)
            self.image_path_label.configure(
                text=f"Imagen: {os.path.basename(filename)}",
                text_color="green"
            )
            self._log_message(f"📁 Imagen seleccionada: {os.path.basename(filename)}")

    def _start_comprehensive_analysis(self):
        """Inicia análisis completo en hilo separado"""
        self.analyze_btn.configure(state="disabled", text="🔄 Analizando...")
        self._log_message("🔍 Iniciando análisis completo...")
        analysis_thread = threading.Thread(target=self._run_comprehensive_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()

    def _run_comprehensive_analysis(self):
        """Ejecuta el análisis completo"""
        try:
            if self.evidence_type.get() == "synthetic":
                self._log_message("📊 Generando caso sintético...")
                case = self.data_generator.generate_case(
                    case_type=self.case_type.get(),
                    case_id=self.current_case_id.get()
                )
                case_file = self.data_generator.save_case(case)
            else:
                self._log_message("⚠️ Procesamiento de evidencia real en desarrollo")
                return

            self._log_message("🔬 Ejecutando análisis forense...")
            self.current_analysis = self.analyzer.analyze_case(case_file)
            self.root.after(0, self._update_analysis_results)
        except Exception as e:
            error_msg = f"❌ Error en análisis: {str(e)}"
            self._log_message(error_msg)
            self.root.after(0, lambda: self._reset_analyze_button())

    def _update_analysis_results(self):
        """Actualiza la interfaz con resultados del análisis"""
        if not self.current_analysis:
            return
        try:
            summary = self.current_analysis['summary']
            risk = self.current_analysis['risk_assessment']

            self.metrics_vars['total_files'].set(str(summary.get('total_files_analyzed', 0)))
            self.metrics_vars['suspicious_files'].set(str(summary.get('suspicious_files_found', 0)))
            self.metrics_vars['total_connections'].set(str(summary.get('total_network_connections', 0)))
            self.metrics_vars['suspicious_connections'].set(str(summary.get('suspicious_connections_found', 0)))
            self.metrics_vars['risk_level'].set(risk.get('risk_level', 'N/A'))
            self.metrics_vars['risk_score'].set(f"{risk.get('overall_risk_score', 0)}/100")

            self.risk_factors_text.delete("1.0", "end")
            risk_factors = risk.get('risk_factors', [])
            for i, factor in enumerate(risk_factors, 1):
                self.risk_factors_text.insert("end", f"{i}. {factor}\n")

            self._update_files_tab()
            self._update_network_tab()

            self.ai_btn.configure(state="normal")
            self.report_btn.configure(state="normal")
            self._log_message("✅ Análisis completado exitosamente")
        except Exception as e:
            self._log_message(f"❌ Error actualizando resultados: {e}")
        finally:
            self._reset_analyze_button()

    def _update_files_tab(self):
        """Actualiza la pestaña de archivos"""
        if not self.current_analysis:
            return
        file_analysis = self.current_analysis.get('file_analysis', {})
        files_info = f"""
📁 ANÁLISIS DEL SISTEMA DE ARCHIVOS
═══════════════════════════════════════════
📊 Estadísticas Generales:
• Total de archivos: {file_analysis.get('total_files', 0)}
• Archivos sospechosos: {file_analysis.get('suspicious_files', 0)}
• Actividad fuera de horario: {file_analysis.get('after_hours_activity', 0)} eventos
• Archivos grandes (>100MB): {file_analysis.get('large_files_count', 0)}
• Herramientas de limpieza: {file_analysis.get('cleanup_tools', 0)}
📈 Distribución por Tipos:
"""
        file_types = file_analysis.get('file_types_distribution', {})
        for file_type, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
            files_info += f"• {file_type}: {count}\n"

        files_info += f"""
⏰ Distribución Horaria:
• Horas con más actividad: {self._get_peak_hours(file_analysis.get('hourly_distribution', {}))}
⚠️ Ubicaciones Sospechosas:
"""
        suspicious_locations = file_analysis.get('suspicious_locations', {})
        for location, count in suspicious_locations.items():
            files_info += f"• {location.title()}: {count} archivos\n"

        files_info += f"""
🎯 Puntuación de Riesgo: {file_analysis.get('risk_score', 0)}/100
        """
        self.files_info_text.delete("1.0", "end")
        self.files_info_text.insert("1.0", files_info)

    def _update_network_tab(self):
        """Actualiza la pestaña de red"""
        if not self.current_analysis:
            return
        network_analysis = self.current_analysis.get('network_analysis', {})
        network_info = f"""
🌐 ANÁLISIS DE ACTIVIDAD DE RED
═══════════════════════════════════════════
📊 Estadísticas Generales:
• Total de conexiones: {network_analysis.get('total_connections', 0)}
• Conexiones sospechosas: {network_analysis.get('suspicious_connections', 0)}
• Transferencias grandes: {network_analysis.get('large_transfers_count', 0)}
• Servicios en la nube: {network_analysis.get('cloud_services_count', 0)}
• Conexiones fuera de horario: {network_analysis.get('after_hours_connections', 0)}
📍 Principales Destinos:
"""
        destinations = network_analysis.get('destinations_distribution', {})
        for dest, count in list(destinations.items())[:5]:
            network_info += f"• {dest}: {count} conexiones\n"

        network_info += f"""
🔌 Puertos Más Utilizados:
"""
        ports = network_analysis.get('ports_distribution', {})
        for port, count in list(ports.items())[:5]:
            network_info += f"• Puerto {port}: {count} conexiones\n"

        network_info += f"""
📡 Protocolos:
"""
        protocols = network_analysis.get('protocols_distribution', {})
        for protocol, count in protocols.items():
            network_info += f"• {protocol}: {count} conexiones\n"

        network_info += f"""
💾 Transferencia Total de Datos: {self._format_bytes(network_analysis.get('total_bytes_transferred', 0))}
🎯 Puntuación de Riesgo: {network_analysis.get('risk_score', 0)}/100
        """
        self.network_info_text.delete("1.0", "end")
        self.network_info_text.insert("1.0", network_info)

    def _get_peak_hours(self, hourly_dist: Dict[int, int]) -> str:
        """Obtiene las horas de mayor actividad"""
        if not hourly_dist:
            return "N/A"
        sorted_hours = sorted(hourly_dist.items(), key=lambda x: x[1], reverse=True)
        top_3 = sorted_hours[:3]
        return ", ".join([f"{hour:02d}:00 ({count})" for hour, count in top_3])

    def _format_bytes(self, bytes_count: int) -> str:
        """Formatea bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.1f} PB"

    def _reset_analyze_button(self):
        """Resetea el botón de análisis"""
        self.analyze_btn.configure(state="normal", text="🔍 Iniciar Análisis Completo")

    def _start_ai_analysis(self):
        """Inicia análisis IA en hilo separado"""
        if not self.current_analysis:
            messagebox.showwarning("Advertencia", "Primero ejecuta el análisis forense")
            return
        if not self.ai_assistant.is_ollama_available:
            messagebox.showerror("Error", "IA no disponible. Verifica instalación de Ollama.")
            return
        self.ai_btn.configure(state="disabled", text="🔄 Analizando con IA...")
        self._log_message("🤖 Iniciando análisis IA...")
        ai_thread = threading.Thread(target=self._run_ai_analysis)
        ai_thread.daemon = True
        ai_thread.start()

    def _run_ai_analysis(self):
        """Ejecuta análisis IA completo"""
        try:
            self.current_ai_insights = self.ai_assistant.get_case_insights(self.current_analysis)
            case_id = self.current_analysis['case_info']['case_id']
            ai_file = self.ai_assistant.save_ai_analysis(self.current_ai_insights, case_id)
            self.root.after(0, self._update_ai_results)
        except Exception as e:
            error_msg = f"❌ Error en análisis IA: {str(e)}"
            self._log_message(error_msg)
            self.root.after(0, self._reset_ai_button)

    def _update_ai_results(self):
        """Actualiza resultados de IA"""
        try:
            if 'executive_summary' in self.current_ai_insights:
                summary = self.current_ai_insights['executive_summary']
                self.ai_response_text.delete("1.0", "end")
                self.ai_response_text.insert("1.0", f"📋 RESUMEN EJECUTIVO:\n{summary}")
            self._log_message("✅ Análisis IA completado")
        except Exception as e:
            self._log_message(f"❌ Error actualizando IA: {e}")
        finally:
            self._reset_ai_button()

    def _reset_ai_button(self):
        """Resetea botón de IA"""
        self.ai_btn.configure(state="normal", text="🤖 Análisis IA")

    def _ai_executive_summary(self):
        """Muestra resumen ejecutivo"""
        self._run_specific_ai_analysis('executive_summary', "📋 RESUMEN EJECUTIVO")

    def _ai_temporal_analysis(self):
        """Muestra análisis temporal"""
        self._run_specific_ai_analysis('temporal_analysis', "⏰ ANÁLISIS TEMPORAL")

    def _ai_network_analysis(self):
        """Muestra análisis de red"""
        self._run_specific_ai_analysis('network_analysis', "🌐 ANÁLISIS DE RED")

    def _ai_recommendations(self):
        """Muestra recomendaciones"""
        self._run_specific_ai_analysis('recommendations', "💡 RECOMENDACIONES")

    def _ai_narrative_report(self):
        """Genera reporte narrativo"""
        if not self.current_analysis:
            messagebox.showwarning("Advertencia", "Primero ejecuta el análisis forense")
            return
        self._log_message("📝 Generando reporte narrativo...")
        def generate_narrative():
            try:
                narrative = self.ai_assistant.generate_narrative_report(self.current_analysis)
                self.root.after(0, lambda: self._show_ai_result("📝 REPORTE NARRATIVO", narrative))
            except Exception as e:
                self._log_message(f"❌ Error generando narrativo: {e}")
        thread = threading.Thread(target=generate_narrative)
        thread.daemon = True
        thread.start()

    def _run_specific_ai_analysis(self, analysis_type: str, title: str):
        """Ejecuta análisis IA específico"""
        if not self.current_analysis:
            messagebox.showwarning("Advertencia", "Primero ejecuta el análisis forense")
            return
        if not self.ai_assistant.is_ollama_available:
            messagebox.showerror("Error", "IA no disponible")
            return
        if self.current_ai_insights and analysis_type in self.current_ai_insights:
            result = self.current_ai_insights[analysis_type]
            self._show_ai_result(title, result)
            return
        self._log_message(f"🤖 Generando {title.lower()}...")
        def generate_analysis():
            try:
                if analysis_type == 'executive_summary':
                    result = self.ai_assistant.generate_executive_summary(self.current_analysis)
                elif analysis_type == 'temporal_analysis':
                    result = self.ai_assistant.analyze_temporal_patterns(self.current_analysis)
                elif analysis_type == 'network_analysis':
                    result = self.ai_assistant.analyze_network_behavior(self.current_analysis)
                elif analysis_type == 'recommendations':
                    result = self.ai_assistant.generate_recommendations(self.current_analysis)
                else:
                    result = "Análisis no disponible"
                self.root.after(0, lambda: self._show_ai_result(title, result))
            except Exception as e:
                self._log_message(f"❌ Error en {analysis_type}: {e}")
        thread = threading.Thread(target=generate_analysis)
        thread.daemon = True
        thread.start()

    def _show_ai_result(self, title: str, content: str):
        """Muestra resultado de IA en la pestaña"""
        self.ai_response_text.delete("1.0", "end")
        self.ai_response_text.insert("1.0", f"{title}:\n{content}")
        self.notebook.select(3)  # Ir a pestaña IA

    def _ai_custom_question(self):
        """Procesa pregunta personalizada"""
        question = self.custom_query_entry.get().strip()
        if not question:
            messagebox.showwarning("Advertencia", "Escribe una pregunta")
            return
        if not self.ai_assistant.is_ollama_available:
            messagebox.showerror("Error", "IA no disponible")
            return
        self._log_message(f"❓ Consultando: {question[:30]}...")
        def ask_question():
            try:
                answer = self.ai_assistant.answer_custom_question(question, self.current_analysis)
                self.root.after(0, lambda: self._show_ai_result("💬 CONSULTA PERSONALIZADA", f"Pregunta: {question}\nRespuesta: {answer}"))
                self.root.after(0, lambda: self.custom_query_entry.delete(0, "end"))
            except Exception as e:
                self._log_message(f"❌ Error en consulta: {e}")
        thread = threading.Thread(target=ask_question)
        thread.daemon = True
        thread.start()

    def _generate_report(self):
        """Genera reporte completo con gráficos incluidos"""
        if not self.current_analysis:
            messagebox.showwarning("Advertencia", "Primero ejecuta el análisis forense")
            return
        try:
            reports_dir = "C:/ForensicAI/reportes"
            os.makedirs(reports_dir, exist_ok=True)
            case_id = self.current_analysis['case_info']['case_id']
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self._log_message("📄 Generando reporte completo con gráficos...")

            visualizations = self.analyzer.create_visualizations(
                self.current_analysis.get('file_analysis', {}),
                self.current_analysis.get('network_analysis', {}),
                reports_dir
            )

            html_filename = os.path.join(reports_dir, f"{case_id}_reporte_visual_{timestamp}.html")
            self._create_html_report(html_filename, visualizations)

            txt_filename = os.path.join(reports_dir, f"{case_id}_reporte_texto_{timestamp}.txt")
            report_content = self.analyzer.generate_summary_report(self.current_analysis)

            if self.current_ai_insights:
                report_content += "\n" + "=" * 60
                report_content += "\n📊 ANÁLISIS DE INTELIGENCIA ARTIFICIAL"
                report_content += "\n" + "=" * 60
                for insight_type, insight_content in self.current_ai_insights.items():
                    if insight_type != 'error':
                        title = insight_type.replace('_', ' ').title()
                        report_content += f"\n🤖 {title}:\n"
                        report_content += "-" * 40 + "\n"
                        report_content += insight_content[:1500]
                        if len(insight_content) > 1500:
                            report_content += "\n[... contenido truncado ...]"

            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self._log_message(f"✅ Reportes generados:")
            self._log_message(f"   📊 HTML: {os.path.basename(html_filename)}")
            self._log_message(f"   📄 TXT: {os.path.basename(txt_filename)}")

            choice = messagebox.askyesnocancel(
                "Reportes Generados",
                f"Reportes guardados exitosamente:\n"
                f"📊 Reporte Visual (HTML): {os.path.basename(html_filename)}\n"
                f"📄 Reporte Texto: {os.path.basename(txt_filename)}\n"
                f"¿Qué deseas hacer?\n"
                f"SÍ = Abrir reporte visual (HTML)\n"
                f"NO = Abrir carpeta de reportes\n"
                f"CANCELAR = Solo guardar"
            )
            if choice is True:
                webbrowser.open(f"file:///{html_filename.replace(os.sep, '/')}")
            elif choice is False:
                os.startfile(reports_dir)
        except Exception as e:
            error_msg = f"❌ Error generando reporte: {str(e)}"
            self._log_message(error_msg)
            messagebox.showerror("Error", error_msg)

    def _create_html_report(self, filename: str, visualizations: Dict[str, str]):
        """Crea reporte HTML con gráficos embebidos"""
        case_info = self.current_analysis['case_info']
        summary = self.current_analysis['summary']
        risk_assessment = self.current_analysis['risk_assessment']
        file_analysis = self.current_analysis.get('file_analysis', {})
        network_analysis = self.current_analysis.get('network_analysis', {})

        image_data = {}
        for viz_type, viz_path in visualizations.items():
            if os.path.exists(viz_path):
                import base64
                with open(viz_path, 'rb') as f:
                    image_data[viz_type] = base64.b64encode(f.read()).decode()

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Forense - {case_info['case_id']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .section h2 {{
            color: #2a5298;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .risk-level {{
            font-size: 1.5em;
            font-weight: bold;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin: 20px 0;
        }}
        .risk-critical {{
            background: #ff4757;
            color: white;
        }}
        .risk-high {{
            background: #ff6b35;
            color: white;
        }}
        .risk-medium {{
            background: #ffa502;
            color: white;
        }}
        .risk-low {{
            background: #7bed9f;
            color: white;
        }}
        .risk-minimal {{
            background: #2ed573;
            color: white;
        }}
        .risk-factors {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #ff4757;
        }}
        .risk-factors li {{
            margin: 8px 0;
            padding: 5px 0;
        }}
        .chart-container {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        .ai-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 25px;
            margin: 30px 0;
        }}
        .ai-section h3 {{
            margin-top: 0;
            color: white;
        }}
        .ai-content {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
        }}
        .timestamp {{
            text-align: right;
            color: #666;
            font-style: italic;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }}
        @media print {{
            body {{ background: white; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 REPORTE FORENSE DIGITAL</h1>
            <p>Análisis con Inteligencia Artificial | {case_info.get('analysis_timestamp', 'N/A')}</p>
        </div>
        <div class="content">
            <div class="section">
                <h2>📋 Información del Caso</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                    <div><strong>ID del Caso:</strong> {case_info.get('case_id', 'N/A')}</div>
                    <div><strong>Tipo:</strong> {case_info.get('case_type', 'N/A').replace('_', ' ').title()}</div>
                    <div><strong>Sospechoso:</strong> {case_info.get('suspect_name', 'N/A')}</div>
                    <div><strong>Fecha de Análisis:</strong> {case_info.get('analysis_timestamp', 'N/A')}</div>
                </div>
            </div>
            <div class="section">
                <h2>📊 Métricas Principales</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('total_files_analyzed', 0)}</div>
                        <div class="metric-label">Archivos Analizados</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('suspicious_files_found', 0)}</div>
                        <div class="metric-label">Archivos Sospechosos</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('total_network_connections', 0)}</div>
                        <div class="metric-label">Conexiones de Red</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('suspicious_connections_found', 0)}</div>
                        <div class="metric-label">Conexiones Sospechosas</div>
                    </div>
                </div>
                <div class="risk-level risk-{risk_assessment.get('risk_level', 'minimal').lower()}">
                    🎯 NIVEL DE RIESGO: {risk_assessment.get('risk_level', 'N/A')} 
                    ({risk_assessment.get('overall_risk_score', 0)}/100)
                </div>
            </div>
            <div class="section">
                <h2>⚠️ Factores de Riesgo Detectados</h2>
                <div class="risk-factors">
                    <ul>"""
        for factor in risk_assessment.get('risk_factors', []):
            html_content += f"<li>{factor}</li>"
        html_content += """
                    </ul>
                </div>
            </div>
            <div class="section">
                <h2>📈 Visualizaciones del Análisis</h2>"""
        if 'overview' in image_data:
            html_content += f"""
                <div class="chart-container">
                    <h3>📊 Resumen General del Análisis</h3>
                    <img src="data:image/png;base64,{image_data['overview']}" alt="Resumen General">
                </div>"""
        if 'risk_indicators' in image_data:
            html_content += f"""
                <div class="chart-container">
                    <h3>🎯 Indicadores de Riesgo</h3>
                    <img src="data:image/png;base64,{image_data['risk_indicators']}" alt="Indicadores de Riesgo">
                </div>"""
        html_content += """
            </div>
            <div class="section">
                <h2>🔍 Análisis Detallado</h2>
                <h3>📁 Sistema de Archivos</h3>
                <ul>"""
        html_content += f"""
                    <li><strong>Actividad fuera de horario:</strong> {file_analysis.get('after_hours_activity', 0)} eventos</li>
                    <li><strong>Archivos grandes (>100MB):</strong> {file_analysis.get('large_files_count', 0)}</li>
                    <li><strong>Herramientas de limpieza:</strong> {file_analysis.get('cleanup_tools', 0)}</li>
                    <li><strong>Puntuación de riesgo:</strong> {file_analysis.get('risk_score', 0)}/100</li>
                </ul>
                <h3>🌐 Actividad de Red</h3>
                <ul>
                    <li><strong>Transferencias grandes:</strong> {network_analysis.get('large_transfers_count', 0)}</li>
                    <li><strong>Servicios en la nube:</strong> {network_analysis.get('cloud_services_count', 0)}</li>
                    <li><strong>Conexiones fuera de horario:</strong> {network_analysis.get('after_hours_connections', 0)}</li>
                    <li><strong>Puntuación de riesgo:</strong> {network_analysis.get('risk_score', 0)}/100</li>
                </ul>
            </div>"""
        if self.current_ai_insights:
            html_content += """
            <div class="ai-section">
                <h2>🤖 Análisis de Inteligencia Artificial</h2>"""
            for insight_type, insight_content in self.current_ai_insights.items():
                if insight_type != 'error':
                    title = insight_type.replace('_', ' ').title()
                    content = insight_content[:800] + "..." if len(insight_content) > 800 else insight_content
                    content = content.replace('\n', '<br>')
                    html_content += f"""
                <div class="ai-content">
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>"""
            html_content += "</div>"
        html_content += f"""
        </div>
        <div class="footer">
            <p><strong>Asistente Forense IA v2.0</strong> | Generado con Llama 3.1 8B Local</p>
            <div class="timestamp">
                Reporte generado el {datetime.datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}
            </div>
        </div>
    </div>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self._log_message(f"✅ Reporte HTML generado: {os.path.basename(filename)}")

    def _clear_results(self):
        """Limpia todos los resultados"""
        for var in self.metrics_vars.values():
            if var != self.metrics_vars['risk_level']:
                var.set("0")
            else:
                var.set("N/A")
        self.metrics_vars['risk_score'].set("0/100")
        text_widgets = [
            self.risk_factors_text,
            self.files_info_text,
            self.network_info_text,
            self.ai_response_text
        ]
        for widget in text_widgets:
            widget.delete("1.0", "end")
        self.current_analysis = None
        self.current_ai_insights = None
        self.ai_btn.configure(state="disabled")
        self.report_btn.configure(state="disabled")
        self.current_case_id.set(self._generate_case_id())
        self.selected_image_path.set("")
        self.image_path_label.configure(
            text="Ninguna imagen seleccionada",
            text_color="gray"
        )
        self._log_message("🗑️ Resultados limpiados - Listo para nuevo análisis")

    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Aplicación cerrada por usuario")
        except Exception as e:
            logger.error(f"Error en aplicación: {e}")


def main():
    """Función principal"""
    print("🚀 Iniciando Asistente Forense IA - Interfaz Gráfica")
    try:
        directories = [
            "C:/ForensicAI/logs",
            "C:/ForensicAI/reportes",
            "C:/ForensicAI/casos_reales/casos_procesados",
            "C:/ForensicAI/casos_reales/imagenes_forenses"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        app = ForensicGUIApplication()
        print("✅ Interfaz gráfica iniciada exitosamente")
        print("🔍 Sistema listo para análisis forense con IA")
        app.run()
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        logger.error(f"Error en main: {e}")


if __name__ == "__main__":
    main()