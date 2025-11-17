/**
 * 📦 TypeScript 類型定義 - 複製此檔案到你的 React 項目
 * 
 * 使用方式：
 * 1. 複製整個檔案到你的 React 項目 (src/types/iot-devices.ts)
 * 2. 導入類型：import { FlattenedGatewayData, FlattenedAnchorData } from './types/iot-devices'
 * 3. 享受 IDE 自動完成和類型檢查！
 * 
 * 最後更新：2025-11-17
 */

/**
 * ============================================
 * Gateway 相關類型
 * ============================================
 */

/**
 * 扁平化後的 Gateway 數據 (2層結構)
 * 
 * 第1層：設備基本信息
 * 第2層：事件數據（傳感器讀數、狀態等）
 * 
 * @example
 * const gateway: FlattenedGatewayData = {
 *   device_id: "gw_001",
 *   device_type: "gateway",
 *   device_name: "客廳網關",
 *   ip_address: "192.168.1.100",
 *   battery_voltage: 3.7,
 *   rssi: -45,
 *   timestamp: "2025-11-17T14:30:00Z"
 * };
 */
export interface FlattenedGatewayData {
  // ========== 第1層：設備基本信息 ==========

  /** 設備唯一 ID (不可變) */
  device_id: string;

  /** 設備類型，固定值："gateway" */
  device_type: "gateway";

  /** 人易讀的設備名稱 (例："客廳網關") */
  device_name: string;

  /** WiFi 連接的 IP 地址 (例："192.168.1.100") */
  ip_address?: string;

  /** MAC 地址 (例："00:1A:2B:3C:4D:5E") */
  mac_address?: string;

  // ========== 位置信息 ==========

  /** X 座標 (單位：米) */
  position_x?: number;

  /** Y 座標 (單位：米) */
  position_y?: number;

  /** Z 座標 (單位：米，通常代表樓層高度) */
  position_z?: number;

  // ========== 設備狀態 ==========

  /** 設備連接狀態："online" | "offline" */
  status: string;

  /** 是否已綁定到 Floor */
  is_bound: boolean;

  /** 設備創建時間 (ISO 8601 格式) */
  created_at?: string;

  /** 最後一次看到該設備的時間 (ISO 8601 格式) */
  last_seen?: string;

  // ========== 第2層：事件數據 ==========

  /** 電池電壓 (單位：V，範圍：2.0-5.0) */
  battery_voltage?: number;

  /** WiFi 信號強度 (單位：dBm，範圍：-200 ~ 0)
   * -45 = 最強，-60 = 強，-75 = 弱，-90 = 很弱
   */
  rssi?: number;

  /** 計算得出的信號品質等級："excellent" | "good" | "fair" | "poor" */
  signal_quality?: string;

  /** 固件版本 (例："v2.1.0") */
  fw_version?: string;

  /** 配置模式："auto" | "manual" */
  config_mode?: string;

  // ========== 時間戳 ==========

  /** 本次數據的時戳 (ISO 8601 格式) */
  timestamp?: string;

  /** Dataflow 處理時戳 (ISO 8601 格式) */
  processing_timestamp?: string;
}

/**
 * ============================================
 * Anchor 相關類型
 * ============================================
 */

/**
 * 扁平化後的 Anchor 數據 (2層結構)
 * 
 * 第1層：設備基本信息
 * 第2層：傳感器數據（生理數據、信號強度等）
 * 
 * @example
 * const anchor: FlattenedAnchorData = {
 *   device_id: "anchor_001",
 *   device_type: "anchor",
 *   device_name: "床位 1",
 *   gateway_id: "gw_001",
 *   heart_rate: 72,
 *   temperature: 36.5,
 *   timestamp: "2025-11-17T14:30:00Z"
 * };
 */
export interface FlattenedAnchorData {
  // ========== 第1層：設備基本信息 ==========

  /** 設備唯一 ID (例："anchor_001") */
  device_id: string;

  /** 設備類型，固定值："anchor" */
  device_type: "anchor";

  /** 人易讀的設備名稱 (例："床位 1 標籤") */
  device_name: string;

  /** 所屬 Gateway ID (例："gw_001") */
  gateway_id?: string;

  /** MAC 地址 (例："AA:BB:CC:DD:EE:FF") */
  mac_address?: string;

