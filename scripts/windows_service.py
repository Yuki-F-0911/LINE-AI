"""
Windows Service用 LINE練習相談アプリケーション
"""

import sys
import os
import subprocess
import time
import logging
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ログ設定
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "service.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class LineRunningConsultationService:
    """LINE練習相談アプリケーション Windows Service"""
    
    def __init__(self):
        self.process = None
        self.running = False
        self.restart_count = 0
        self.max_restarts = 5
        
    def start_app(self):
        """アプリケーション起動"""
        try:
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--workers", "1"
            ]
            
            logger.info(f"アプリケーションを起動中: {' '.join(cmd)}")
            
            self.process = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"アプリケーションが起動しました (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"アプリケーション起動エラー: {str(e)}")
            return False
    
    def stop_app(self):
        """アプリケーション停止"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
                logger.info("アプリケーションを正常に停止しました")
            except subprocess.TimeoutExpired:
                self.process.kill()
                logger.warning("アプリケーションを強制終了しました")
            except Exception as e:
                logger.error(f"アプリケーション停止エラー: {str(e)}")
            finally:
                self.process = None
    
    def is_app_running(self):
        """アプリケーション稼働確認"""
        if not self.process:
            return False
        
        # プロセスの状態確認
        if self.process.poll() is not None:
            return False
        
        # ヘルスチェック
        try:
            import requests
            response = requests.get("http://localhost:8000/health/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def monitor_and_restart(self):
        """監視・自動再起動"""
        while self.running:
            try:
                if not self.is_app_running():
                    logger.warning("アプリケーションが停止しています")
                    
                    if self.restart_count < self.max_restarts:
                        logger.info(f"再起動を試行中 ({self.restart_count + 1}/{self.max_restarts})")
                        self.stop_app()
                        
                        if self.start_app():
                            self.restart_count = 0
                            logger.info("再起動に成功しました")
                        else:
                            self.restart_count += 1
                            logger.error(f"再起動に失敗しました ({self.restart_count}/{self.max_restarts})")
                    else:
                        logger.critical("最大再起動回数に達しました。サービスを停止します。")
                        self.running = False
                        break
                
                # 30秒間隔で監視
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("キーボード割り込みを受信しました")
                self.running = False
                break
            except Exception as e:
                logger.error(f"監視エラー: {str(e)}")
                time.sleep(10)
    
    def run(self):
        """サービス実行"""
        logger.info("LINE練習相談アプリケーションサービスを開始します")
        
        self.running = True
        
        # 初回起動
        if not self.start_app():
            logger.critical("初回起動に失敗しました")
            return
        
        try:
            # 監視・自動再起動ループ
            self.monitor_and_restart()
        finally:
            # 終了処理
            self.stop_app()
            logger.info("LINE練習相談アプリケーションサービスを終了しました")

def main():
    """メイン関数"""
    service = LineRunningConsultationService()
    service.run()

if __name__ == "__main__":
    main() 