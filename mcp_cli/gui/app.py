#!/usr/bin/env python3
"""
GUI Application for MCP CLI.
"""

import asyncio
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QTabWidget, QPushButton, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QMessageBox, QListWidget, QFormLayout,
    QListWidgetItem, QDialog, QGroupBox, QCheckBox, QDialogButtonBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

# Import MCP CLI functions
from mcp_cli.core import (
    load_config, save_config, list_servers, run_query,
    add_server, remove_server, export_config, import_config,
    get_server_info, list_tools, DEFAULT_MODEL
)

class AsyncWorker(QThread):
    """Worker thread to run async tasks."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        self.running = True
    
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.coro) if self.running else None
            loop.close()
            if self.running:
                self.finished.emit(result if result else "Operation completed successfully.")
        except Exception as e:
            if self.running:
                self.error.emit(str(e))
    
    def stop(self):
        """Stop the thread safely."""
        self.running = False
        self.wait()


class AddServerDialog(QDialog):
    """Dialog for adding a new MCP server."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add MCP Server")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Server details
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        form_layout.addRow("Server Name:", self.name_edit)
        
        self.command_edit = QLineEdit()
        form_layout.addRow("Command:", self.command_edit)
        
        self.args_edit = QLineEdit()
        form_layout.addRow("Arguments:", self.args_edit)
        
        # Environment variables
        env_group = QGroupBox("Environment Variables")
        env_layout = QVBoxLayout()
        
        self.env_list = QListWidget()
        add_env_button = QPushButton("Add Variable")
        add_env_button.clicked.connect(self.add_env_var)
        remove_env_button = QPushButton("Remove Variable")
        remove_env_button.clicked.connect(self.remove_env_var)
        
        env_buttons_layout = QHBoxLayout()
        env_buttons_layout.addWidget(add_env_button)
        env_buttons_layout.addWidget(remove_env_button)
        
        env_layout.addWidget(self.env_list)
        env_layout.addLayout(env_buttons_layout)
        env_group.setLayout(env_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(env_group)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def add_env_var(self):
        """Add a new environment variable to the list."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Environment Variable")
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        key_edit = QLineEdit()
        value_edit = QLineEdit()
        form_layout.addRow("Key:", key_edit)
        form_layout.addRow("Value:", value_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            key = key_edit.text().strip()
            value = value_edit.text().strip()
            if key:
                self.env_list.addItem(f"{key}={value}")
    
    def remove_env_var(self):
        """Remove the selected environment variable from the list."""
        selected_items = self.env_list.selectedItems()
        for item in selected_items:
            self.env_list.takeItem(self.env_list.row(item))
    
    def get_server_config(self):
        """Get the server configuration from the dialog."""
        name = self.name_edit.text().strip()
        command = self.command_edit.text().strip()
        args = self.args_edit.text().strip().split()
        
        env_dict = {}
        for i in range(self.env_list.count()):
            key_value = self.env_list.item(i).text()
            key, value = key_value.split("=", 1)
            env_dict[key] = value
        
        return {
            "name": name,
            "command": command,
            "args": args,
            "env": env_dict if env_dict else None
        }


class EditServerDialog(QDialog):
    """Dialog for editing an existing MCP server."""
    
    def __init__(self, parent=None, server_name=None, server_config=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Server: {server_name}")
        self.setMinimumWidth(500)
        self.server_name = server_name
        self.server_config = server_config
        
        layout = QVBoxLayout()
        
        # Server details
        form_layout = QFormLayout()
        
        self.command_edit = QLineEdit(self.server_config.get("command", ""))
        form_layout.addRow("Command:", self.command_edit)
        
        self.args_edit = QLineEdit(" ".join(self.server_config.get("args", [])))
        form_layout.addRow("Arguments:", self.args_edit)
        
        # Environment variables
        env_group = QGroupBox("Environment Variables")
        env_layout = QVBoxLayout()
        
        self.env_list = QListWidget()
        # Add existing env variables
        env_vars = self.server_config.get("env", {})
        for key, value in env_vars.items():
            self.env_list.addItem(f"{key}={value}")
        
        add_env_button = QPushButton("Add Variable")
        add_env_button.clicked.connect(self.add_env_var)
        edit_env_button = QPushButton("Edit Variable")
        edit_env_button.clicked.connect(self.edit_env_var)
        remove_env_button = QPushButton("Remove Variable")
        remove_env_button.clicked.connect(self.remove_env_var)
        
        env_buttons_layout = QHBoxLayout()
        env_buttons_layout.addWidget(add_env_button)
        env_buttons_layout.addWidget(edit_env_button)
        env_buttons_layout.addWidget(remove_env_button)
        
        env_layout.addWidget(self.env_list)
        env_layout.addLayout(env_buttons_layout)
        env_group.setLayout(env_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(env_group)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def add_env_var(self):
        """Add a new environment variable to the list."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Environment Variable")
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        key_edit = QLineEdit()
        value_edit = QLineEdit()
        form_layout.addRow("Key:", key_edit)
        form_layout.addRow("Value:", value_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            key = key_edit.text().strip()
            value = value_edit.text().strip()
            if key:
                self.env_list.addItem(f"{key}={value}")
    
    def edit_env_var(self):
        """Edit the selected environment variable."""
        selected_items = self.env_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No environment variable selected")
            return
        
        item = selected_items[0]
        key_value = item.text()
        key, value = key_value.split("=", 1)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Environment Variable")
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        key_edit = QLineEdit(key)
        value_edit = QLineEdit(value)
        form_layout.addRow("Key:", key_edit)
        form_layout.addRow("Value:", value_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            new_key = key_edit.text().strip()
            new_value = value_edit.text().strip()
            if new_key:
                item.setText(f"{new_key}={new_value}")
    
    def remove_env_var(self):
        """Remove the selected environment variable from the list."""
        selected_items = self.env_list.selectedItems()
        for item in selected_items:
            self.env_list.takeItem(self.env_list.row(item))
    
    def get_server_config(self):
        """Get the server configuration from the dialog."""
        command = self.command_edit.text().strip()
        args = self.args_edit.text().strip().split()
        
        env_dict = {}
        for i in range(self.env_list.count()):
            key_value = self.env_list.item(i).text()
            key, value = key_value.split("=", 1)
            env_dict[key] = value
        
        return {
            "command": command,
            "args": args,
            "env": env_dict if env_dict else None
        }


class MCPCliGui(QMainWindow):
    """Main window for the MCP CLI GUI application."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MCP CLI GUI")
        self.setMinimumSize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add tabs
        self.create_servers_tab(tabs)
        self.create_run_query_tab(tabs)
        self.create_tools_tab(tabs)
        self.create_config_tab(tabs)
        
        main_layout.addWidget(tabs)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Track active threads
        self.active_threads = []
        
        # Initialize server list
        self.refresh_server_list()
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop all active threads before closing
        for thread in self.active_threads:
            if thread.isRunning():
                thread.stop()
        
        # Accept the close event
        event.accept()
    
    def create_servers_tab(self, tabs):
        """Create the Servers tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Servers list
        self.servers_list = QListWidget()
        self.servers_list.itemClicked.connect(self.show_server_info)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Server")
        add_button.clicked.connect(self.add_server_dialog)
        
        edit_button = QPushButton("Edit Server")
        edit_button.clicked.connect(self.edit_server_action)
        
        remove_button = QPushButton("Remove Server")
        remove_button.clicked.connect(self.remove_server_action)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_server_list)
        
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addWidget(refresh_button)
        
        # Server info
        self.server_info = QTextEdit()
        self.server_info.setReadOnly(True)
        
        layout.addWidget(QLabel("Configured MCP Servers:"))
        layout.addWidget(self.servers_list)
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("Server Information:"))
        layout.addWidget(self.server_info)
        
        tab.setLayout(layout)
        tabs.addTab(tab, "Servers")
    
    def create_run_query_tab(self, tabs):
        """Create the Run Query tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Server selection
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("Server:"))
        self.query_server_combo = QComboBox()
        server_layout.addWidget(self.query_server_combo)
        
        # Model selection
        server_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        self.model_combo.setCurrentText(DEFAULT_MODEL)
        server_layout.addWidget(self.model_combo)
        
        # Query input
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Enter your query here...")
        
        # Run button
        run_button = QPushButton("Run Query")
        run_button.clicked.connect(self.run_query_action)
        
        # Results
        self.query_results = QTextEdit()
        self.query_results.setReadOnly(True)
        
        layout.addLayout(server_layout)
        layout.addWidget(QLabel("Query:"))
        layout.addWidget(self.query_input)
        layout.addWidget(run_button)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.query_results)
        
        tab.setLayout(layout)
        tabs.addTab(tab, "Run Query")
    
    def create_tools_tab(self, tabs):
        """Create the Tools tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Server selection
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("Server:"))
        self.tools_server_combo = QComboBox()
        server_layout.addWidget(self.tools_server_combo)
        
        # Model selection
        server_layout.addWidget(QLabel("Model:"))
        self.tools_model_combo = QComboBox()
        self.tools_model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        self.tools_model_combo.setCurrentText(DEFAULT_MODEL)
        server_layout.addWidget(self.tools_model_combo)
        
        # List button
        list_button = QPushButton("List Tools")
        list_button.clicked.connect(self.list_tools_action)
        
        # Tools results
        self.tools_results = QTextEdit()
        self.tools_results.setReadOnly(True)
        
        layout.addLayout(server_layout)
        layout.addWidget(list_button)
        layout.addWidget(QLabel("Available Tools:"))
        layout.addWidget(self.tools_results)
        
        tab.setLayout(layout)
        tabs.addTab(tab, "Tools")
    
    def create_config_tab(self, tabs):
        """Create the Configuration tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Export/Import
        config_layout = QHBoxLayout()
        
        self.export_path = QLineEdit()
        self.export_path.setPlaceholderText("Path to export configuration...")
        export_button = QPushButton("Export Config")
        export_button.clicked.connect(self.export_config_action)
        
        self.import_path = QLineEdit()
        self.import_path.setPlaceholderText("Path to import configuration...")
        import_button = QPushButton("Import Config")
        import_button.clicked.connect(self.import_config_action)
        
        export_layout = QVBoxLayout()
        export_layout.addWidget(QLabel("Export Configuration:"))
        export_layout.addWidget(self.export_path)
        export_layout.addWidget(export_button)
        
        import_layout = QVBoxLayout()
        import_layout.addWidget(QLabel("Import Configuration:"))
        import_layout.addWidget(self.import_path)
        import_layout.addWidget(import_button)
        
        config_layout.addLayout(export_layout)
        config_layout.addLayout(import_layout)
        
        layout.addLayout(config_layout)
        
        tab.setLayout(layout)
        tabs.addTab(tab, "Configuration")
    
    def refresh_server_list(self):
        """Refresh the list of servers in all tabs."""
        try:
            # Clear lists
            self.servers_list.clear()
            self.query_server_combo.clear()
            self.tools_server_combo.clear()
            
            # Get servers from config
            config = load_config()
            servers = config.get("mcpServers", {})
            
            if not servers:
                return
            
            # Add servers to list and combos
            for name, server_config in servers.items():
                command = server_config.get("command", "N/A")
                args = " ".join(server_config.get("args", []))
                display_text = f"{name}: {command} {args}"
                
                self.servers_list.addItem(display_text)
                self.query_server_combo.addItem(name)
                self.tools_server_combo.addItem(name)
            
            self.statusBar().showMessage("Server list refreshed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh server list: {str(e)}")
    
    def show_server_info(self, item):
        """Show information about the selected server."""
        if not item:
            return
        
        server_name = item.text().split(":", 1)[0]
        
        try:
            # Get server info from config
            config = load_config()
            servers = config.get("mcpServers", {})
            
            if server_name not in servers:
                return
            
            server_config = servers[server_name]
            command = server_config.get("command", "N/A")
            args = " ".join(server_config.get("args", []))
            
            # Format server info
            info_text = f"Server: {server_name}\n"
            info_text += f"Command: {command}\n"
            info_text += f"Arguments: {args}\n"
            
            if "env" in server_config:
                info_text += "\nEnvironment variables:\n"
                for key, value in server_config["env"].items():
                    info_text += f"  {key}={value}\n"
            
            self.server_info.setText(info_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get server info: {str(e)}")
    
    def add_server_dialog(self):
        """Show dialog to add a new server."""
        dialog = AddServerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            server_config = dialog.get_server_config()
            try:
                add_server(
                    server_config["name"],
                    server_config["command"],
                    server_config["args"],
                    server_config["env"]
                )
                self.refresh_server_list()
                self.statusBar().showMessage(f"Server '{server_config['name']}' added successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add server: {str(e)}")
    
    def remove_server_action(self):
        """Remove the selected server."""
        selected_items = self.servers_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No server selected")
            return
        
        server_name = selected_items[0].text().split(":", 1)[0]
        
        reply = QMessageBox.question(
            self, "Confirm Removal",
            f"Are you sure you want to remove the server '{server_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                remove_server(server_name)
                self.refresh_server_list()
                self.statusBar().showMessage(f"Server '{server_name}' removed successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove server: {str(e)}")
    
    def run_query_action(self):
        """Run a query against the selected server."""
        server_name = self.query_server_combo.currentText()
        if not server_name:
            QMessageBox.warning(self, "Warning", "No server selected")
            return
        
        query = self.query_input.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "Warning", "Query is empty")
            return
        
        model = self.model_combo.currentText()
        
        self.statusBar().showMessage(f"Running query on server '{server_name}'...")
        self.query_results.clear()
        self.query_results.setText("Processing query, please wait...")
        
        # Create worker thread
        worker = AsyncWorker(run_query(server_name, query, model, return_result=True))
        worker.finished.connect(self.handle_query_results)
        worker.error.connect(self.handle_query_error)
        
        # Add to active threads
        self.active_threads.append(worker)
        
        # Start the thread
        worker.start()
    
    def handle_query_results(self, result):
        """Handle the results of a query."""
        self.query_results.setText(result)
        self.statusBar().showMessage("Query completed")
    
    def handle_query_error(self, error_message):
        """Handle an error that occurred during a query."""
        self.query_results.setText(f"Error: {error_message}")
        self.statusBar().showMessage("Query failed")
    
    def list_tools_action(self):
        """List tools available from the selected server."""
        server_name = self.tools_server_combo.currentText()
        if not server_name:
            QMessageBox.warning(self, "Warning", "No server selected")
            return
        
        model = self.tools_model_combo.currentText()
        
        self.statusBar().showMessage(f"Listing tools for server '{server_name}'...")
        self.tools_results.clear()
        self.tools_results.setText("Retrieving tools, please wait...")
        
        # Create worker thread
        worker = AsyncWorker(list_tools(server_name, model, return_result=True))
        worker.finished.connect(self.handle_tools_results)
        worker.error.connect(self.handle_tools_error)
        
        # Add to active threads
        self.active_threads.append(worker)
        
        # Start the thread
        worker.start()
    
    def handle_tools_results(self, result):
        """Handle the results of a tools listing."""
        self.tools_results.setText(result)
        self.statusBar().showMessage("Tools listed successfully")
    
    def handle_tools_error(self, error_message):
        """Handle an error that occurred during a tools listing."""
        self.tools_results.setText(f"Error: {error_message}")
        self.statusBar().showMessage("Failed to list tools")
    
    def export_config_action(self):
        """Export configuration to a file."""
        filepath = self.export_path.text().strip()
        if not filepath:
            QMessageBox.warning(self, "Warning", "Export path is empty")
            return
        
        try:
            export_config(filepath)
            self.statusBar().showMessage(f"Configuration exported to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export configuration: {str(e)}")
    
    def import_config_action(self):
        """Import configuration from a file."""
        filepath = self.import_path.text().strip()
        if not filepath:
            QMessageBox.warning(self, "Warning", "Import path is empty")
            return
        
        if not os.path.exists(filepath):
            QMessageBox.critical(self, "Error", f"File '{filepath}' not found")
            return
        
        try:
            import_config(filepath)
            self.refresh_server_list()
            self.statusBar().showMessage(f"Configuration imported from {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import configuration: {str(e)}")

    def edit_server_action(self):
        """Edit the selected server."""
        selected_items = self.servers_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No server selected")
            return
        
        server_name = selected_items[0].text().split(":", 1)[0]
        
        try:
            # Get server info from config
            config = load_config()
            servers = config.get("mcpServers", {})
            
            if server_name not in servers:
                QMessageBox.warning(self, "Warning", f"Server '{server_name}' not found")
                return
            
            server_config = servers[server_name]
            
            # Show edit dialog
            dialog = EditServerDialog(self, server_name, server_config)
            if dialog.exec_() == QDialog.Accepted:
                updated_config = dialog.get_server_config()
                
                # Update config
                config["mcpServers"][server_name] = updated_config
                save_config(config)
                
                # Refresh
                self.refresh_server_list()
                self.statusBar().showMessage(f"Server '{server_name}' updated successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit server: {str(e)}")


def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    window = MCPCliGui()
    window.show()
    sys.exit(app.exec_()) 