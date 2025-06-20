#!/bin/bash

# LINE練習相談アプリケーション 監視スクリプト

LOG_FILE="/var/log/line-running-consultation-monitor.log"
SERVICE_NAME="line-running-consultation"
HEALTH_URL="http://localhost:8000/health/"
ALERT_EMAIL="admin@example.com"

# ログ関数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# アラート送信関数
send_alert() {
    local message="$1"
    log "🚨 アラート: $message"
    # メール送信（設定されている場合）
    if command -v mail &> /dev/null; then
        echo "$message" | mail -s "LINE練習相談アプリケーション アラート" "$ALERT_EMAIL"
    fi
}

# サービス状態チェック
check_service_status() {
    if ! systemctl is-active --quiet "$SERVICE_NAME"; then
        log "❌ サービスが停止しています"
        send_alert "サービス $SERVICE_NAME が停止しています"
        
        # 自動再起動試行
        log "🔄 サービス再起動を試行中..."
        systemctl restart "$SERVICE_NAME"
        sleep 10
        
        if systemctl is-active --quiet "$SERVICE_NAME"; then
            log "✅ サービス再起動成功"
            send_alert "サービス $SERVICE_NAME の再起動に成功しました"
        else
            log "❌ サービス再起動失敗"
            send_alert "サービス $SERVICE_NAME の再起動に失敗しました"
        fi
        return 1
    fi
    return 0
}

# ヘルスチェック
check_health() {
    if ! curl -f -s "$HEALTH_URL" > /dev/null; then
        log "❌ ヘルスチェック失敗"
        send_alert "ヘルスチェックが失敗しました: $HEALTH_URL"
        return 1
    fi
    return 0
}

# リソース使用量チェック
check_resources() {
    # CPU使用率チェック
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        log "⚠️ CPU使用率が高い: ${cpu_usage}%"
        send_alert "CPU使用率が高い: ${cpu_usage}%"
    fi
    
    # メモリ使用量チェック
    local mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    if (( $(echo "$mem_usage > 80" | bc -l) )); then
        log "⚠️ メモリ使用率が高い: ${mem_usage}%"
        send_alert "メモリ使用率が高い: ${mem_usage}%"
    fi
    
    # ディスク使用量チェック
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    if [ "$disk_usage" -gt 80 ]; then
        log "⚠️ ディスク使用率が高い: ${disk_usage}%"
        send_alert "ディスク使用率が高い: ${disk_usage}%"
    fi
}

# ログファイルサイズチェック
check_log_size() {
    local log_size=$(du -m /var/log/line-running-consultation-monitor.log 2>/dev/null | cut -f1)
    if [ "$log_size" -gt 100 ]; then
        log "📝 ログファイルが大きくなりました。ローテーションします。"
        mv "$LOG_FILE" "${LOG_FILE}.old"
        touch "$LOG_FILE"
    fi
}

# メイン処理
main() {
    log "🔍 監視チェック開始"
    
    # サービス状態チェック
    if ! check_service_status; then
        log "❌ サービス状態チェック失敗"
        exit 1
    fi
    
    # ヘルスチェック
    if ! check_health; then
        log "❌ ヘルスチェック失敗"
        exit 1
    fi
    
    # リソース使用量チェック
    check_resources
    
    # ログファイルサイズチェック
    check_log_size
    
    log "✅ 監視チェック完了"
}

# スクリプト実行
main "$@" 