  // ========== 位置信息 ==========

  /** X 座標 (單位：米，UWB 定位) */
  position_x?: number;

  /** Y 座標 (單位：米，UWB 定位) */
  position_y?: number;

  /** Z 座標 (單位：米，通常代表樓層) */
  position_z?: number;

  // ========== 設備狀態 ==========

  /** 設備連接狀態："online" | "offline" */
  status: string;

  /** 是否已綁定到人員 */
  is_bound: boolean;

  /** 最後一次看到該設備的時間 */
  last_seen?: string;

  // ========== 第2層：傳感器數據 ==========

  /** 電池電壓 (單位：V，範圍：2.0-5.0) */
  battery_voltage?: number;

  /** WiFi/BLE 信號強度 (單位：dBm，範圍：-200 ~ 0) */
  rssi?: number;

  /** 心率 (單位：bpm，範圍：30-200)
   * 用於心率監測的穿戴設備
   */
  heart_rate?: number;

  /** 體溫 (單位：°C，範圍：35-42，精度：0.1°C)
   * 如果設備包含溫度傳感器
   */
  temperature?: number;

  /** 濕度 (單位：%，範圍：0-100)
   * 如果設備包含濕度傳感器
   */
  humidity?: number;

  // ========== 設備配置 ==========

  /** 是否需要固件更新 */
  fw_update?: boolean;

  /** LED 燈是否啟用 */
  led_enabled?: boolean;

  /** 藍牙是否啟用 */
  ble_enabled?: boolean;

  /** 是否為 UWB 發起者 */
  is_initiator?: boolean;

  // ========== 時間戳 ==========

  /** 本次數據的時戳 (ISO 8601 格式) */
  timestamp?: string;

  /** Dataflow 處理時戳 (ISO 8601 格式) */
  processing_timestamp?: string;
}

/**
 * ============================================
 * API 響應類型
 * ============================================
 */

/**
 * API 響應 - 單個 Gateway
 */
export interface GatewayResponse {
  success: boolean;
  data: FlattenedGatewayData;
  message?: string;
}

/**
 * API 響應 - Gateway 列表
 */
export interface GatewayListResponse {
  success: boolean;
  data: FlattenedGatewayData[];
  count: number;
  message?: string;
}

/**
 * API 響應 - 單個 Anchor
 */
export interface AnchorResponse {
  success: boolean;
  data: FlattenedAnchorData;
  message?: string;
}

/**
 * API 響應 - Anchor 列表
 */
export interface AnchorListResponse {
  success: boolean;
  data: FlattenedAnchorData[];
  count: number;
  message?: string;
}

/**
 * ============================================
 * 前端發送的格式 (用於 MQTT)
 * ============================================
 */

/**
 * 前端發送的 Gateway 原始格式 (4層嵌套)
 * 注意：這是 MQTT 消息格式，Dataflow 會轉換成 FlattenedGatewayData
 */
export interface GatewayMqttMessage {
  gateway_id: string;
  name: string;
  ip_address?: string;
  cloudData?: {
    id?: number;
    gateway_id?: number;
    pub?: {
      msg?: {
        data?: {
          battery_voltage?: number;
          rssi?: number;
        };
      };
    };
    fw_version?: string;
  };
}

/**
 * 前端發送的 Anchor 原始格式 (4層嵌套)
 * 注意：這是 MQTT 消息格式，Dataflow 會轉換成 FlattenedAnchorData
 */
export interface AnchorMqttMessage {
  anchor_id: string;
  gateway_id?: string;
  cloudData?: {
    pub?: {
      msg?: {
        data?: {
          heart_rate?: number;
          temperature?: number;
          rssi?: number;
          battery_voltage?: number;
        };
      };
    };
    fw_update?: number;
    led?: number;
    ble?: number;
    initiator?: number;
    position?: {
      x?: number;
      y?: number;
      z?: number;
    };
  };
}

/**
 * ============================================
 * 工具類型
 * ============================================
 */

/**
 * 設備類型聯合
 */
export type DeviceType = "gateway" | "anchor";

/**
 * 設備數據聯合
 */
export type DeviceData = FlattenedGatewayData | FlattenedAnchorData;

/**
 * 設備狀態
 */
export type DeviceStatus = "online" | "offline" | "unknown";

/**
 * 信號品質等級
 */
