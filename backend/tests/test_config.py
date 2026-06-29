from app.core.settings import get_settings

def test_settings_load_correctly():
    settings = get_settings()
    assert settings.PROJECT_NAME == "Legal RAG API"
    assert settings.CHUNK_SIZE == 500
    assert settings.OCR_ENGINE == "PaddleOCR"
