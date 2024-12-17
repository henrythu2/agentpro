from fastapi.testclient import TestClient
from app.main import app

def test_chinese_text_clustering():
    """Test clustering endpoint with Chinese customer service texts"""
    client = TestClient(app)
    
    # Test data
    test_data = {
        "model_id": "kmeans",
        "texts": [
            "客服问题：手机无法开机，已经尝试强制重启",
            "客服问题：充电器插入后没有反应",
            "客服问题：屏幕突然黑屏，之前没有摔过"
        ]
    }
    
    # Test clustering endpoint
    response = client.post("/api/cluster", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

if __name__ == "__main__":
    success = test_chinese_text_clustering()
    print(f"Test {'passed' if success else 'failed'}")