export type SignalQuality = "excellent" | "good" | "fair" | "poor";

/**
 * ============================================
 * 類型守衛（Type Guards）
 * ============================================
 */

/**
 * 檢查是否為 Gateway
 * @example
 * if (isGateway(device)) {
 *   console.log(device.ip_address);
 * }
 */
export function isGateway(device: DeviceData): device is FlattenedGatewayData {
  return device.device_type === "gateway";
}

/**
 * 檢查是否為 Anchor
 * @example
 * if (isAnchor(device)) {
 *   console.log(device.heart_rate);
 * }
 */
export function isAnchor(device: DeviceData): device is FlattenedAnchorData {
  return device.device_type === "anchor";
}

/**
 * ============================================
 * React Component Props 類型
 * ============================================
 */

/**
 * Gateway 卡片組件的 Props
 */
export interface GatewayCardProps {
  gateway: FlattenedGatewayData;
  onClick?: (gateway: FlattenedGatewayData) => void;
  onDelete?: (deviceId: string) => void;
}

/**
 * Anchor 卡片組件的 Props
 */
export interface AnchorCardProps {
  anchor: FlattenedAnchorData;
  onClick?: (anchor: FlattenedAnchorData) => void;
  onDelete?: (deviceId: string) => void;
}

/**
 * 設備列表組件的 Props
 */
export interface DeviceListProps {
  devices: DeviceData[];
  loading?: boolean;
  error?: string;
  onRefresh?: () => void;
}

/**
 * ============================================
 * 常數定義
 * ============================================
 */

/**
 * RSSI 信號強度分級
 */
export const RSSI_THRESHOLDS = {
  EXCELLENT: -50,   // -50 ~ 0: 最強信號
  GOOD: -70,        // -70 ~ -50: 好
  FAIR: -85,        // -85 ~ -70: 中等
  POOR: -100,       // -100 ~ -85: 弱
  // < -100: 無信號
} as const;

/**
 * 心率正常範圍
 */
export const HEART_RATE_RANGES = {
  NORMAL_LOW: 60,
  NORMAL_HIGH: 100,
  LOW_ALARM: 50,
  HIGH_ALARM: 120,
} as const;

/**
 * 體溫正常範圍
 */
export const TEMPERATURE_RANGES = {
  NORMAL_LOW: 36.0,
  NORMAL_HIGH: 37.5,
  MILD_FEVER: 38.0,
  HIGH_FEVER: 39.0,
} as const;

/**
 * 電池電壓警告範圍
 */
export const BATTERY_VOLTAGE_RANGES = {
  FULL: 4.0,
  GOOD: 3.5,
  MEDIUM: 3.0,
  WARNING: 2.5,
  CRITICAL: 2.0,
} as const;

/**
 * ============================================
 * 使用示例
 * ============================================
 */

/*
// 例子 1: 顯示 Gateway 信息
function GatewayDisplay({ gateway }: { gateway: FlattenedGatewayData }) {
  return (
    <div>
      <h3>{gateway.device_name}</h3>
      <p>IP: {gateway.ip_address}</p>
      <p>RSSI: {gateway.rssi} dBm</p>
      <p>信號: {gateway.signal_quality}</p>
      <p>電池: {gateway.battery_voltage}V</p>
    </div>
  );
}

// 例子 2: 顯示 Anchor 生理數據
function AnchorVitals({ anchor }: { anchor: FlattenedAnchorData }) {
  return (
    <div>
      <h3>{anchor.device_name}</h3>
      <p>心率: {anchor.heart_rate} bpm</p>
      <p>溫度: {anchor.temperature}°C</p>
      <p>RSSI: {anchor.rssi} dBm</p>
    </div>
  );
}

// 例子 3: 使用類型守衛
function DeviceInfo({ device }: { device: DeviceData }) {
  if (isGateway(device)) {
    return <div>Gateway: {device.ip_address}</div>;
  }
  if (isAnchor(device)) {
    return <div>Anchor: Heart Rate {device.heart_rate} bpm</div>;
  }
  return <div>Unknown device</div>;
}
*/

export default {
  isGateway,
  isAnchor,
  RSSI_THRESHOLDS,
  HEART_RATE_RANGES,
  TEMPERATURE_RANGES,
  BATTERY_VOLTAGE_RANGES,
};

