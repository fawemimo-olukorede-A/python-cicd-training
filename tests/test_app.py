"""
Unit and Integration Tests for Flask Application.
These tests run in the CI pipeline before any deployment.

LESSON: Why tests matter in CI/CD
- Tests run automatically on every push/PR
- Failing tests BLOCK deployment (prevent broken code in production)
- Give confidence that changes don't break existing functionality
"""
import pytest
from app import app


@pytest.fixture
def client():
    """
    Test client fixture.
    Creates a test client for making requests to the app.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# =============================================================================
# HEALTH CHECK TESTS (Critical for CI/CD)
# =============================================================================

class TestHealthEndpoints:
    """Tests for health check endpoints - these MUST pass for deployment."""

    def test_health_endpoint_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self, client):
        """Health endpoint should indicate healthy status."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_readiness_endpoint_returns_200(self, client):
        """Readiness endpoint should return 200 OK."""
        response = client.get('/ready')
        assert response.status_code == 200

    def test_readiness_endpoint_indicates_ready(self, client):
        """Readiness endpoint should indicate app is ready."""
        response = client.get('/ready')
        data = response.get_json()
        assert data['ready'] is True


# =============================================================================
# APPLICATION ROUTE TESTS
# =============================================================================

class TestApplicationRoutes:
    """Tests for main application routes."""

    def test_index_page_loads(self, client):
        """Index page should load successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_hello_with_name_returns_greeting(self, client):
        """Hello endpoint should return greeting with name."""
        response = client.post('/hello', data={'name': 'Student'})
        assert response.status_code == 200
        assert b'Student' in response.data

    def test_hello_without_name_redirects(self, client):
        """Hello endpoint should redirect if no name provided."""
        response = client.post('/hello', data={'name': ''})
        assert response.status_code == 302  # Redirect


# =============================================================================
# API ENDPOINT TESTS
# =============================================================================

class TestAPIEndpoints:
    """Tests for API endpoints."""

    def test_api_greet_returns_message(self, client):
        """API greet endpoint should return JSON greeting."""
        response = client.get('/api/greet/TestUser')
        assert response.status_code == 200
        data = response.get_json()
        assert 'Hello, TestUser!' in data['message']

    def test_api_add_numbers(self, client):
        """API add endpoint should sum two numbers."""
        response = client.post('/api/add',
                               json={'a': 5, 'b': 3},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 8

    def test_api_add_negative_numbers(self, client):
        """API add endpoint should handle negative numbers."""
        response = client.post('/api/add',
                               json={'a': -5, 'b': 3},
                               content_type='application/json')
        data = response.get_json()
        assert data['result'] == -2
