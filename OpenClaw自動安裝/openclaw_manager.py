from __future__ import annotations

import json
import queue
import re
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from urllib.parse import urlsplit, urlunsplit
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk


def get_app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


APP_ROOT = get_app_root()
HELPER_SCRIPT = APP_ROOT / "scripts" / "openclaw_helper.ps1"
DEFAULT_PORT = "18789"


class OpenClawManagerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("OpenClaw 自動安裝與控制工具")
        self.geometry("1080x760")
        self.minsize(980, 700)

        self.shell_executable = self._detect_shell_executable()
        self.log_queue: queue.Queue[str] = queue.Queue()
        self.gateway_process: subprocess.Popen[str] | None = None
        self.task_running = False
        self.gateway_executable_path: str | None = None

        self.status_text = tk.StringVar(value="準備就緒")
        self.port_var = tk.StringVar(value=DEFAULT_PORT)
        self.gateway_state_var = tk.StringVar(value="未知")
        self.node_var = tk.StringVar(value="未檢查")
        self.npm_var = tk.StringVar(value="未檢查")
        self.git_var = tk.StringVar(value="未檢查")
        self.python_var = tk.StringVar(value="未檢查")
        self.pwsh_var = tk.StringVar(value="未檢查")
        self.openclaw_var = tk.StringVar(value="未檢查")
        self.prefix_var = tk.StringVar(value="未檢查")
        self.requirements_var = tk.StringVar(value="未檢查")

        self._build_ui()
        self.after(150, self._drain_log_queue)
        self.refresh_status()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, padding=16)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        ttk.Label(
            header,
            text="OpenClaw 自動安裝與控制工具",
            font=("Microsoft JhengHei UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(header, textvariable=self.status_text).grid(row=0, column=1, sticky="e")

        controls = ttk.Frame(self, padding=(16, 0, 16, 12))
        controls.grid(row=1, column=0, sticky="nsew")
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        env_frame = ttk.LabelFrame(controls, text="環境與安裝", padding=12)
        env_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        env_frame.columnconfigure(1, weight=1)

        runtime_frame = ttk.LabelFrame(controls, text="執行與操作", padding=12)
        runtime_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        runtime_frame.columnconfigure(1, weight=1)

        self._add_status_row(env_frame, 0, "PowerShell 7", self.pwsh_var)
        self._add_status_row(env_frame, 1, "Node.js", self.node_var)
        self._add_status_row(env_frame, 2, "npm", self.npm_var)
        self._add_status_row(env_frame, 3, "Git", self.git_var)
        self._add_status_row(env_frame, 4, "Python", self.python_var)
        self._add_status_row(env_frame, 5, "OpenClaw", self.openclaw_var)
        self._add_status_row(env_frame, 6, "npm 全域路徑", self.prefix_var)
        self._add_status_row(env_frame, 7, "需求檢查", self.requirements_var)

        button_bar = ttk.Frame(env_frame)
        button_bar.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        button_bar.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Button(button_bar, text="重新檢查", command=self.refresh_status).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(button_bar, text="安裝/更新依賴", command=self.install_prerequisites).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(button_bar, text="安裝 OpenClaw", command=self.install_openclaw).grid(row=0, column=2, sticky="ew", padx=6)
        ttk.Button(button_bar, text="反安裝 OpenClaw", command=self.uninstall_openclaw).grid(row=0, column=3, sticky="ew", padx=(6, 0))

        self._add_status_row(runtime_frame, 0, "Gateway 狀態", self.gateway_state_var)

        ttk.Label(runtime_frame, text="Gateway Port").grid(row=1, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(runtime_frame, textvariable=self.port_var).grid(row=1, column=1, sticky="ew", pady=(12, 0))

        runtime_buttons = ttk.Frame(runtime_frame)
        runtime_buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        runtime_buttons.columnconfigure((0, 1), weight=1)
        runtime_buttons.columnconfigure((2, 3), weight=1)

        ttk.Button(runtime_buttons, text="啟動 Onboard", command=self.run_onboard).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 6))
        ttk.Button(runtime_buttons, text="啟動 Gateway", command=self.start_gateway).grid(row=0, column=1, sticky="ew", padx=6, pady=(0, 6))
        ttk.Button(runtime_buttons, text="停止 Gateway", command=self.stop_gateway).grid(row=1, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(runtime_buttons, text="開啟 Dashboard", command=self.open_dashboard).grid(row=1, column=1, sticky="ew", padx=6)
        ttk.Button(runtime_buttons, text="執行 Doctor", command=self.run_doctor).grid(row=0, column=2, sticky="ew", padx=6, pady=(0, 6))
        ttk.Button(runtime_buttons, text="清除日誌", command=self.clear_log).grid(row=1, column=2, sticky="ew", padx=6)

        notes = ttk.Label(
            runtime_frame,
            text=(
                "Onboard 會開新終端執行 `openclaw onboard --install-daemon`。\n"
                "Dashboard 預設使用 http://127.0.0.1:18789，必要時可修改 Port。"
            ),
            justify="left",
        )
        notes.grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 0))

        log_frame = ttk.LabelFrame(self, text="執行日誌", padding=16)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_widget = tk.Text(log_frame, wrap="word", font=("Consolas", 10), state="disabled")
        self.log_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_widget.configure(yscrollcommand=scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _add_status_row(self, parent: ttk.Widget, row: int, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Label(parent, textvariable=variable).grid(row=row, column=1, sticky="w", pady=2)

    def _detect_shell_executable(self) -> str:
        for candidate in ("pwsh", "powershell"):
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
        raise RuntimeError("找不到 pwsh 或 powershell，無法執行安裝腳本。")

    def _drain_log_queue(self) -> None:
        while True:
            try:
                message = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self.log_widget.configure(state="normal")
            self.log_widget.insert("end", f"{message}\n")
            self.log_widget.see("end")
            self.log_widget.configure(state="disabled")
        self.after(150, self._drain_log_queue)

    def log(self, message: str) -> None:
        self.log_queue.put(message.rstrip())

    def set_status(self, message: str) -> None:
        self.after(0, lambda: self.status_text.set(message))

    def clear_log(self) -> None:
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.configure(state="disabled")

    def _run_task(self, label: str, target) -> None:
        if self.task_running:
            messagebox.showinfo("工作進行中", "請先等待目前作業完成。")
            return

        def worker() -> None:
            self.task_running = True
            self.set_status(label)
            try:
                target()
            except Exception as exc:
                error_message = str(exc)
                self.log(f"[錯誤] {error_message}")
                self.after(0, lambda message=error_message: messagebox.showerror("執行失敗", message))
            finally:
                self.task_running = False
                self.set_status("準備就緒")

        threading.Thread(target=worker, daemon=True).start()

    def _powershell_command(self, extra_args: list[str]) -> list[str]:
        args = [self.shell_executable]
        if Path(self.shell_executable).name.lower().startswith("pwsh"):
            args.extend(["-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass"])
        else:
            args.extend(["-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass"])
        return args + extra_args

    def _run_helper_json(self, action: str) -> dict:
        command = self._powershell_command(["-File", str(HELPER_SCRIPT), "-Action", action])
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"{action} 執行失敗")
        payload = (result.stdout or "").strip()
        if not payload:
            raise RuntimeError(f"{action} 沒有回傳可解析的輸出。")
        return json.loads(payload)

    def _stream_process(self, command: list[str], on_complete=None) -> int:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        assert process.stdout is not None
        for line in process.stdout:
            self.log(line.rstrip())

        return_code = process.wait()
        if on_complete:
            on_complete(return_code)
        return return_code

    def _find_openclaw_executable(self) -> str | None:
        candidates = []
        if self.gateway_executable_path:
            candidates.append(self.gateway_executable_path)

        for name in ("openclaw.cmd", "openclaw.exe", "openclaw"):
            resolved = shutil.which(name)
            if resolved:
                candidates.append(resolved)

        npm_path = shutil.which("npm.cmd") or shutil.which("npm")
        if npm_path:
            result = subprocess.run(
                [npm_path, "prefix", "-g"],
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                prefix = result.stdout.strip()
                if prefix:
                    candidates.append(str(Path(prefix) / "openclaw.cmd"))

        for candidate in candidates:
            if candidate and Path(candidate).exists():
                self.gateway_executable_path = candidate
                return candidate

        return None

    def _resolve_openclaw_command(self) -> list[str]:
        executable = self._find_openclaw_executable()
        if executable:
            return [executable]
        return ["openclaw"]

    def refresh_status(self) -> None:
        def work() -> None:
            self.log("[資訊] 重新檢查系統環境與 OpenClaw 狀態")
            status = self._run_helper_json("status")
            self.after(0, lambda: self._apply_status(status))

        self._run_task("正在重新檢查環境", work)

    def _apply_status(self, status: dict) -> None:
        tools = status.get("tools", {})
        requirements = status.get("requirements", {})
        gateway = status.get("gateway", {})

        self.pwsh_var.set(self._format_tool_status(tools.get("pwsh")))
        self.node_var.set(self._format_tool_status(tools.get("node")))
        self.npm_var.set(self._format_tool_status(tools.get("npm")))
        self.git_var.set(self._format_tool_status(tools.get("git")))
        self.python_var.set(self._format_tool_status(tools.get("python") or tools.get("py")))
        self.openclaw_var.set(self._format_tool_status(tools.get("openclaw")))
        self.prefix_var.set(tools.get("npmGlobalPrefix") or "未取得")

        node_ok = requirements.get("nodeSatisfiesMinimum")
        node_recommended = requirements.get("nodeRecommended")
        pwsh7_ok = requirements.get("pwsh7Installed")
        req_parts = []
        req_parts.append(f"PowerShell 7: {'是' if pwsh7_ok else '否'}")
        req_parts.append(f"Node 最低版本: {'通過' if node_ok else '未通過'}")
        req_parts.append(f"Node 建議版本: {'通過' if node_recommended else '未通過'}")
        self.requirements_var.set(" | ".join(req_parts))

        running = gateway.get("running")
        pids = gateway.get("pids") or []
        self.gateway_state_var.set("執行中" + (f" (PID: {', '.join(str(pid) for pid in pids)})" if pids else "") if running else "未執行")

        resolved_path = tools.get("openclaw", {}).get("path") or tools.get("openclawResolvedPath")
        self.gateway_executable_path = resolved_path

        self.log("[資訊] 環境檢查完成")

    def _format_tool_status(self, tool_info: dict | None) -> str:
        if not tool_info:
            return "未檢查"
        if not tool_info.get("installed"):
            return "未安裝"
        version = tool_info.get("version") or "已安裝"
        path = tool_info.get("path")
        if path:
            return f"{version} | {path}"
        return version

    def install_prerequisites(self) -> None:
        def work() -> None:
            self.log("[執行] 安裝或更新 PowerShell 7 / Node.js / Git / Python")
            command = self._powershell_command(["-File", str(HELPER_SCRIPT), "-Action", "install-prerequisites"])
            return_code = self._stream_process(command)
            if return_code != 0:
                raise RuntimeError("安裝依賴失敗，請查看日誌。")
            self.log("[完成] 依賴安裝流程完成")
            status = self._run_helper_json("status")
            self.after(0, lambda: self._apply_status(status))

        self._run_task("正在安裝或更新依賴", work)

    def install_openclaw(self) -> None:
        def work() -> None:
            self.log("[執行] 安裝 OpenClaw 套件")
            command = self._powershell_command(["-File", str(HELPER_SCRIPT), "-Action", "install-openclaw"])
            return_code = self._stream_process(command)
            if return_code != 0:
                raise RuntimeError("安裝 OpenClaw 失敗，請查看日誌。")
            self.log("[完成] OpenClaw 安裝完成")
            status = self._run_helper_json("status")
            self.after(0, lambda: self._apply_status(status))

        self._run_task("正在安裝 OpenClaw", work)

    def uninstall_openclaw(self) -> None:
        if not messagebox.askyesno("確認", "確定要反安裝 OpenClaw 嗎？"):
            return

        def work() -> None:
            self.log("[執行] 反安裝 OpenClaw")
            command = self._powershell_command(["-File", str(HELPER_SCRIPT), "-Action", "uninstall-openclaw"])
            return_code = self._stream_process(command)
            if return_code != 0:
                raise RuntimeError("反安裝 OpenClaw 失敗，請查看日誌。")
            self.log("[完成] OpenClaw 反安裝完成")
            status = self._run_helper_json("status")
            self.after(0, lambda: self._apply_status(status))

        self._run_task("正在反安裝 OpenClaw", work)

    def run_onboard(self) -> None:
        try:
            command_text = "openclaw onboard --install-daemon"
            subprocess.Popen(
                self._powershell_command(["-NoExit", "-Command", command_text]),
                creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
            )
            self.log(f"[執行] 已在新終端啟動: {command_text}")
        except Exception as exc:
            messagebox.showerror("無法啟動 Onboard", str(exc))

    def start_gateway(self) -> None:
        if self.gateway_process and self.gateway_process.poll() is None:
            messagebox.showinfo("Gateway 執行中", "OpenClaw Gateway 已經在執行。")
            return

        port = self.port_var.get().strip() or DEFAULT_PORT
        if not port.isdigit():
            messagebox.showerror("Port 錯誤", "Gateway Port 必須是數字。")
            return

        command = self._resolve_openclaw_command() + ["gateway", "--port", port, "--verbose"]

        try:
            self.gateway_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            )
        except FileNotFoundError:
            messagebox.showerror("找不到 OpenClaw", "請先安裝 OpenClaw，或重新執行環境檢查。")
            return
        except Exception as exc:
            messagebox.showerror("無法啟動 Gateway", str(exc))
            return

        self.log(f"[執行] 啟動 Gateway: {' '.join(command)}")
        self.gateway_state_var.set("啟動中")

        def consume_gateway_output() -> None:
            assert self.gateway_process is not None
            assert self.gateway_process.stdout is not None
            for line in self.gateway_process.stdout:
                self.log(line.rstrip())
            return_code = self.gateway_process.wait()
            self.log(f"[資訊] Gateway 已結束，exit code = {return_code}")
            self.gateway_process = None
            self.after(0, self.refresh_status)

        threading.Thread(target=consume_gateway_output, daemon=True).start()
        self.after(1200, self.refresh_status)

    def stop_gateway(self) -> None:
        def work() -> None:
            self.log("[執行] 停止所有 OpenClaw Gateway 行程")
            command = self._powershell_command(["-File", str(HELPER_SCRIPT), "-Action", "stop-gateway"])
            return_code = self._stream_process(command)
            if return_code != 0:
                raise RuntimeError("停止 Gateway 失敗，請查看日誌。")
            self.gateway_process = None
            status = self._run_helper_json("status")
            self.after(0, lambda: self._apply_status(status))

        self._run_task("正在停止 Gateway", work)

    def open_dashboard(self) -> None:
        port = self.port_var.get().strip() or DEFAULT_PORT
        if not port.isdigit():
            messagebox.showerror("Port 錯誤", "Gateway Port 必須是數字。")
            return

        command = self._resolve_openclaw_command() + ["dashboard", "--no-open"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False, encoding="utf-8", errors="replace")
        except FileNotFoundError:
            messagebox.showerror("找不到 OpenClaw", "請先安裝 OpenClaw，或重新執行環境檢查。")
            return
        except Exception as exc:
            messagebox.showerror("無法取得 Dashboard URL", str(exc))
            return

        if result.returncode != 0:
            messagebox.showerror("無法取得 Dashboard URL", result.stderr.strip() or result.stdout.strip() or "openclaw dashboard 執行失敗。")
            return

        match = re.search(r"Dashboard URL:\s*(\S+)", result.stdout)
        if not match:
            messagebox.showerror("無法取得 Dashboard URL", "OpenClaw 沒有回傳可用的 Dashboard URL。")
            return

        dashboard_url = match.group(1)
        parsed = urlsplit(dashboard_url)
        host = parsed.hostname or "127.0.0.1"
        netloc = f"{host}:{port}"
        if parsed.username:
            credentials = parsed.username
            if parsed.password:
                credentials = f"{credentials}:{parsed.password}"
            netloc = f"{credentials}@{netloc}"
        url = urlunsplit((parsed.scheme or "http", netloc, parsed.path, parsed.query, parsed.fragment))
        webbrowser.open(url)
        self.log(f"[執行] 開啟 Dashboard: {url}")

    def run_doctor(self) -> None:
        def work() -> None:
            self.log("[執行] openclaw doctor")
            command = self._resolve_openclaw_command() + ["doctor"]
            return_code = self._stream_process(command)
            if return_code != 0:
                raise RuntimeError("OpenClaw doctor 執行失敗，請查看日誌。")
            self.log("[完成] OpenClaw doctor 執行完成")

        self._run_task("正在執行 OpenClaw doctor", work)

    def _on_close(self) -> None:
        if self.gateway_process and self.gateway_process.poll() is None:
            if not messagebox.askyesno("關閉程式", "Gateway 仍在執行，確定要直接關閉視窗嗎？"):
                return
        self.destroy()


def main() -> None:
    if not HELPER_SCRIPT.exists():
        raise SystemExit(f"找不到輔助腳本: {HELPER_SCRIPT}")
    app = OpenClawManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()