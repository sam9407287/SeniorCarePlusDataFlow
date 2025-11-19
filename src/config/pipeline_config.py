"""Pipeline 配置管理"""

import os
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Pipeline 配置類"""
    
    # GCP 配置
    project_id: str
    region: str = "asia-east1"
    
    # Pub/Sub 配置
    gateway_pubsub_topic: Optional[str] = None
    anchor_pubsub_topic: Optional[str] = None
    
    # BigQuery 配置
    bigquery_dataset: str = "senior_care_analytics"
    gateway_table: str = "gateway_events"
    anchor_table: "anchor_events"
    
    # 儲存空間配置
    gcs_temp_bucket: str = None
    gcs_staging_bucket: str = None
    
    # Pipeline 配置
    batch_size: int = 1000
    max_num_workers: int = 10
    temp_location: str = None
    staging_location: str = None
    
    # 日誌配置
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Post-initialization validation"""
        if not self.project_id:
            raise ValueError("project_id 不能為空")
        
        if not self.temp_location:
            self.temp_location = f"gs://{self.gcs_temp_bucket}/temp"
        
        if not self.staging_location:
            self.staging_location = f"gs://{self.gcs_staging_bucket}/staging"


def get_config(env: str = "dev") -> Config:
    """
    讀取配置文件
    
    Args:
        env: 環境名稱 ("dev", "test", "prod")
        
    Returns:
        Config 對象
    """
    
    # 優先讀取環境變數
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "asia-east1")
    
    # 如果環境變數未設置，讀取 YAML 配置文件
    if not project_id:
        config_file = os.path.join(
            os.path.dirname(__file__),
            f"../../../config/{env}.yaml"
        )
        
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
        else:
            # 使用默認配置
            config_data = {
                "project_id": "your-gcp-project-id",
                "region": "asia-east1"
            }
    else:
        config_data = {
            "project_id": project_id,
            "region": region
        }
    
    return Config(**config_data)


# 預設配置
DEFAULT_CONFIG = {
    "dev": {
        "project_id": "senior-care-plus-dev",
        "region": "asia-east1",
        "gcs_temp_bucket": "senior-care-dev-temp",
        "gcs_staging_bucket": "senior-care-dev-staging",
        "log_level": "DEBUG"
    },
    "test": {
        "project_id": "senior-care-plus-test",
        "region": "asia-east1",
        "gcs_temp_bucket": "senior-care-test-temp",
        "gcs_staging_bucket": "senior-care-test-staging",
        "log_level": "INFO"
    },
    "prod": {
        "project_id": "senior-care-plus-prod",
        "region": "asia-east1",
        "gcs_temp_bucket": "senior-care-prod-temp",
        "gcs_staging_bucket": "senior-care-prod-staging",
        "log_level": "WARNING"
    }
}




