#!/usr/bin/env python3
"""
Windows Service for LINE練習相談 Application
24時間稼働対応
"""

import subprocess
import time
import logging
import logging.handlers
import sys
import os
import signal
import requests
from pathlib import Path

# ログディレクトリ作成
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            log_dir / "service.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class LineAppService:
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.max_restarts = 5
        self.check_interval = 30  # 30秒間隔でチェック
        self.running = True
        
        # アプリケーション起動コマンド
        self.app_command = [
            sys.executable, "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0", "--port", "8000", "--workers", "1"
        ]
        
    def start_app(self):
        """アプリケーションを起動"""
        try:
            if self.process and self.process.poll() is None:
                logger.info("Application is already running")
                return True
                
            logger.info(f"Starting application: {' '.join(self.app_command)}")
            self.process = subprocess.Popen(
                self.app_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 起動確認
            time.sleep(1)
            if self.process.poll() is None:
                logger.info(f"Application started successfully (PID: {self.process.pid})")
                return True
            else:
                logger.error("Application failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting application: {str(e)}")
            return False
    
    def stop_app(self):
        """アプリケーションを停止"""
        try:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                time.sleep(2)
                
                if self.process.poll() is None:
                    self.process.kill()
                    time.sleep(1)
                    
                logger.info("Application stopped successfully")
            else:
                logger.info("Application was not running")
                
        except Exception as e:
            logger.error(f"Error stopping application: {str(e)}")
    
    def check_health(self):
        """ヘルスチェック"""
        try:
            response = requests.get("http://localhost:8000/health/", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Health check failed: {str(e)}")
            return False
    
    def restart_app(self):
        """アプリケーションを再起動"""
        if self.restart_count >= self.max_restarts:
            logger.error(f"Maximum restart attempts ({self.max_restarts}) reached")
            return False
            
        self.restart_count += 1
        logger.info(f"Attempting restart ({self.restart_count}/{self.max_restarts})")
        
        self.stop_app()
        
        if self.start_app():
            logger.info("Restart successful")
            return True
        else:
            logger.error("Restart failed")
            return False
    
    def run(self):
        """メインサービスループ"""
        logger.info("LINE Training Consultation Application Service started")
        
        # 初回起動
        if not self.start_app():
            logger.error("Failed to start application initially")
            return
        
        # 監視ループ
        while self.running:
            try:
                time.sleep(self.check_interval)
                
                if not self.check_health():
                    logger.warning("Application is not responding")
                    if not self.restart_app():
                        logger.error("Failed to restart application, exiting")
                        break
                else:
                    # ヘルスチェック成功時は再起動カウントをリセット
                    if self.restart_count > 0:
                        self.restart_count = 0
                        logger.info("Application is healthy, restart count reset")
                
            except KeyboardInterrupt:
                logger.info("Service interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in service loop: {str(e)}")
                break
        
        # 終了処理
        logger.info("Stopping LINE Training Consultation Application Service")
        self.stop_app()
    
    def signal_handler(self, signum, frame):
        """シグナルハンドラ"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

def main():
    """メイン関数"""
    service = LineAppService()
    
    # シグナルハンドラ設定
    signal.signal(signal.SIGINT, service.signal_handler)
    signal.signal(signal.SIGTERM, service.signal_handler)
    
    try:
        service.run()
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 